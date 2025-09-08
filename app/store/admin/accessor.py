import hashlib
import typing

from aiohttp.web_exceptions import HTTPForbidden

from app.admin.models import Admin
from app.base.base_accessor import BaseAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        new_admin = await self.create_admin(self.app.config.admin.email,
                                            self.app.config.admin.password)
        self.app.database.admins.append(new_admin)

    async def get_by_email(self, email: str) -> Admin | None:
        if not email: raise HTTPForbidden
        for admin_ in self.app.database.admins:
            if admin_.email == email:
                return admin_
        raise HTTPForbidden

    async def create_admin(self, email: str, password: str) -> Admin:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return Admin(len(self.app.database.admins) + 1, email, hashed_password)

