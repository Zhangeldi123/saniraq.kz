from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, FastAPI, Response, Request
from api.user import user_router
from api.house import house_router

app = FastAPI()
app.include_router(user_router)
app.include_router(house_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}