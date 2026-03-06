from fastapi import FastAPI
from auth_routers import router
from database import engine
from models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get('/')
async def teste():
    return {'testando' : 'funcionou'}