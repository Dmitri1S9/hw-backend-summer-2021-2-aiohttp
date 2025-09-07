from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)

from app.admin.models import Admin
from app.store import Store, setup_store
from app.store.database.database import Database
from app.web.config import Config, setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes
from aiohttp_apispec import setup_aiohttp_apispec


class Application(AiohttpApplication):
    config: Config | None = None
    store: Store | None = None
    database: Database = Database()


class Request(AiohttpRequest):
    admin: Admin | None = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


app = Application()


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    setup_store(app)
    setup_aiohttp_apispec(
        app=app,
        title="My API",
        version="v1",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs",
    )
    setup_middlewares(app)
    setup_routes(app)
    return app
