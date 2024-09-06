from celery import Celery
from datetime import datetime
from time import sleep
import os
import mysql.connector

redis_url = os.getenv("REDIS_URL", f"redis://{os.getenv('REDIS_HOST')}:6379")

app = Celery('tasks', broker=redis_url, backend=redis_url)


def status():
    result = []
    active_nodes = app.control.inspect().active()
    for name, value in active_nodes.items():
        is_busy = len(value) > 0
        result.append({"name": name, "busy": is_busy})
    return result


@app.task
def dummy_task(id: str, seconds: int):
    mydb = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user="app",
        password="app",
        database="app"
    )
    mycursor = mydb.cursor()
    sleep(seconds)
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    mycursor.execute(
        "UPDATE tasks SET status = %s, finished_at = %s WHERE id = %s", ("DONE", int(ts), id))
    mydb.commit()
    mycursor.close()
    mydb.close()
    return "Done"
