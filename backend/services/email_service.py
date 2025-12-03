

from backend.repositories.user_repository import UserRepository
from backend.repositories.email_token_repository import EmailTokenRepository
from backend.infrastructure.security import Passwords, Tokens
from backend.infrastructure.db import AsyncDatabase
from backend.infrastructure.errors import InvalidTokenError, UserNotFoundError
import datetime

class EmailService:

    def __init__(self, db: AsyncDatabase):
        self._pw = Passwords()
        self._tk = Tokens()
        self._er = EmailTokenRepository(db)
        self._ur = UserRepository(db)
        
        
    async def generate_verification_url(self, user_id: int, email: str) -> str:
        
        verification_string = await self._tk.generate_random_token()
        
        vs_hashed = await self._pw.hash_pw(verification_string)
        created_at = datetime.datetime.now(datetime.timezone.utc)
        
        token_id = await self._er.store_email_token(user_id, vs_hashed, (created_at + datetime.timedelta(hours=24)), created_at)
        
        #send_email(email, url) (Create this functionality)
        url = f"https://mywebsite.com/verify-email?token={token_id}.{verification_string}"
        return url
    
    
    async def verify_email_token(self, token: str) -> None:
        
        token_id, raw_token = token.split(".")
        token_id = int(token_id)
        
        payload = await self._er.find_by_token_id(token_id)
        
        if not payload or payload is None:
            raise InvalidTokenError("Token not found")
        
        user_id = payload.get("user_id")
        stored_token = payload.get("email_token_hash")
        expires_at = payload.get("expires_at")
        used_at = payload.get("used_at")
        
        
        current_time = datetime.datetime.now(datetime.timezone.utc)
        
        if not await self._pw.verify_pw(raw_token, stored_token):
            raise InvalidTokenError("Invalid token, token doesn't match")
        
        if expires_at < current_time:
            raise InvalidTokenError("Expired token")
        
        if used_at:
            raise InvalidTokenError("Token has already been used")
        
        if not await self._er.mark_email_token_verified(token_id):
            raise InvalidTokenError("Token Not Found")
        
        if not await self._ur.update_user(user_id, email_verified_at=current_time):
            raise UserNotFoundError("User not found")
    
    
    async def resend_verification(self, user_id: str, email: str) -> str:
        user_tokens = await self._er.find_by_user_id(user_id)
        if user_tokens:
            for d in user_tokens:
                await self._er.mark_email_token_verified(d.get("id"))
                
        return await self.generate_verification_url(user_id, email)
                
        