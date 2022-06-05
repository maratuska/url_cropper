from fastapi import FastAPI, APIRouter

from app.connections.db import init_db_and_tables
from app.settings import AppConfig
from app.api.handlers import router as api_router


__all__ = [
    'AppManager',
]


class AppManager:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._app = self._create_app()
        self._configure_routing()

    def _create_app(self) -> FastAPI:
        return FastAPI(
            debug=self._config.api_settings.debug,
            on_startup=[self._on_startup],
        )

    def _configure_routing(self):
        self._router = APIRouter()
        self._router.include_router(prefix='/api', router=api_router)
        self._app.include_router(router=self._router)

    @classmethod
    async def _on_startup(cls):
        await init_db_and_tables()

    @property
    def app_instance(self) -> FastAPI:
        return self._app
