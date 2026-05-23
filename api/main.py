from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routes
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://silver-youtiao-253988.netlify.app/'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)

app.include_router(routes.router)
