from fastapi import FastAPI, APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/statistics')
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_statistics_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="statistics.html"
    )

def register_router(app: FastAPI) -> None:
    app.include_router(router)