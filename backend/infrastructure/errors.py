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