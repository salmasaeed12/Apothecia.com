from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models.models import Users, Business, Products

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to Apothecia"}

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["back_end.models.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)