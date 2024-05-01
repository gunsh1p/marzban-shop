from fastapi import Request
from fastapi.responses import RedirectResponse

from db.models import Admin

class CheckAuthMiddleware:
    async def __call__(self, request: Request, call_next):
        if url.startswith("/api"):
            response = await call_next(request)
            return response
        url = request.url.path
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
                url="/dashboard/",
                status_code=302
            )
        response = await call_next(request)
        return response