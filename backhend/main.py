from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

latest_data = {}


class HeartRateData(BaseModel):
    heart_rate: float
    rr_interval: float | None = None


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.get("/get_latest")
def receive_heart_rate(data: HeartRateData):
    global latest_data

    latest_data = {
        "heart_rate": data.heart_rate,
        "rr_interval": data.rr_interval
    }

    print("收到 Android 資料：", latest_data)

    return {
        "status": "success",
        "data": latest_data
    }


@app.get("/get_latest")
def get_heart_rate():
    return latest_data
