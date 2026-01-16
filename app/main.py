from fastapi import FastAPI
from app.api.routes.states_routes import router as states_router
from app.api.routes.ports_routes import router as ports_router
from app.api.routes.tide_routes import router as tide_router

app = FastAPI(title="PortoMaré API")

app.include_router(states_router)
app.include_router(ports_router)
app.include_router(tide_router)
