import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
from pathlib import Path

from trabalho_a4.api_service import ApiService

STATIC_PATH = Path(__file__).parent / "static"

app = FastAPI(
    title="API da Calculadora de Caixa de Gordura",
    description="Uma API para calcular o volume necessário para caixas de gordura.",
    version="1.0.0"
)
api_service = ApiService()

app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    index_html_path = STATIC_PATH / "index.html"
    try:
        with open(index_html_path, encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content=f"<h1>Arquivo index.html não encontrado no caminho: {index_html_path}</h1>", status_code=404)

@app.get("/get_residential_capacity", tags=["Caixa de Gordura"])
def get_residential_capacity(num_sinks: int, num_people: Optional[int] = 0):
    return api_service.calculate_residential(num_sinks, num_people)

@app.get("/get_commercial_capacity", tags=["Caixa de Gordura"])
def get_commercial_capacity(num_meals: int):
    return api_service.calculate_commercial(num_meals)

@app.get("/get_siphon_box_pipes", tags=["Caixa Sinfonada"])
def get_siphon_box_pipes(
    sinks: int = 0,
    showers: int = 0,
    tubs: int = 0,
    laundry: int = 0,
    utility_sinks: int = 0,
    floor_drains: int = 0
    ):
    return api_service.calculate_siphon_pipes(
        sinks,
        showers,
        tubs,
        laundry,
        utility_sinks,
        floor_drains
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

