import json
import typing

from aiohttp.web_exceptions import (HTTPUnprocessableEntity, HTTPBadRequest, HTTPUnauthorized,
HTTPForbidden, HTTPNotFound, HTTPNotImplemented, HTTPConflict, HTTPInternalServerError)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from marshmallow import ValidationError

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text) if e.text else {},
        )
    except HTTPBadRequest as e:
        error_code = int(e.status_code)
        return error_json_response(
            http_status=error_code,
            status=HTTP_ERROR_CODES[error_code],
            message=e.reason,
            data={"details": e.text} if e.text else {},
        )
    except HTTPUnauthorized as e:
        error_code = int(e.status_code)
        return error_json_response(
            http_status=error_code,
            status=HTTP_ERROR_CODES[error_code],
            message=e.reason,
            data={"data": e.text} if e.text else {},
        )
    except HTTPForbidden as e:
        error_code = int(e.status_code)
        return error_json_response(
            http_status=error_code,
            status=HTTP_ERROR_CODES[error_code],
            message=e.reason,
            data={"details": e.text} if e.text else {},
        )
    except HTTPNotFound as e:
        error_code = int(e.status_code)
        return error_json_response(
            http_status=error_code,
            status=HTTP_ERROR_CODES[error_code],
            message=e.reason,
            data={"details": e.text} if e.text else {},
        )
    except HTTPNotImplemented as e:
        error_code = int(e.status_code)
        return error_json_response(
            http_status=error_code,
            status=HTTP_ERROR_CODES[error_code],
            message=e.reason,
            data={"details": e.text} if e.text else {},
        )
    except HTTPConflict as e:
        error_code = int(e.status_code)
        return error_json_response(
            http_status=error_code,
            status=HTTP_ERROR_CODES[error_code],
            message=e.reason,
            data={"details": e.text} if e.text else {},
        )
    except HTTPInternalServerError as e:
        error_code = int(e.status_code)
        return error_json_response(
            http_status=error_code,
            status=HTTP_ERROR_CODES[error_code],
            message=e.reason,
            data={"details": e.text} if e.text else {},
        )
    # except Exception as e:
    #     return error_json_response(
    #         status=HTTP_ERROR_CODES[500],
    #         message="Upps... Server error):",
    #         data={},
    #     )

    return response
    # TODO: обработать все исключения-наследники HTTPException и отдельно Exception, как server error
    #  использовать текст из HTTP_ERROR_CODES


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
