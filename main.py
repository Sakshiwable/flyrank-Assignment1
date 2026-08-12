from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3

app = FastAPI()

DATABASE = "tasks.db"

def init_db():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor = connection.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        connection.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", 0),
                ("Build CRUD API", 0),
                ("Push project to GitHub", 0)
            ]
        )

    connection.commit()
    connection.close()

init_db()

class TaskCreate(BaseModel):
    title: str


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        "SELECT id, title, done FROM tasks"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return dict(row)


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    title = task.title.strip()

    if not title:
        return JSONResponse(
            status_code=400,
            content={"error": "Title cannot be empty"}
        )

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    cursor = connection.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, 0)
    )

    task_id = cursor.lastrowid
    connection.commit()

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return dict(row)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updates: dict):
    if not updates:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"}
        )

    if "title" in updates:
        if not isinstance(updates["title"], str) or not updates["title"].strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title cannot be empty"}
            )

    if "done" in updates:
        if not isinstance(updates["done"], bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Done must be true or false"}
            )

    if "title" not in updates and "done" not in updates:
        return JSONResponse(
            status_code=400,
            content={"error": "Provide title or done"}
        )

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    if row is None:
        connection.close()
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    if "title" in updates and "done" in updates:
        connection.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (updates["title"].strip(), int(updates["done"]), task_id)
        )

    elif "title" in updates:
        connection.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (updates["title"].strip(), task_id)
        )

    elif "done" in updates:
        connection.execute(
            "UPDATE tasks SET done = ? WHERE id = ?",
            (int(updates["done"]), task_id)
        )

    connection.commit()

    row = connection.execute(
        "SELECT id, title, done FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return dict(row)


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    connection.close()