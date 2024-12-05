#import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routers.group_router import group_router
from app.routers.quote_router import quote_router
from app.routers.song_router import song_router


app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://192.168.1.2:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(group_router)
app.include_router(song_router)
app.include_router(quote_router)
#uvicorn.run(app=app, host="127.0.0.1", port=8000)