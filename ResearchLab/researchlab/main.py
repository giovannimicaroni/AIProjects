from fastapi import FastAPI, HTTPException, Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from researchlab.agents.searcher import SearcherAgent
from starlette.middleware.sessions import SessionMiddleware
from fastapi.concurrency import run_in_threadpool
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI()
router = APIRouter()

app.add_middleware(
    SessionMiddleware,
    secret_key="ENTER API KEY",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    message: str


@router.get("/settings", response_class=HTMLResponse)
def settings_page():
    return (STATIC_DIR / "settings.html").read_text()


@router.post("/settings")
def set_api_key(request: Request, api_key: str = Form(...)):
    if not api_key.startswith("sk-"):
        raise HTTPException(400, "Invalid API key")

    response = RedirectResponse("/", status_code=302)
    request.session["openai_api_key"] = api_key
    return response


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    if "openai_api_key" not in request.session:
        return RedirectResponse("/settings")
    return (STATIC_DIR / "index.html").read_text()


@router.post("/chat")
async def chat(request: Request, payload: ChatRequest):
    api_key = request.session.get("openai_api_key")
    if not api_key:
        raise HTTPException(401, "API key not set")

    agent = SearcherAgent(openai_api_key=api_key)

    result = await run_in_threadpool(
        agent.run_query, payload.message
    )

    return {"answer": result}


app.include_router(router)
