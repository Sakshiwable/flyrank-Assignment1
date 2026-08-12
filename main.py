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

    new_id = max([task["id"] for task in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": title,
        "done": False
    }

    tasks.append(new_task)

    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updates: dict):
    # Find the task
    for task in tasks:
        if task["id"] == task_id:

            # Body must not be empty
            if not updates:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Request body cannot be empty"}
                )

            # Validate title if provided
            if "title" in updates:
                if not isinstance(updates["title"], str) or not updates["title"].strip():
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title cannot be empty"}
                    )
                task["title"] = updates["title"].strip()

            # Validate done if provided
            if "done" in updates:
                if not isinstance(updates["done"], bool):
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Done must be true or false"}
                    )
                task["done"] = updates["done"]

            # At least title or done should be provided
            if "title" not in updates and "done" not in updates:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Provide title or done"}
                )

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )