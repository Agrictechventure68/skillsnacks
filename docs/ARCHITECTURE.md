 SkillSnacks Architecture

## Overview
SkillSnacks is a vocational learning platform with:
- *Frontend*: HTML/CSS/JS (or React for advanced features)
- *Backend*: Flask/Django (Python) or Express (Node.js)
- *Database*: SQLite (MVP), scalable to PostgreSQL/MySQL
- *Static Content Loader*: Automatically imports JSON learning modules from /contents/modules

## System Flow
1. User signs up/logs in
2. Frontend fetches skills via REST API
3. Backend retrieves skills from database or JSON modules
4. User progress is stored in database
5. Admin can add/edit/delete skills through Admin interface

## Key Files
- /docs/API_Docs.md – Backend route documentation
- /backend/module_loader.py – Dynamic JSON module loader
- /frontend/scripts.js – Fetches skills from backend dynamically


