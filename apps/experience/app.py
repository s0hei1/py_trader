from fastapi import FastAPI

from apps.experience.api.api import experience_api

app = FastAPI()

app.include_router(experience_api)
