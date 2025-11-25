

	# •	Responsibilities:
	# •	authenticate(username, password):
	# •	Fetch user by username using userRepository.
	# •	Verify password against hashed password (via security utilities).
	# •	If valid:
	# •	Generate access token (e.g. JWT with user id, role, expiry).
	# •	Optionally generate refresh token.
	# •	Return token(s) and user info.
	# •	(Optional) logout, refreshToken, etc.
 
 
from refresh_token_repository import RefreshTokenRepository
from backend.repositories.user_repository import UserRepository
from backend.infrastructure.security import Passwords, Tokens
import datetime
 
class AuthService:
    
    def __init__(self, db):
        self._tr = RefreshTokenRepository(db)
        self._ur = UserRepository(db)
        self._sec = Passwords()
        self._tok = Tokens()
    
    async def authenticate(self, username: str, password: str) -> tuple[str,str]:
        """
        Checks username and password 
        """
        
        u = await self._ur.find_by_username(username)
        stored_pw_hash = u["pw_hash"]
        
        
        if await self._sec.verify_pw(password, stored_pw_hash):
            return await self._new_tokens(u["user_id"], u["username"], u["job_title"])
        
        else: 
            raise ValueError("Invalid password")
        
    async def refresh_jwt(self, user_id: int, refresh_token: str) -> tuple[str, str]:
        
        srt = await self._tr.find_by_user_id(user_id) #system refresh token object (token, expires, revoked)
        sys_revoked = srt["revoked"]
  
        if sys_revoked:
            return ValueError("Revoked refresh token")
        
        sys_expires = srt["expires"]
        
        if sys_expires < datetime.datetime.now(datetime.timezone.utc):
            return ValueError("Expired Token")
        
        sys_r_token = srt["refresh_token"]
        
        
        if await self._sec.verify_pw(refresh_token, sys_r_token):
            await self._tr.revoke_refresh_token(sys_r_token) #revoke the old refresh token
            
            user = await self._ur.find_by_id(user_id)
            username = user["username"]
            job_title = user["job_title"]
            
            
            return await self._new_tokens(user_id, username, job_title)
        
        else:
            return ValueError("Refresh token doesn't match")
    
    async def verify_jwt(self, jwt: str) -> dict:
        payload = await self._tok.verify_jwt(jwt)
        
        if payload.get("error_msg") != None:
            return ValueError(payload["error_msg"])
        else:
            return payload
    
    async def _new_tokens(self, user_id:str , username: str, job_title:str) -> tuple[str, str]:
        
        jwt = await self._tok.generate_jwt(user_id, username, job_title)
        
        refresh = await self._tok.generate_random_token()
        expiry_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=14)
        refresh_hashed = await self._sec.hash_pw(refresh)
        await self._tr.store_refresh_token(user_id, refresh_hashed, expiry_date)
        
        return jwt, refresh