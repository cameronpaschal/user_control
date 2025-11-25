

from backend.infrastructure.db import AsyncDatabase
import datetime

class EmailTokenRepository:
    
    def __init__(self, db: AsyncDatabase):
        self._db = db
        
    
    async def store_email_token(self, user_id: int, token: str, expires_at: datetime, created_at: datetime) -> None:
        
        
        query = """
        INSERT INTO email_verification_tokens (user_id, email_token_hash, expires_at, created_at)
        VALUES ($1, $2, $3, $4)
        RETURNING id;
        """
        
        params = (
			user_id,
			token,
			expires_at,
			created_at
		)
        
        return await self._db.fetch_val(query, params=params)
    
    async def mark_email_token_verified(self, token_id: int) -> None:
        used_at = datetime.datetime.now(datetime.timezone.utc)
        query = """
        UPDATE email_verification_tokens
        SET used_at = $1
        WHERE id = $2;
        """
        
        params = [used_at, token_id]
        
        return await self._db.execute(query, params=params)
    
    async def find_by_token_id(self, token_id: int) -> dict:
        
        query = """
        SELECT user_id, email_token_hash, expires_at, used_at
        FROM email_verification_tokens
        WHERE id = $1;
        """
        
        params = [token_id]
        
        return await self._db.fetch_one(query, params=params)
    
    async def find_by_user_id(self, user_id: int) -> dict:
        
        query = """
        SELECT id, email_token_hash, expires_at, used_at
        FROM email_verification_tokens
        WHERE user_id = $1 AND used_at IS null;
        """
        
        params = [user_id]
        
        return await self._db.fetch_all(query, params=params)