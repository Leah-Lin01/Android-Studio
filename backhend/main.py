from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Android 傳過來的資料格式
class HeartRateData(BaseModel):
    device_id: str
    timestamp: int
    heart_rate: List[float]


# 測試 Backend 是否正常
@app.get("/")
def root():
    return {
        "status": "OK",
        "message": "HRV Backend is running"
    }


# 接收 Android 心率資料
@app.post("/heart-rate")
def receive_heart_rate(data: HeartRateData):

    print("收到裝置：", data.device_id)
    print("收到時間：", data.timestamp)
    print("收到心率：", data.heart_rate)

    return {
        "status": "success",
        "device_id": data.device_id,
        "received_samples": len(data.heart_rate)
    }