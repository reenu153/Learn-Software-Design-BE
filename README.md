# Software Design Academy — Backend
 
FastAPI backend for **Software Design Academy (SDA)**, an LLM-powered platform for learning software design and UML through automated AI feedback.
 
Built as part of an MSc thesis at TU/e: *"Design and Evaluation of a Web-Based Platform for Learning Software Design using UML with Automated AI Feedback."*
 
## Tech Stack
 
- **Framework:** FastAPI (async)
- **ORM:** SQLAlchemy (async) with Alembic migrations
- **Database:** PostgreSQL
- **AI:**OpenAI API for automated UML feedback generation
- **Deployment:** Render
## Features
 
- REST API for UML diagram exercises (class diagrams, deployment diagrams, etc.)
- Criteria-grounded chain-of-thought prompting for automated feedback on student submissions
- Structured evaluation using `must_have` / `should_not_have` / `common_mistakes` JSON criteria
- User progress tracking logic
## Getting Started
 
### Prerequisites
 
- Python 3.10+
- PostgreSQL
- OPENAI API key
### Installation
 
```bash
git clone https://github.com/<your-username>/learn-software-design-BE.git
cd learn-software-design-BE
 
### Run with Docker
 
```bash
docker compose up --build
```
 
### Environment Variables
 
Create a `.env` file by copying the .env.template file

 
### Database Setup
 
```bash
docker compose exec api alembic revision --autogenerate -m "your message here" 
docker compose exec api alembic upgrade head
```
 
 
API docs available at `http://localhost:8000/docs`.
 
## Project Structure
 
```
alembic               # Migrations
app/
├── main.py           # FastAPI app entrypoint
├── models/           # SQLAlchemy models
├── schemas.py        # Pydantic schemas
├── routers/          # API route handlers
├── services/         # Business logic, AI feedback generation
├── database.py       # Database session/config
└── enums
└── helpers

       
```


The different prompt startegies used to generate design feedback is available at app/prompts

