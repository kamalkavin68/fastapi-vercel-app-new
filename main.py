from fastapi import FastAPI
from threading import Thread
import time

app = FastAPI()

count = 0

@app.get("/")
async def root():
    return {"detail": f"Current count is {count}"}

def first_fun():
    while 1:
        time.sleep(3)
        global count
        count += 1
        print(count)

t1 = Thread(target=first_fun)
t1.start()
t1.join()
