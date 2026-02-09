---
name: auth-skill
description: Handle secure user authentication including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Auth Skill

## Instructions

1. **User Signup**
   - Validate email and password  
   - Hash passwords securely before storing  
   - Register user with Better Auth  
   - Store Better Auth user ID in database  

2. **User Signin**
   - Verify credentials via Better Auth  
   - Create authenticated session  
   - Issue JWT token  

3. **Password Security**
   - Use bcrypt or argon2 for hashing  
   - Never store plain-text passwords  
   - Use secure comparison for verification  

4. **JWT Tokens**
   - Generate JWT after successful login  
   - Include user_id and email in payload  
   - Sign with shared secret  
   - Set token expiration  

5. **Token Validation**
   - Read JWT from `Authorization: Bearer <token>`  
   - Verify signature and expiry  
   - Extract user identity  
   - Reject invalid tokens  

6. **Better Auth Integration**
   - Use Better Auth as the identity provider  
   - Sync Better Auth users with backend database  
   - Use Better Auth session to generate JWT  

## Best Practices
- Always validate inputs before processing  
- Use HTTPS for all auth requests  
- Never trust client-provided user IDs  
- Protect all private APIs with JWT  
- Rotate secrets regularly  

## Example Flow

```text
Signup → Better Auth → Password Hashed → User Stored  
Signin → Better Auth → JWT Issued  
Frontend → Sends JWT → Backend → Validates → Authorizes User  
