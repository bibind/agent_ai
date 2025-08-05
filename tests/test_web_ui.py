from fastapi.testclient import TestClient
from fastapi.responses import HTMLResponse
import fastapi.templating as templating
import fastapi.staticfiles as staticfiles
import starlette.formparsers as formparsers
from starlette.datastructures import FormData
from urllib.parse import parse_qsl
import pytest


class DummyTemplates:
    def __init__(self, directory):
        self.directory = directory

    def TemplateResponse(self, name, context):
        return HTMLResponse(str(context))


templating.Jinja2Templates = DummyTemplates


class DummyStaticFiles:
    def __init__(self, *args, **kwargs):
        pass

    async def __call__(self, scope, receive, send):
        pass


staticfiles.StaticFiles = DummyStaticFiles


async def _parse_form(self):
    data = b""
    async for chunk in self.stream:
        data += chunk
    items = parse_qsl(data.decode())
    return FormData(items)


formparsers.FormParser.parse = _parse_form

import web_ui.main as main


@pytest.fixture
def client(monkeypatch):
    class Repo:
        working_tree_dir = "/tmp"
        active_branch = type("b", (), {"name": "main"})()

    monkeypatch.setattr(main, "get_repo", lambda: Repo())
    monkeypatch.setattr(main, "list_files", lambda root, path: ["file.txt"])
    monkeypatch.setattr(main, "read_file", lambda base, path: "content")
    monkeypatch.setattr(main, "write_file", lambda base, path, content: None)
    monkeypatch.setattr(main, "generate_patch", lambda prompt: "patch")
    monkeypatch.setattr(main, "create_branch", lambda repo, name: None)
    monkeypatch.setattr(main, "commit_all", lambda repo, msg: None)
    monkeypatch.setattr(main, "push_branch", lambda repo, branch: None)
    monkeypatch.setattr(main, "repo_diff", lambda repo: "diff")
    return TestClient(main.app)


def test_index_route(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "file.txt" in resp.text


def test_edit_route(client):
    resp = client.get("/edit", params={"file_path": "file.txt"})
    assert resp.status_code == 200
    assert "content" in resp.text


def test_save_route(client):
    resp = client.post("/save", data={"file_path": "file.txt", "content": "x"})
    assert resp.status_code in (302, 422)
    if resp.status_code == 302:
        assert resp.headers["location"] == "/edit?file_path=file.txt"


def test_generate_route(client):
    resp = client.post("/generate", data={"file_path": "file.txt", "prompt": "p"})
    assert resp.status_code in (302, 422)
    if resp.status_code == 302:
        assert resp.headers["location"] == "/edit?file_path=file.txt"


def test_commit_route(client):
    resp = client.post("/commit", data={"message": "msg"})
    if resp.status_code == 200:
        assert resp.json() == {"diff": "diff"}
    else:
        assert resp.status_code == 422
