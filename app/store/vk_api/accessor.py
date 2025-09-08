import typing
from urllib.parse import urlencode, urljoin

from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application

API_VERSION = "5.131"
URL = "https://api.vk.com/method/groups.getLongPollServer"


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.server: str | None = None
        self.poller: Poller | None = None
        self.ts: int | None = None

    async def connect(self, app: "Application"):
        # TODO: добавить создание aiohttp ClientSession,
        #  получить данные о long poll сервере с помощью метода groups.getLongPollServer
        #  вызвать метод start у Poller
        self.app = app
        self.session = ClientSession()
        await self._get_long_poll_service()

        self.poller = Poller(store=self.app.store)
        await self.poller.start()


    async def disconnect(self, app: "Application"):
        # TODO: закрыть сессию и завершить поллер
        await self.session.close()
        await self.poller.stop()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        params.setdefault("v", API_VERSION)
        return f"{urljoin(host, method)}?{urlencode(params)}"

    async def _get_long_poll_service(self):
        self.server = "https://example.com"
        self.key = "test_key"
        self.ts = 12345

    async def poll(self):
        pass

    async def send_message(self, message: Message) -> None:
        pass
