	# •	Responsibilities:
	# •	Password hashing:
	# •	Functions to hash a plaintext password and verify it.
	# •	Token utilities:
	# •	Generate JWT (or other token type).
	# •	Verify and decode tokens.
	# •	Possibly random ID / token generation.
 
from passlib.hash import argon2
import jwt
import datetime
import os
import secrets
import asyncio
from backend.infrastructure.config import Config


config = Config.load()

_SECRET = config.jwt.secret_key
if not _SECRET:
    raise RuntimeError("JWT_SECRET environment variable not set")

_ACCESS_TOKEN_EXP_MINUTES = config.jwt.access_token_exp_minutes

class Passwords:
    
    @staticmethod
    async def hash_pw(password: str) -> str:
        return await asyncio.to_thread(argon2.hash,password)
    
    @staticmethod
    async def verify_pw(password: str, hash: str) -> bool:
        return await asyncio.to_thread(argon2.verify, password, hash)
    
class Tokens:
    @staticmethod
    async def generate_jwt(user_id: int, username: str, job_title: str) -> str:
        now = datetime.datetime.now(datetime.timezone.utc)
        payload = {
			"user_id" : user_id,
			"username" : username,
			"iat" : now,
			"exp" : now + datetime.timedelta(minutes=_ACCESS_TOKEN_EXP_MINUTES),
			"job_title" : job_title
		}
        
        return await asyncio.to_thread(jwt.encode, payload, _SECRET, algorithm="HS256")
    
    @staticmethod
    async def verify_jwt(token: str) -> dict:
        try:
            payload = await asyncio.to_thread(jwt.decode, token, _SECRET, algorithms="HS256")
            
            return payload
        except jwt.ExpiredSignatureError:
            return {"error_msg": "Expired Signature"}
        except jwt.InvalidTokenError:
            return {"error_msg" : "Invalid Token"}
    
    @staticmethod    
    async def generate_random_token(length: int=32) -> str:
        return secrets.token_urlsafe(length)