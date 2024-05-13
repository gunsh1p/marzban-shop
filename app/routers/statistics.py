from datetime import datetime, timedelta

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from db.models import Buy

router = APIRouter(prefix='/statistics')
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_statistics_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="statistics.html"
    )

@router.get("/buys", response_class=JSONResponse)
async def get_buys(start: str = 0, end: str = 0):
    if start == 0:
        start = (datetime.now() - timedelta(days=6)).strftime('%d-%m-%Y')
    if end == 0:
        end = datetime.now().strftime('%d-%m-%Y')
    try:
        start_date = datetime.strptime(start, '%d-%m-%Y')
        end_date = datetime.strptime(end, '%d-%m-%Y') + timedelta(days=1)
    except ValueError:
        content = {
            "message": 'Invalid start or end date'
        }
        response = JSONResponse(content=content, status_code=400)
        return response
    buys = await Buy.filter(time__gte=start_date, time__lt=end_date).all()
    content = {
        "data": [buy.to_dict() for buy in buys]
    }
    response = JSONResponse(content=content)
    return response



def register_router(app: FastAPI) -> None:
    app.include_router(router)