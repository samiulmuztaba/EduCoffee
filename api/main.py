from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500', 'https://samiulmuztaba.github.io/'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)

app.include_router(routes.router)