from fastapi.responses import HTMLResponse

__all__ = ("template",)

def template(name: str) -> HTMLResponse:
    """Return an HTML template."""
    with open(f'./templates/{name}') as f:
        return HTMLResponse(f.read())

