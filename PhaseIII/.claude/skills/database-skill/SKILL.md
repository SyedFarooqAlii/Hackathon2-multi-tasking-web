---
name: database-skill
description: Design and manage database schemas including tables, migrations, and relational structure for backend systems.
---

# Database Skill

## Instructions

1. **Schema Design**
   - Define tables and columns
   - Choose correct data types
   - Apply primary and foreign keys
   - Enforce relationships and constraints  

2. **Table Creation**
   - Create normalized tables  
   - Add indexes for performance  
   - Define unique and not-null rules  
   - Support multi-user data separation  

3. **Migrations**
   - Generate versioned migration files  
   - Apply and rollback schema changes  
   - Keep schema in sync across environments  

4. **Data Integrity**
   - Enforce referential integrity  
   - Prevent orphaned records  
   - Use transactions for critical writes  

5. **Optimization**
   - Add indexes to frequently queried fields  
   - Avoid redundant data  
   - Design for scalability  

## Best Practices
- Always use migrations, never manual table edits  
- Never store sensitive data in plain text  
- Use UUIDs or indexed IDs  
- Keep schemas simple and well normalized  
- Use soft deletes when needed  
- Backward-compatible migrations only  

## Example Structure

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  title TEXT NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT now()
);
