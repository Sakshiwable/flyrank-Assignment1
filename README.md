# Task API

A simple CRUD REST API built with Python and FastAPI as part of the FlyRank Backend AI Engineering internship.

## Features

- Create tasks
- Read all tasks
- Read a single task
- Update tasks
- Delete tasks
- Input validation
- Swagger UI documentation

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic

## Project Structure

```text
task_api/
├── main.py
├── README.md
├── swagger.png
└── .gitignore

The flyrank_backend virtual environment is used locally and is excluded from GitHub using .gitignore.

Setup
1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL
cd task_api
2. Create a virtual environment
python -m venv flyrank_backend
3. Activate the virtual environment

For Windows PowerShell:

.\flyrank_backend\Scripts\Activate.ps1
4. Install dependencies
pip install fastapi uvicorn
Run the API

Start the server using:

python -m uvicorn main:app --reload

The API will run at:

http://127.0.0.1:8000
Swagger UI

FastAPI provides interactive API documentation through Swagger UI.

Open:

http://127.0.0.1:8000/docs

You can use the Swagger UI to test all CRUD operations.

API Endpoints
Method	Endpoint	Description
GET	/	Returns API information
GET	/health	Checks whether the server is running
GET	/tasks	Returns all tasks
GET	/tasks/{id}	Returns a single task
POST	/tasks	Creates a new task
PUT	/tasks/{id}	Updates an existing task
DELETE	/tasks/{id}	Deletes a task
CRUD Operations
Create

Use:

POST /tasks

Request body:

{
  "title": "Buy milk"
}

Successful response:

201 Created

Example response:

{
  "id": 4,
  "title": "Buy milk",
  "done": false
}
Read

Get all tasks:

GET /tasks

Get one task:

GET /tasks/1

If the task does not exist, the API returns:

404 Not Found
Update

Use:

PUT /tasks/1

Example request:

{
  "title": "Complete FastAPI assignment",
  "done": true
}
Delete

Use:

DELETE /tasks/1

Successful deletion returns:

204 No Content




C:\Users\wable\Desktop\FlyRank\task_api\swagger.png



## SQLite Database

This project uses SQLite for persistent data storage.

SQLite was chosen because it is lightweight, requires no separate database server, and stores the database in a single file.

The database file is:

`tasks.db`

The `tasks` table contains:

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key for each task |
| title | TEXT | Task title |
| done | BOOLEAN | Task completion status |

The database and table are created automatically when the application starts if they do not already exist.

Three example tasks are inserted only when the table is empty.

## Example SQL Query

One SQL query executed during this assignment was:

```sql
SELECT * FROM tasks;


C:\Users\wable\Desktop\FlyRank\task_api\Database.png


