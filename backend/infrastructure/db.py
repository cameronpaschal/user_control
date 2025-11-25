# Instructions for use: 
# db_config = DatabaseConfig.from_env()
# async_db = AsyncDatabase(db_config)

# In FastAPI startup event: await async_db.init_pool()
# In FastAPI shutdown event: await async_db.close_pool()

from dataclasses import dataclass
import os
import asyncpg
from backend.infrastructure.config import DatabaseConfig
from typing import Any, Iterable, List, Optional

class AsyncDatabase:
    """
    Responsible for:
    - Creating and managing an async connection pool
    - Providing async helpers to run queries / commands
    - Providing an async transaction context manager
    """
     
    def __init__(self, config: DatabaseConfig) -> None:
         self._config = config
         self._pool: Optional[asyncpg.pool.Pool] = None
         
    async def init_pool(self) -> None:
        """
        Call this once at app startup to initialize the pool.
        """
        if self._pool is not None:
            return
        
        self._pool = await asyncpg.create_pool(
			min_size=self._config.min_connections,
			max_size=self._config.max_connections,
			host=self._config.host,
			port=self._config.port,
   			database=self._config.database,
   			user=self._config.user,
   			password=self._config.password	
		)
        
    async def close_pool(self) -> None:
        """
        Close all connections in the pool (ex shutdown)
        """
        
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
    
    def _ensure_pool(self) -> asyncpg.pool.Pool:
        if self._pool is None:
            raise RuntimeError("Database pool is not initialized, Call init_pool() first.")
        return self._pool
    
    #Query helpers
    
    async def fetch_all(self, sql: str, params: Optional[Iterable[Any]] = None) -> List[dict]:
        """
		Run a SELECT query and return all rows as a list of dicts.
		"""
        pool = self._ensure_pool()
        async with pool.acquire() as conn:
            rows = await conn.fetch(sql, *(params or []))
            return [dict(row) for row in rows]
        
    async def fetch_one(self, sql:str, params: Optional[Iterable[Any]] = None) -> Optional[dict]:
        """
		Run a SELECT query and return one row as a dict
		"""
        
        pool = self._ensure_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(sql, *(params or []))
            return dict(row) if row is not None else None
        
    async def execute(self, sql: str, params: Optional[Iterable[Any]] = None) -> str:
        """
		Run an INSERT / UPDATE / DELETE without returning rows.
		Returns the command tag (e.g. "INSERT 0 1").
		""" 
        pool = self._ensure_pool()
        async with pool.acquire() as conn:
            result = await conn.execute(sql, *(params or []))
            return result
        
    async def fetch_val(self, sql: str, params: Optional[Iterable[Any]] = None) -> Any:
        """
		Run an INSERT / UPDATE / DELETE without returning rows.
		Returns the a raw python value ex -> 23(token_id), hugepoppa(username)
		""" 
        pool = self._ensure_pool()
        async with pool.acquire() as conn:
            return await conn.fetchval(sql, *(params or []))
        
    def transaction(self):
        """
		Async context manager for multi-step transactions.

		Usage (in a repository):

			async with db.transaction() as conn:
				await conn.execute(...)
				await conn.execute(...)
			# commit happens automatically if no exception
		"""
        return _AsyncTransactionContext(self)

class _AsyncTransactionContext:
    
    """
    Internal async context manager to handle BEGIN / COMMIT / ROLLBACK
    on a single async connection.
    """
    
    def __init__(self, db: AsyncDatabase) -> None:
        self._db = db
        self._conn: Optional[asyncpg.Connection] = None
        self._tx = None
        
        
    async def __aenter__(self) -> asyncpg.Connection:
        pool = self._db._ensure_pool()
        self._conn = await pool.acquire()
        self._tx = self._conn.transaction()
        await self._tx.start()
        return self._conn
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                await self._tx.commit()
            else: 
                await self._tx.rollback()
        finally:
            pool = self._db._ensure_pool()
            await pool.release(self._conn)
            self._conn = None
            self._tx = None





		