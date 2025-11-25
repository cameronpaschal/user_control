

	# •	Extract auth token (from header or cookie).
	# •	Verify token (e.g., JWT signature, expiry).
	# •	Load user identity (user id, roles/permissions).
	# •	Attach user info to request context.
	# •	Reject request if authentication fails.