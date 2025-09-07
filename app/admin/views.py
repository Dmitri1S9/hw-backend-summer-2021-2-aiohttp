from aiohttp.web_exceptions import HTTPForbidden
import hashlib

from aiohttp_apispec import response_schema, docs, request_schema
from .schemes import AdminSchema

from app.web.app import View
from aiohttp.web_response import json_response
from ..web.schemes import OkResponseSchema

class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        email = data.get('email')
        password = hashlib.sha256(data.get('password').encode()).hexdigest()

        admin_ = await self.store.admins.get_by_email(email)
        if admin_.password != password:
            raise HTTPForbidden

        return json_response({
            "status": "ok",
            "data": {"id": admin_.id, "email": admin_.email}
        })


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
