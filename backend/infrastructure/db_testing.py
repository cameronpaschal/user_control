

from db import AsyncDatabase
from config import Config
import datetime
import asyncio
from typing import Optional, List




async def test():

    config = Config.load()


    datab = AsyncDatabase(config.db)
    
    await datab.init_pool()
    query = """
    SELECT * FROM users
    """
    rows = await datab.fetch_all(query)
    print(rows)

    # user_id = 1
    
    # clause = "user_id = $1"
    # query = f"""
    #     SELECT *
    #     FROM users
    #     WHERE {clause}
    #     LIMIT 1;
    #     """
    
    # params = [user_id]
    # rows2 = await datab.fetch_one(query, params=params)
    
    # print(rows2['pw_hash'])
    
    # data = await create_user(datab, "newuser", "email@gmail.com", "johnathan", "manager", "password1", "new user what's up")
    #data = await update_user(datab, 3, new_username="yippie123")
    data = await delete_user(datab, 1)
    print(data)
    await datab.close_pool()
    
    
async def create_user(db: AsyncDatabase, username: str, email: str, display_name: str, job_title: str, pw_hash: str, bio: str = None) -> str:
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
        msg = await db.execute(query, params=params)
        return msg
    
    
async def update_user(db: AsyncDatabase,id: int, new_username: Optional[str] = None, new_email: Optional[str] = None, new_display_name: Optional[str] = None, new_bio: Optional[str] = None, new_job_title: Optional[str] = None, new_pw_hash: Optional[str] = None) -> None:
    updates = []
    params: List[str] = []
    
    if new_username:
        updates.append(f"username = ${len(updates) + 1}")
        params.append(new_username)
        
    if new_email:
        updates.append(f"email = ${len(updates) + 1}")
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
    return await db.execute(query, params=params)

async def delete_user(db: AsyncDatabase, id: int) -> str:
    query = """
    DELETE FROM users 
    WHERE user_id = $1;
    """
    return await db.execute(query, params=[id])
    
asyncio.run(test())

