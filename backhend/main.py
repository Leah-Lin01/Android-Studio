from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(
    title="HRV Backend API",
    description="接收 Android 心率資料並進行後續 HRV 分析",
    version="1.0.0"
)


# =========================
# Android 傳送資料的格式
# =========================

class HeartRateData(BaseModel):
    device_id: str
    timestamp: int
    heart_rate: List[float]
    rr_intervals: List[float] = []


# =========================
# 測試 Backend
# =========================

@app.get("/")
def root():
    return {
        "status": "OK",
        "message": "HRV Backend is running"
    }


# =========================
# 接收 Android 心率資料
# =========================

@app.post("/heart-rate")
def receive_heart_rate(data: HeartRateData):

    print("\n========== 收到心率資料 ==========")
    print("Device ID:", data.device_id)
    print("Timestamp:", data.timestamp)
    print("Heart Rate:", data.heart_rate)
    print("RR Intervals:", data.rr_intervals)
    print("資料筆數:", len(data.heart_rate))
    print("=================================\n")

    return {
        "status": "success",
        "device_id": data.device_id,
        "received_hr_samples": len(data.heart_rate),
        "received_rr_samples": len(data.rr_intervals),
        "message": "Heart rate data received successfully"
    }
