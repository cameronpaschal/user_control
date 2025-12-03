
from backend.infrastructure.db import AsyncDatabase
import datetime

class RefreshTokenRepository:
    
    def __init__(self, db: AsyncDatabase):
        self._db = db
        
    
    async def store_refresh_token(self, user_id: int, token: str, expiry: datetime) -> None:
        
        query = """
        INSERT INTO refresh_tokens (user_id, refresh_token, expires, revoked)
        VALUES ($1, $2, $3, $4)
        RETURNING token_id;
        """
        
        params = (
			user_id,
			token,
			expiry,
			False
		)
        
        return await self._db.fetch_val(query, params=params)
    
    async def revoke_refresh_token(self, token: str) -> None:
        #this could be changed back to revoking the token rather than deleting it, or another method could be created for admin functionality
        query = """
        DELETE FROM refresh_tokens
        WHERE refresh_token = $1;
        """
        
        params = [token]
        
        return await self._db.execute(query, params=params)
    
    async def find_by_token(self, token: str) -> dict:
        
        query = """
        SELECT user_id, expires, revoked
        FROM refresh_tokens
        WHERE refresh_token = $1;
        """
        
        params = [token]
        
        return await self._db.fetch_one(query, params=params)
    
    async def find_by_token_id(self, id: int) -> dict:
        
        query = """
        SELECT user_id, refresh_token, expires, revoked
        FROM refresh_tokens
        WHERE token_id = $1;
        """
        
        params = [id]
        
        return await self._db.fetch_one(query, params=params)
    
    
        
        
        
        
        