from fastapi import Request
from fastapi.responses import RedirectResponse

from db.models import Admin

class CheckAuthMiddleware:
    async def __call__(self, request: Request, call_next):
        url = request.url.path
        if url.startswith("/api"):
            response = await call_next(request)
            return response
        username: str = request.cookies.get('username')
        password: str = request.cookies.get('password')
        if not (username or password) and not url.startswith("/auth"):
            return RedirectResponse(
                url="/auth/",
                status_code=302
            )
        is_existed = await Admin.get_or_none(username=username, password=password)
        if is_existed and url.startswith("/auth"):
            return RedirectResponse(
                url="/statistics/",
                status_code=302
            )
        if not is_existed and not url.startswith("/auth"):
            response = RedirectResponse(
                url="/auth/",
                status_code=302
            )
            response.delete_cookie('username', httponly=True)
            response.delete_cookie('password', httponly=True)
            return response
        response = await call_next(request)
        return response