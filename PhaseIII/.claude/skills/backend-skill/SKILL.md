---
name: backend-skill
description: Build backend APIs, handle requests and responses, and connect the application to the database.
---

# Backend Skill

## Instructions

1. **API Routes**
   - Define RESTful endpoints  
   - Use clear URL structures  
   - Support CRUD operations  
   - Follow HTTP method conventions  

2. **Request Handling**
   - Parse and validate incoming data  
   - Handle query params, headers, and body  
   - Return structured JSON responses  

3. **Response Handling**
   - Use proper HTTP status codes  
   - Send success and error messages clearly  
   - Handle edge cases gracefully  

4. **Database Integration**
   - Connect to database using ORM  
   - Perform create, read, update, delete operations  
   - Map models to database tables  

5. **Business Logic Layer**
   - Keep logic separate from routing  
   - Use services to process data  
   - Enforce application rules  

6. **Error Handling**
   - Catch and log backend errors  
   - Return safe error messages  
   - Never expose sensitive data  

## Best Practices
- Keep routes thin and services thick  
- Always validate input before DB operations  
- Use transactions for critical updates  
- Use async operations where possible  
- Keep database queries optimized  

## Example Structure

```text
Request → API Route → Service Layer → Database → Service Layer → API Response
