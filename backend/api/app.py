from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import worker.tasks as tasks
import mysql.connector
from datetime import datetime
import random
import os


mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user="app",
    password="app",
    database="app"
)

mycursor = mydb.cursor()
mycursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    seconds INT NOT NULL DEFAULT 0,
    started_at INT DEFAULT NULL,
    finished_at INT DEFAULT NULL
);
                 """)

app = FastAPI()


class TaskOut(BaseModel):
    id: str
    status: str
    seconds: int
    started_at: int | None
    finished_at: int | None


@app.get("/create")
def create() -> TaskOut:
    seconds = random.randint(1, 10)
    mycursor.execute(
        "INSERT INTO tasks (name, status, seconds) VALUES (%s, %s, %s)", ("Great task", "NEW", seconds))
    mydb.commit()
    return TaskOut(id=str(mycursor.lastrowid), status="NEW", seconds=seconds, started_at=None, finished_at=None)


@app.get("/start")
def start(id: str) -> TaskOut:
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    mycursor.execute(
        "SELECT seconds FROM tasks WHERE id = %s", (id,))
    s = mycursor.fetchone()
    mydb.commit()
    mycursor.execute(
        "UPDATE tasks SET status = %s, started_at = %s WHERE id = %s", ("STARTED", int(ts), id))
    mydb.commit()
    r = tasks.dummy_task.delay(id=id, seconds=s[0])
    return TaskOut(id=id, status="STARTED", seconds=s[0], started_at=0, finished_at=0)


@app.get("/status")
def status(id: str) -> TaskOut:
    mycursor.execute(
        "SELECT status, seconds, started_at, finished_at FROM tasks WHERE id = %s", (id,))
    row = mycursor.fetchone()
    mydb.commit()
    print(row)
    return TaskOut(id=id, status=row[0], seconds=row[1], started_at=row[2], finished_at=row[3])


@app.get("/system")
def system():
    r = tasks.status()
    return r
