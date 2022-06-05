from typing import Optional

from pydantic.networks import AnyHttpUrl
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlmodel import SQLModel, Field


class OriginUrlBase(SQLModel):
    url: AnyHttpUrl = Field(
        sa_column=Column(
            'url',
            String,
            unique=True,
        ),
    )


class OriginUrl(OriginUrlBase, table=True):
    __tablename__ = 'origin_urls'

    id: Optional[int] = Field(default=None, primary_key=True)


class OriginUrlRead(OriginUrlBase):
    id: int


class ShortUrlBase(SQLModel):
    url: AnyHttpUrl
    origin_url_id: int


class ShortUrl(ShortUrlBase, table=True):
    __tablename__ = 'short_urls'

    id: Optional[int] = Field(default=None, primary_key=True)
    origin_url_id: int = Field(
        sa_column=Column(
            'origin_url_id',
            Integer,
            ForeignKey('origin_urls.id', ondelete='CASCADE'),
            nullable=False,
        ),
    )


class ShortUrlRead(ShortUrlBase):
    id: int


class ShortUrlCreate(SQLModel):
    origin_url: AnyHttpUrl
