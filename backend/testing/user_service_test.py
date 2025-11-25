



from backend.services.user_service import UserService
from backend.infrastructure.config import Config
from backend.infrastructure.db import AsyncDatabase
import asyncio


async def test_create_user(username: str, email: str, display_name: str, job_title: str, password: str, bio: str = None) -> str:
    
    config = Config.load()
    db = AsyncDatabase(config.db)
    
    await db.init_pool()
    us = UserService(db)
    msg = await us.create_user(username, email, display_name, job_title, password, bio)
    await db.close_pool()
    print(msg)
    return 



asyncio.run(test_create_user("bigpoppa23", "email@email.com", "the real mc", "CEO", "ILOVEPI44", "this is my first account"))