

from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Env variable '{name}' is required")
    return value


@dataclass
class DatabaseConfig:
    host: str
    port: str
    database: str
    user: str
    password: str
    min_connections: int = 1
    max_connections: int = 10
    
    @classmethod
    def from_env(cls) -> "DatabaseConfig":
        return cls(
            host=os.getenv("DB_HOST", "localhost"),
            port=_require_env("DB_PORT"),
            database=_require_env("DB_NAME"),
            user=_require_env("DB_USER"),
            password=_require_env("DB_PASSWORD"),
            min_connections=int(os.getenv("DB_POOL_MIN", "1")),
            max_connections=int(os.getenv("DB_POOL_MAX", "10")),
        )

@dataclass
class JWTConfig:
    secret_key: str
    access_token_exp_minutes: int
    refresh_token_exp_days: int
    
    @classmethod
    def from_env(cls):
        return cls(
			secret_key=_require_env("SECRET_KEY"),
			access_token_exp_minutes=int(os.getenv("ACCESS_TOKEN_EXP_MINUTES", "15")),
			refresh_token_exp_days=int(os.getenv("REFRESH_TOKEN_EXP_DAYS", "14"))
		)
        
@dataclass
class AppConfig:
    port: int
    log_level: str
    
    @classmethod
    def from_env(cls):
        return cls(
			port=int(os.getenv("POST", "8000")),
			log_level=os.getenv("LOG_LEVEL", "info")
		)


@dataclass
class Config:
    db: DatabaseConfig
    jwt: JWTConfig
    app: AppConfig
    
    @classmethod
    def load(cls):
        return cls(
			db=DatabaseConfig.from_env(),
			jwt=JWTConfig.from_env(),
			app=AppConfig.from_env()
		)
        
