from backend.services.email_service import EmailService
from backend.infrastructure.config import Config
from backend.infrastructure.db import AsyncDatabase
import asyncio


async def test_generate_email_url(user_id: int, email: str) -> str:
    
    config = Config.load()
    db = AsyncDatabase(config.db)
    
    await db.init_pool()
    email_s = EmailService(db)
    
    url = await email_s.generate_verification_url(user_id, email)

    await db.close_pool()
    
    print(url)
    
    return 

async def test_verify_email_token(token: str) -> bool:
    
    config = Config.load()
    db = AsyncDatabase(config.db)
    
    await db.init_pool()
    email_s = EmailService(db)
    
    url = await email_s.verify_email_token(token)

    await db.close_pool()
    
    print(url)
    
    return 

async def test_resend_email_url(user_id: int, email: str) -> str:
    
    config = Config.load()
    db = AsyncDatabase(config.db)
    
    await db.init_pool()
    email_s = EmailService(db)
    
    url = await email_s.resend_verification(user_id, email)

    await db.close_pool()
    
    print(url)
    
    return 

# asyncio.run(test_generate_email_url(3, "gmail@gmail.com")) 

# asyncio.run(test_verify_email_token("1.eXqEMlEViNmK59Gn-JatORcrEdHzbkTOzqAS9QN3d30"))

asyncio.run(test_resend_email_url(3, "gmail@gmail.com")) 

# "1.eXqEMlEViNmK59Gn-JatORcrEdHzbkTOzqAS9QN3d30"