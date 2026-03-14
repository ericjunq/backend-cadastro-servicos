from fastapi import FastAPI
from task_routers import task_router
from auth_routers import auth_router
from database import engine
from models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(task_router)

@app.get('/')
async def teste():
    return {'testando' : 'funcionou'}