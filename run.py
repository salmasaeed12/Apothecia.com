from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.models import *
from app.routes.auth import *
app = FastAPI()
#signals
from tortoise.signals import post_save
from typing import List, Optional, Type
from tortoise import BaseDBAsyncClient

@post_save(User)
async def create_profile(sender: Type[User], instance: User, using_db: BaseDBAsyncClient, **kwargs):
    await Profile.create(user=instance)
    if created:
        print(f"Profile created for {instance.email}")
        

@app.post("/register")
async def register(user: UserCreate):
    user_info = user.dict(exclude_unset=True)
    user_info["password_hash"] = get_password_hash(user_info["password"])
    user_opject = await User.create(**user_info)
    new_user = await User_Pydantic.from_tortoise_orm(user_opject)
    return{
        "msg": "User created successfully",
        "user": new_user
    
    }

@app.get("/")
def index():
    return {"message": "Welcome to Apothecia"}

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"app": ["app.models.*"]},
    generate_schemas=True,
    add_exception_handlers=True
)

    
if __name__ == "__main__":
    import uvicorn
    #! in the production mode, we need to change the Log level to "info" and reload to False
    uvicorn.run("app:app", host="127.0.0.1", port=5000, log_level="debug", reload=True)