

from backend.infrastructure.security import Passwords, Tokens

import asyncio

pw = Passwords()

tok = Tokens()

async def pw_test(password: str):

    password = await pw.hash_pw(password)
    print(password)

    success = await pw.verify_pw("SuperSecurePassword", password)


    print(success)
    
    
    
    
    
async def token_test(user_id: int, username: str, job_title: str) -> None:
    
    token = await tok.generate_jwt(user_id, username, job_title)
    print(token)
    
    token_decoded = await tok.verify_jwt(token)
    print(token_decoded)
    random_token = await tok.generate_random_token()
    
    print(random_token)
        
    
asyncio.run(pw_test(password="SuperSecurePassword"))
asyncio.run(token_test(2,"big_poppa", "CEO"))