

	# •	Responsibilities:
	# •	Implement core user-related business rules:
	# •	getAllUsers()
	# •	getUserById(id)
	# •	createUser(userData)
	# •	Validate domain rules (unique username, password requirements).
	# •	Hash password before saving.
	# •	Call userRepository.create.
	# •	updateUser(id, changes)
	# •	Decide which fields are allowed to be updated.
	# •	If password changes, hash it.
	# •	Call userRepository.update.
	# •	deleteUser(id)
	# •	Possibly disallow deleting oneself or enforce rules.
	# •	Notes:
	    # •	Service layer should not know about HTTP. It deals in domain objects / DTOs and throws domain-specific errors (e.g. UserNotFound, ValidationError).
     
from backend.repositories.user_repository import UserRepository
from backend.infrastructure.security import Passwords
     
class UserService:
    
    def __init__(self, db):
        self._ur=UserRepository(db)
        self._pw=Passwords()
    
    async def register_user(self, username: str, email: str, display_name: str, job_title: str, password:str, bio: str = None) -> str:
        email = email.strip().lower()
        username = username.strip().lower()
 
        self._validate_password(password)
        self._validate_username(username)
        
        if await self._ur.find_by_username(username):
            raise ValueError("Username already taken")
        
        if await self._ur.find_by_email(email):
            raise ValueError("Email already taken")
        
        
        pw_hashed = await self._pw.hash_pw(password)
        
        return await self._ur.create_user(username, email, display_name, job_title, pw_hashed, bio)
        
    # async def update_profile
    # async def update_password
    # async def update_username
    # async def update_email
    
    
    
    def _validate_password(self, password: str) -> None:
        errors = []
        if len(password) < 8:			
            errors.append("Password must be at least 8 characters long.")
            
        if not any(c.islower() for c in password):
            errors.append("Password must contain a lowercase letter.")
            
        if not any(c.isupper() for c in password):
            errors.append("Password must contain an uppercase letter.")
            
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain a digit.")
            
        if not any(not c.isalnum() for c in password):
            errors.append("Password must contain a symbol (e.g. !@#$%).")
            
        if errors:		# In your app this might be a custom exception  
            raise ValueError(" ".join(errors))
        
        
    def _validate_username(self, username: str) -> None:
        username = username.strip().lower()
        
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        
        if len(username) > 30:
            raise ValueError("Username cannot be longer than 30 characters")
        
        allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_.")
        if any(c not in allowed for c in username):
            raise ValueError("Username may only contain lowercase letters, digits, \'.\', and \'_\'.")