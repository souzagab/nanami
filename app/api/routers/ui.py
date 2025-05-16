from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["UI"], include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
  """
  Serves the main index page / homepage.
  """

  templates = request.app.state.templates
  return templates.TemplateResponse("pages/index.html", {"request": request, "page_title": "Nanami"})
