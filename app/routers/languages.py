from fastapi import APIRouter, Request, FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

from db.models import Language, Scene
from constants import language_template

router = APIRouter(prefix="/languages")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_languages_page(request: Request):
    return templates.TemplateResponse(request=request, name='languages.html')

@router.get("/get", response_class=JSONResponse)
async def get_languages():
    ls = await Language.all()
    content = {
        'data': [lang.to_dict() for lang in ls]
    }
    return JSONResponse(content=content)

@router.post('/add', response_class=JSONResponse)
async def add_language(title: str = Form(default = ''), code: str = Form(default = '')):
    if len(code) == 0 or len(title) == 0:
        content = {
            'error': 'Invalid data!'
        }
        return JSONResponse(
            content=content,
            status_code=400
        )
    is_exists = await Language.get_or_none(code=code)

    if is_exists is not None:
        content = {
            'error': 'Current language code already exists!'
        }
        return JSONResponse(
            content=content,
            status_code=400
        )
    lang = await Language.create(
        title=title,
        code=code
    )
    for t, v in language_template.SCENES.items():
        for a, txt in v.items():
            await Scene.create(title=t, action=a, text=txt, language=lang)
    content = {
        'data': lang.to_dict()
    }
    return JSONResponse(content=content)

@router.get('/scenes', response_class=JSONResponse)
async def get_scenes(title: str = ''):
    language = await Language.get_or_none(title=title)
    scenes = await Scene.filter(language=language).all()
    content = {
        'data': [await scene.to_dict() for scene in scenes]
    }

    return JSONResponse(content=content)

@router.put('/update', response_class=JSONResponse)
async def update_scene(lang_title: str = Form(default = ''), scene_title: str = Form(default = ''), action: str = Form(default = ''), text: str = Form(default='')):
    if len(lang_title) == 0 or len(scene_title) == 0 or len(action) == 0 or len(text) == 0:
        content = {
            'error': 'Invalid data!'
        }
        return JSONResponse(
            content=content,
            status_code=400
        )
    language = await Language.get_or_none(title=lang_title)
    if language is None:
        content = {
            'error': 'Invalid language!'
        }
        return JSONResponse(
            content=content,
            status_code=400
        )
    scene = await Scene.get_or_none(title=scene_title, action=action, language=language)
    if scene is None:
        content = {
            'error': 'Invalid scene!'
        }
        return JSONResponse(
            content=content,
            status_code=400
        )
    scene.text = text
    await scene.save()
    content = {
        'data': await scene.to_dict()
    }
    return JSONResponse(content=content)


def register_router(app: FastAPI) -> None:
    app.include_router(router)