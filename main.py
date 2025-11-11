from fastapi import FastAPI

from logic import isEven

app = FastAPI()


@app.get("/isEven/{num}")
async def root(num: int):
    return {"isEven": isEven(num)}
