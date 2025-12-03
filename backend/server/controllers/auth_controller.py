from backend.services.auth_service import AuthService
from backend.services.email_service import EmailService
from backend.services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from backend.dependencies.dependencies import get_auth_service, get_email_service, get_current_user, get_user_service
from backend.infrastructure.errors import IncorrectPasswordError, InvalidTokenError, UserNotFoundError
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
        
@router.get("/email-verify", status_code=200)
async def verify_email(token: str,
                       email_service: EmailService = Depends(get_email_service)):
    
    try:
        await email_service.verify_email_token(token)
        
        return {"status" : "Email verified!"}
    except InvalidTokenError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=422, detail=str(e))
    

@router.post("/gen-email-verify", status_code=200)
async def generate_verification_email(current_user = Depends(get_current_user),
                                      email_service: EmailService = Depends(get_email_service),
                                      user_service: UserService = Depends(get_user_service)):
    
    try:
        user = await user_service.get_user_by_id(current_user["user_id"])
        user_id = user["user_id"]
        email = user["email"]
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    try:
        url = await email_service.generate_verification_url(user_id, email)
        
        return {"status" : "verificaiton url created!",
                "url" : f"{url}"}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.post("/resend-email-verify", status_code=200)
async def resend_email_verification(current_user = Depends(get_current_user),
                                      email_service: EmailService = Depends(get_email_service),
                                      user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.get_user_by_id(current_user["user_id"])
        user_id = user["user_id"]
        email = user["email"]
        
    except UserNotFoundError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
    try:
        url = await email_service.resend_verification(user_id, email)
        
        return {"status" : "verificaiton url created!",
                "url" : f"{url}"}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))