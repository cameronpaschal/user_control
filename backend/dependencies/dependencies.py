from fastapi import Depends, HTTPException, Request, status
from backend.services.auth_service import AuthService
from backend.services.user_service import UserService
from backend.infrastructure.db import AsyncDatabase

    

async def get_db(request: Request) -> AsyncDatabase:
    return request.app.state.db

async def get_user_service(db: AsyncDatabase = Depends(get_db)) -> UserService:
    return UserService(db)

async def get_auth_service(db: AsyncDatabase = Depends(get_db)) -> AuthService:
    return AuthService(db)


async def get_current_user(request: Request,
                           auth_service: AuthService = Depends(get_auth_service)) -> dict:
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = auth_header.removeprefix("Bearer ").strip()
    
    payload = await auth_service.verify_jwt(token)
    
    if "error_msg" in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=payload["error_msg"]
        )
        
    return payload
