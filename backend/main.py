
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.server.routes.user_routes import router as user_router
from backend.server.routes.auth_routes import router as auth_router
from backend.infrastructure.db import AsyncDatabase
from backend.infrastructure.config import Config

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = Config.load()
    db = AsyncDatabase(config.db)
    await db.init_pool()
    app.state.db = db
    
    try:
        yield
    finally:
        await app.state.db.close_pool()



app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)


    