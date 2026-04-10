Backend bug: Allows duplicate email creation instead of raising error 409: Duplicate email returns 500 instead of 409
  The API crashes (500) instead of handling a business rule violation
  The OpenAPI spec expects 409 Conflict for duplicates
  
**Endpoint:** POST /{env}/users  
**Expected:** 409 Conflict when creating a user with an existing email  
**Actual:** 500 Internal Server Error  

**Steps to reproduce:**
1. Create a user with email `duplicate@example.com`
2. Attempt to create the same user again
**Impact:** API crashes instead of enforcing business rules.


Backend bug: Get missing user returns 500 instead of 404: 
  Missing users are not handled gracefully
  API throws an internal error instead of returning Not Found

**Endpoint:** GET /{env}/users/{email}  
**Expected:** 404 Not Found  
**Actual:** 500 Internal Server Error  

**Steps to reproduce:**
1. Request a non-existent user email
**Impact:** Missing resources are not handled gracefully.


Security bug: Missing authentication header for delete operation of user:
  The API allows destructive operations without authentication

**Endpoint:** DELETE /{env}/users/{email}  
**Expected:** 401 Unauthorized when no auth token is provided  
**Actual:** 204 No Content  
**Security Impact:** Allows unauthenticated deletion of user data.


