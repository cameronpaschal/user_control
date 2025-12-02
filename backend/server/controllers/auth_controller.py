from backend.services.auth_service import AuthService
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from backend.dependencies.dependencies import get_auth_service
from backend.infrastructure.errors import IncorrectPasswordError, InvalidTokenError
from pydantic import BaseModel


router = APIRouter(
	prefix="/auth",
    tags=["auth"],
)

class Login(BaseModel):
    username: str
    password: str


@router.post("/login", status_code=200)
async def auth_login(payload: Login,
                     response: Response,
                     auth_service: AuthService = Depends(get_auth_service)):
    try:
        jwt, refresh = await auth_service.authenticate(payload.username, payload.password)
        response.set_cookie(
			key="refresh_token",
			value=refresh,            
			httponly=True,            
			secure=False, # Set true for Https only
			samesite="strict",        
			max_age=60*60*24*14,      
			path="/auth/refresh",     
		)
        
        return {"status": "user authenticated!", 
                "access_token": jwt}
    except IncorrectPasswordError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.post("/refresh", status_code=200)
async def auth_refresh(request: Request,
                       response: Response, 
                       auth_service: AuthService = Depends(get_auth_service)):
    raw_cookie = request.cookies.get("refresh_token")
    
    if not raw_cookie:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    try:
        user_id, refresh_token = raw_cookie.split(".",1)
    except ValueError:
        raise HTTPException(status_code=400, detail="Malformed refresh token")

    
    
    try:
        new_jwt, new_refresh = await auth_service.refresh_jwt(int(user_id), refresh_token)
        response.set_cookie(
			key="refresh_token",
			value=new_refresh,           
			httponly=True,            
			secure=False, # Set true for Https only
			samesite="strict",        
			max_age=60*60*24*14,      
			path="/auth/refresh",     
		)
        
        return {"status": "refresh token issued!", 
                "access_token": new_jwt}
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))
        
