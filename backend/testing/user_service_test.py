



from backend.services.user_service import UserService
from backend.infrastructure.config import Config
from backend.infrastructure.db import AsyncDatabase
import asyncio


def build_db():
    config = Config.load()
    db = AsyncDatabase(config.db)
    return db

async def test_create_user(username: str, email: str, display_name: str, job_title: str, password: str, bio: str = None) -> str:

    db = build_db()
    
    await db.init_pool()
    us = UserService(db)
    msg = await us.create_new_user(username, email, display_name, job_title, password, bio)
    await db.close_pool()
    print(msg)
    return 


async def test_update_email(id: int, email: str) -> str:
    db = build_db()
    
    await db.init_pool()
    us = UserService(db)
    msg = await us.update_email(id, email)
    await db.close_pool()
    print(msg)
    return 

async def test_update_password(id: int, new_pw: str) -> str:
    db = build_db()
    
    await db.init_pool()
    us = UserService(db)
    msg = await us.update_password(id, new_pw)

    await db.close_pool()
    
    print(msg)
    return




# asyncio.run(test_create_user("largepoppa", "largepoppa@gmail.com", "johhny", "CFO", "IlovePI47$", "this is my second account"))

#Previous user created
#u: bigpoppa23
#p: H@ppyFeet22


asyncio.run(test_update_email(4, "bigpoppa2@gmail.com"))
# asyncio.run(test_update_password(4, "H@ppyFeet22"))