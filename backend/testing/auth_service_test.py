
from backend.services.auth_service import AuthService
from backend.infrastructure.config import Config
from backend.infrastructure.db import AsyncDatabase
import asyncio


async def test_auth_login(username: str, password: str) -> tuple[str,str]:
    
    config = Config.load()
    db = AsyncDatabase(config.db)
    
    await db.init_pool()
    auth_s = AuthService(db)
    
    
    jwt, refresh = await auth_s.authenticate(username, password)
    
    # jwt, refresh = await auth_s.refresh_jwt(4, "bsDpkLjYjVyUbc9XUGxUIM4X2EVDtc0YMGlr8ylWWg4")
    
    # payload = await auth_s.verify_jwt("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6ImJpZ3BvcHBhMjMiLCJpYXQiOjE3NjM4NTg3MTMsImV4cCI6MTc2Mzg1OTYxMywiam9iX3RpdGxlIjoiQ0VPIn0.4ej4eHE51Wkx2c9sPjJv2Lz__68XVUfrsB-h2rDw-aE")
        
   
    
    
    await db.close_pool()
    print(jwt)
    print(refresh)
    # print(payload)
    return 



asyncio.run(test_auth_login("bigpoppa23", "ILOVEPI4")) #should be ILOVEPI44