from fastapi import APIRouter, Depends, status, HTTPException
from pydantic.networks import AnyHttpUrl

from app.api.exceptions import DuplicateUrlError, UrlNotFound
from app.api.service import UrlService
from app.api.models import ShortUrlRead, ShortUrlCreate, OriginUrlRead


__all__ = [
    'router',
]


router = APIRouter(prefix='/url')


@router.post('/', response_model=ShortUrlRead, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url_create: ShortUrlCreate,
    service: UrlService = Depends(),
):
    try:
        new_url = await service.create_short_url(url_create=url_create)
    except DuplicateUrlError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    return new_url


@router.delete('/')
async def delete_by_short_url(
    short_url: AnyHttpUrl,
    service: UrlService = Depends(),
):
    try:
        await service.delete_url(short_url=short_url)
    except UrlNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/origin', response_model=OriginUrlRead)
async def get_origin_url(
    short_url: AnyHttpUrl,
    service: UrlService = Depends(),
):
    try:
        origin_url_read = await service.get_origin_url_by_short(short_url=short_url)
    except UrlNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return origin_url_read
