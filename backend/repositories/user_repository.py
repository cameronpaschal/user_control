	# •	Responsibilities:
	# •	Interact directly with PostgreSQL queries (or ORM).
	# •	Methods like:
	# •	findById(id)
	# •	findByUsername(username)
	# •	findAll()
	# •	create(userRecord)
	# •	update(id, updatedFields)
	# •	delete(id)
	# •	Return plain data objects.
 
 
from backend.infrastructure.db import AsyncDatabase
import datetime
from asyncpg import UniqueViolationError
from typing import Optional, List



class UserRepository:
    
    def __init__(self, db: AsyncDatabase):
        self._db = db
    
    

    async def find_by_id(self, user_id: int) -> Optional[dict]:
        
        
        query = """
        SELECT user_id, username, email, display_name, bio, job_title, created_at, updated_at, email_verified_at
        FROM users
        WHERE user_id = $1
        LIMIT 1;
        """
        
        params = [user_id]
        return await self._db.fetch_one(query, params=params)
    
    
    async def find_by_username(self, username: str) -> Optional[dict]:
        """used exclusively for passwords"""
        
        query = """
        SELECT *
        FROM users
        WHERE username = $1
        LIMIT 1;
        """
        params = [username]
        return await self._db.fetch_one(query, params=params)
    
    async def find_by_email(self, email: str) -> Optional[dict]:
        
        query = """
        SELECT user_id, username, email, display_name, bio, job_title, created_at, updated_at, email_verified_at
        FROM users
        WHERE email = $1
        LIMIT 1;
        """
        params = [email]
        return await self._db.fetch_one(query, params=params)
    
    async def find_all(self) -> list[dict]:
        
        query = """
        SELECT user_id, username, email, display_name, bio, job_title, created_at, updated_at, email_verified_at 
        FROM users;
        """
        return await self._db.fetch_all(query)
    
    
    async def create_user(self, username: str, email: str, display_name: str, job_title: str, pw_hash: str, bio: str = None) -> Optional[int]:
        
        created_at = datetime.datetime.now(datetime.timezone.utc)
        
        query = """
        INSERT INTO users (username, email, display_name, bio, job_title, pw_hash, created_at, updated_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING user_id;
        """
        params = (
			username,
			email,
			display_name,
   			bio,
			job_title,
			pw_hash,
			created_at,
   			created_at
		)
        try:
            user_id = await self._db.fetch_val(query, params=params)
            return user_id
        except UniqueViolationError as e:
            raise ValueError("Username or email already exists") from e
     	
    
    async def update_user(self, id: int, new_username: Optional[str] = None, new_email: Optional[str] = None, new_display_name: Optional[str] = None, new_bio: Optional[str] = None, new_job_title: Optional[str] = None, new_pw_hash: Optional[str] = None, email_verified_at: datetime = None) -> str:
        updates = []
        params: List[str] = []
        
        if new_username:
            updates.append(f"username = ${len(updates) + 1}")
            params.append(new_username)
            
        if new_email:
            updates.append(f"email = ${len(updates) + 1}, email_verified_at = null")
            # updates.append("email_verified_at = null")
            params.append(new_email)
            
        if new_display_name:
            updates.append(f"display_name = ${len(updates) + 1}")
            params.append(new_display_name)
            
        if new_bio:
            updates.append(f"bio = ${len(updates) + 1}")
            params.append(new_bio)
        
        if new_job_title:
            updates.append(f"job_title = ${len(updates) + 1}")
            params.append(new_job_title)
        
        if new_pw_hash:
            updates.append(f"pw_hash = ${len(updates) + 1}")
            params.append(new_pw_hash)
            
        if not updates:
            raise ValueError("no updates requested")
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(id)
        
        query = f"""
        UPDATE users
        SET {','.join(updates)}
        WHERE user_id = ${len(updates)};
        """   
        return await self._db.execute(query, params=params)
    
    async def delete_user(self, id: int) -> str:
        query = """
        DELETE FROM users 
        WHERE user_id = $1;
        """
        return await self._db.execute(query, params=[id])
        
        

	
    