from config import FASTAPI_HOST, FASTAPI_LOG_LEVEL, FASTAPI_PORT, FASTAPI_ENV
import utils.logging_settings
from routers.main_router import mainRouter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mainRouter)


if __name__ == "__main__":
    if FASTAPI_ENV == "prod":
        uvicorn.run("api:app", port=FASTAPI_PORT, log_level=FASTAPI_LOG_LEVEL, reload=False, host=FASTAPI_HOST)
    elif FASTAPI_ENV == "dev":
        uvicorn.run("api:app", port=FASTAPI_PORT, log_level=FASTAPI_LOG_LEVEL, reload=True, host=FASTAPI_HOST)
