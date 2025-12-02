	# •	Responsibilities:
	# •	Define reusable error classes:
	# •	AuthenticationError
	# •	AuthorizationError
	# •	ValidationError
	# •	NotFoundError
	# •	DatabaseError
	# •	Makes it easy for errorMiddleware to map them to HTTP status codes.
 
class ServiceError(Exception):
    """Base exception for service errors."""
    
class AuthenticationError(ServiceError):
    """Authentication Failure"""
    
class UserNotFoundError(Exception):
    """Could not find user error"""

class InvalidEmailError(Exception):
    """Invalid format or email"""
    
class InvalidPasswordError(Exception):
    """Invalid password format"""
    
class UsernameAlreadyExistsError(Exception):
    """Username already exists in the database"""
    
class InvalidUsernameError(Exception):
    """Invalid username format"""
    
class UnauthorizedActionError(Exception):
    """When a user tries to do something they can't"""
    
class MissingArgumentError(Exception):
    """When a method is missing one or more arguments"""

class IncorrectPasswordError(Exception):
    """When a user enters an incorrect password when authenticating"""
    
class InvalidTokenError(Exception):
    """When a user passes an invalid token"""