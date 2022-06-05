from abc import ABC

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.connections.db import get_session


__all__ = [
    'AbstractService'
]


class AbstractService(ABC):
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session
