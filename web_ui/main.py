from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from services.git_ops import open_repo, create_branch, commit_all, push_branch, repo_diff
from services.code_analyzer import list_files, read_file, write_file
from services.ai_agent import generate_patch
from logging_config import configure_logging, logger
from uuid import uuid4
import os

app = FastAPI()
BASE_REPO_PATH = Path(os.environ.get("REPO_PATH", "."))

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")
configure_logging(level=os.environ.get("LOG_LEVEL", "INFO"))


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))
    with logger.contextualize(request_id=request_id):
        response = await call_next(request)
    return response


def get_repo():
    return open_repo(str(BASE_REPO_PATH))


@app.get("/", response_class=HTMLResponse)
def index(request: Request, path: str = ""):
    repo = get_repo()
    files = list_files(repo.working_tree_dir, path)
    return templates.TemplateResponse("index.html", {"request": request, "files": files, "path": path})


@app.get("/edit", response_class=HTMLResponse)
def edit_file(request: Request, file_path: str):
    content = read_file(BASE_REPO_PATH, file_path)
    return templates.TemplateResponse("edit.html", {"request": request, "content": content, "file_path": file_path})


@app.post("/save")
def save_file(file_path: str = Form(...), content: str = Form(...)):
    write_file(BASE_REPO_PATH, file_path, content)
    return RedirectResponse(url=f"/edit?file_path={file_path}", status_code=302)


@app.post("/generate")
def generate(file_path: str = Form(...), prompt: str = Form(...)):
    patch = generate_patch(prompt)
    write_file(BASE_REPO_PATH, file_path, patch)
    return RedirectResponse(url=f"/edit?file_path={file_path}", status_code=302)


@app.post("/commit")
def commit(message: str = Form(...)):
    repo = get_repo()
    create_branch(repo, message)
    commit_all(repo, message)
    push_branch(repo, repo.active_branch.name)
    return {"diff": repo_diff(repo)}
