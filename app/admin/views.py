from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
import hashlib

from aiohttp_apispec import response_schema, docs, request_schema
from .schemes import AdminSchema

from app.web.app import View

from ..web.schemes import OkResponseSchema
from ..web.utils import json_response


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

        response = json_response(
            data={"id": admin_.id, "email": admin_.email}
        )
        response.set_cookie("email", str(admin_.email))
        response.set_cookie("id", str(admin_.id))
        return response


class AdminCurrentView(View):
    @response_schema(OkResponseSchema, 200)
    async def get(self):
        admin_id = self.request.cookies.get("id")
        admin_email = self.request.cookies.get("email")
        if not admin_email or not admin_id:
            raise HTTPUnauthorized

        return json_response(
            data={
                "id": int(admin_id),
                "email": admin_email
            }
        )
