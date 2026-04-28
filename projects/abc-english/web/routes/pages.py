"""HTML page routes (server-side rendered templates).

These routes render Jinja2 templates that provide the page shell.
All dynamic data is fetched client-side via the JSON API under ``/api/*``.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Templates live at ``web/templates`` (relative to repo root when uvicorn is
# launched from there). We resolve an absolute path so the app works no matter
# where the process is started from.
_TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATE_DIR))

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
async def episodes_page(request: Request) -> HTMLResponse:
    """Landing page — list of episodes."""
    return templates.TemplateResponse(
        request,
        "episodes.html",
        {"active_nav": "episodes"},
    )


@router.get("/study/{episode_id}", response_class=HTMLResponse)
async def study_page(request: Request, episode_id: str) -> HTMLResponse:
    """Study page for a single episode."""
    return templates.TemplateResponse(
        request,
        "study.html",
        {
            "episode_id": episode_id,
            "active_nav": "episodes",
        },
    )


@router.get("/notebook", response_class=HTMLResponse)
async def notebook_page(request: Request) -> HTMLResponse:
    """User vocabulary notebook page."""
    return templates.TemplateResponse(
        request,
        "notebook.html",
        {"active_nav": "notebook"},
    )
