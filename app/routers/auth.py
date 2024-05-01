from typing import Union

from fastapi import FastAPI, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from db.models import Admin
from utils.get_password_hash import get_password_hash

router = APIRouter(prefix='/auth')
templates = Jinja2Templates(directory="templates")

@router.get('/', response_class=HTMLResponse)
async def get_auth_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="auth.html"
    )

@router.post('/', response_class=Union[HTMLResponse, RedirectResponse])
async def check_auth(request: Request, username: str = Form(default = ""), password: str = Form(default=""), remember: str = Form(default="")):
    if not (username or password):
        context = {
            'error': 'Invalid data!'
        }
        return templates.TemplateResponse(
            request=request, 
            name="auth.html",
            context=context
        )
    hashed_password = get_password_hash(password)
    is_existed = await Admin.get_or_none(
        username=username, 
        password=hashed_password
    )
    if not is_existed:
        context = {
            'error': 'Invalid data!'
        }
        return templates.TemplateResponse(
            request=request, 
            name="auth.html",
            context=context
        )
    response = RedirectResponse(
        url="/statistics/",
        status_code=302
    )
    max_age = None if remember == '1' else 3600 * 24
    response.set_cookie(key='username', value=username, httponly=True, max_age=max_age)
    response.set_cookie(key='password', value=hashed_password, httponly=True, max_age=max_age)
    return response

def register_router(app: FastAPI) -> None:
    app.include_router(router)