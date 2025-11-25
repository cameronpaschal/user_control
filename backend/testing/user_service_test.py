



from backend.services.user_service import UserService
from backend.infrastructure.config import Config
from backend.infrastructure.db import AsyncDatabase
from typing import Optional, List
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


async def test_delete_user(id_deleter: int, id_deletee: int) -> str:
    db = build_db()
    
    await db.init_pool()
    us = UserService(db)
    msg = await us.delete_user_by_id(4, 2)

    await db.close_pool()
    
    print(msg)
    return

async def test_update_profile(id: int, new_display_name: Optional[str] = None, new_bio: Optional[str] = None, new_job_title: Optional[str] = None) -> str:
    db = build_db()
    
    await db.init_pool()
    us = UserService(db)
    msg = await us.update_profile(id, new_display_name=new_display_name, new_bio=new_bio, new_job_title=new_job_title)

    await db.close_pool()
    
    print(msg)
    return
    
    
async def test_get_user_by_id(id: int) -> dict:
    db = build_db()
    
    await db.init_pool()
    us = UserService(db)
    msg = await us.get_user_by_id(id)

    await db.close_pool()
    
    print(msg)
    return
    
async def test_get_all_users() -> dict:
    db = build_db()
    
    await db.init_pool()
    us = UserService(db)
    msg = await us.get_all_users()

    await db.close_pool()
    
    print(msg)
    return



# asyncio.run(test_create_user("largepoppa", "largepoppa@gmail.com", "johhny", "CFO", "IlovePI47$", "this is my second account"))

#Previous user created
#u: bigpoppa23
#p: H@ppyFeet22


# asyncio.run(test_update_email(4, "bigpoppa2@gmail.com"))
# asyncio.run(test_update_password(4, "H@ppyFeet22"))

asyncio.run(test_get_all_users())
# asyncio.run(test_get_user_by_id(4))
# asyncio.run(test_update_profile(3, "jimmy", "this is my third account", "New User"))
# asyncio.run(test_delete_user(4,2))