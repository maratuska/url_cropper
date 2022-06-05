import shortuuid
from sqlalchemy import exists
from sqlmodel import select

from app.abc import AbstractService
from app.api.exceptions import DuplicateUrlError, UrlNotFound
from app.api.models import ShortUrlCreate, ShortUrlRead, OriginUrl, ShortUrl
from app.settings import conf


class UrlService(AbstractService):
    _short_base_url: str = conf.api_settings.short_base_url

    async def create_short_url(self, url_create: ShortUrlCreate) -> ShortUrl:
        if await self._is_origin_url_exists(origin_url_value=url_create.origin_url):
            raise DuplicateUrlError(f'Origin url {url_create.origin_url} already exists')

        origin_url = OriginUrl(url=url_create.origin_url)
        self._session.add(origin_url)
        await self._session.commit()

        short_url_value = _create_short_url_by_origin(
            origin_url=url_create.origin_url,
            short_base_url=self._short_base_url,
        )
        short_url = ShortUrl(
            url=short_url_value,
            origin_url_id=origin_url.id,
        )
        self._session.add(short_url)
        await self._session.commit()

        return short_url

    async def delete_url(self, short_url: str) -> None:
        origin_url = await self.get_origin_url_by_short(short_url=short_url)

        await self._session.delete(origin_url)
        await self._session.commit()

    async def get_origin_url_by_short(self, short_url: str) -> OriginUrl:
        short_url = await self.get_short_url(short_url_value=short_url)
        origin_url = await self.get_origin_url_by_id(url_id=short_url.origin_url_id)

        return origin_url

    async def get_origin_url_by_id(self, url_id: int) -> OriginUrl:
        origin_url = await self._session.get(entity=OriginUrl, ident=url_id)
        if origin_url is None:
            raise UrlNotFound

        return origin_url

    async def get_short_url(self, short_url_value: str) -> ShortUrl:
        statement = select(ShortUrl).where(ShortUrl.url == short_url_value)
        results = await self._session.execute(statement=statement)
        short_url = results.scalar_one_or_none()
        if short_url is None:
            raise UrlNotFound

        return short_url

    async def _is_origin_url_exists(self, origin_url_value) -> bool:
        statement = exists(OriginUrl).select(OriginUrl.url == origin_url_value)
        result = await self._session.execute(statement=statement)
        is_exists = result.scalar()
        return is_exists


def _create_short_url_by_origin(origin_url: str, short_base_url: str) -> str:
    token = shortuuid.uuid(name=origin_url)
    short_url = f'{short_base_url}/{token}'
    return short_url
