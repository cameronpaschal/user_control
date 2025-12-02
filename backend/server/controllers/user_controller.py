from datetime import datetime
from backend.services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException
from backend.dependencies.dependencies import get_current_user, get_user_service
from backend.infrastructure.errors import UsernameAlreadyExistsError, UserNotFoundError, InvalidEmailError, InvalidPasswordError, InvalidUsernameError, UnauthorizedActionError,MissingArgumentError
from pydantic import BaseModel

    
class NewUser(BaseModel):
    username: str
    email: str
    display_name: str
    job_title: str
    password: str
    bio: str | None = None
    
class UpdateProfile(BaseModel):
    new_display_name: str | None = None
    new_bio: str | None = None
    new_job_title: str | None = None
    
class UpdatePassword(BaseModel):
    new_password: str	
    
class UpdateUsername(BaseModel):
    new_username: str

class UpdateEmail(BaseModel):
    new_email: str

class AuthenticatedUser(BaseModel):
    user_id: int
    username: str
    iat: datetime
    exp: datetime
    job_title: str
 
 
router = APIRouter(
    prefix="/users",
    tags=["users"],
    )

@router.get("/", status_code=200)
async def get_all_users(current_user = Depends(get_current_user), 
                        user_service: UserService = Depends(get_user_service)):
	"""this returns data about all users

	Args:
		None

	Returns:
		List[dict]: [{'user_id': <int>, 
			'username': <string>, 
			'email': <string>, 
			'display_name': <string>, 
			'bio': <string> or None, 
			'job_title': <string>, 
			'created_at': <datetime object>, 
			'updated_at': <datetime object>, 'email_verified_at': <datetime object> or None}]
	"""
	
	return await user_service.get_all_users()


@router.get("/{user_id}", status_code=200)
async def get_user_by_id(user_id: int,
                        current_user = Depends(get_current_user), 
                        user_service: UserService = Depends(get_user_service)):
	"""this returns data about a user

	Args:
		user_id (int): the user id

	Returns:
		dict: {'user_id': <int>, 
			'username': <string>, 
			'email': <string>, 
			'display_name': <string>, 
			'bio': <string> or None, 
			'job_title': <string>, 
			'created_at': <datetime object>, 
			'updated_at': <datetime object>, 'email_verified_at': <datetime object> or None}
	"""
	try:
		return await user_service.get_user_by_id(user_id)
	except UserNotFoundError as e:
		raise HTTPException(status_code=404, detail=str(e))


@router.post("/create", status_code=201)
async def create_user(payload: NewUser,
                      current_user = Depends(get_current_user), 
                      user_service: UserService = Depends(get_user_service)
                      ):
    
    try:
        return {"status" : "user created!", 
                "user_id" : await user_service.create_new_user(payload.username, payload.email, payload.display_name, payload.job_title, payload.password, payload.bio)
                }
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidEmailError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except InvalidPasswordError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except InvalidUsernameError as e:
        raise HTTPException(status_code=422, detail=str(e))
  
    
@router.patch("/{user_id}/profile", status_code=200)
async def update_profile(user_id: int, 
                         payload: UpdateProfile, 
                         current_user = Depends(get_current_user), 
                         user_service: UserService = Depends(get_user_service)):
    
    new_display_name = payload.new_display_name
    new_bio = payload.new_bio
    new_job_title = payload.new_job_title
    
    try:
        await user_service.update_profile(user_id, new_display_name, new_bio, new_job_title)
        
        return {"status" : "profile updated!"}
    except MissingArgumentError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@router.patch("/{user_id}/password", status_code=200)
async def update_password(user_id: int,
                         payload: UpdatePassword,
                         current_user = Depends(get_current_user),
                         user_service: UserService = Depends(get_user_service)):
    
    try:
        await user_service.update_password(user_id,payload.new_password)
        return {"status" : "password updated!"}
    except InvalidPasswordError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@router.patch("/{user_id}/username", status_code=200)
async def update_username(user_id:int,
                          payload: UpdateUsername,
                          current_user = Depends(get_current_user),
                          user_service: UserService = Depends(get_user_service)):
    
    try:
        await user_service.update_username(user_id, payload.new_username)
        return {"status" : "username updated!"}
    except InvalidUsernameError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@router.patch("/{user_id}/email", status_code=200)
async def update_email(user_id: int,
                       payload: UpdateEmail,
                       current_user = Depends(get_current_user),
                       user_service: UserService = Depends(get_user_service)):
    
    try:
        await user_service.update_email(user_id, payload.new_email)
        return {"status" : "email updated!"}
    except InvalidEmailError as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@router.delete("/{user_id_to_be_deleted}", status_code=200)
async def delete_user(user_id_to_be_deleted: int,
                      current_user = Depends(get_current_user),
                      user_service: UserService = Depends(get_user_service)):
    
    try:
        await user_service.delete_user_by_id(int(current_user["user_id"]), user_id_to_be_deleted)
        return {"status" : f"user with id: {user_id_to_be_deleted} has been deleted!"}
    except UnauthorizedActionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
