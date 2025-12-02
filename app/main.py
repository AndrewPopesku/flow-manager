from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Flow Manager", description="A microservice to manage and execute task flows."
)

app.include_router(router)
