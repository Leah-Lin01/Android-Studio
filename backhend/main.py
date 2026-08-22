from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 定義接收手機傳過來的原始數據格式
class SignalData(BaseModel):
    ecg: float
    ppg: float

# 全域變數，用來暫存最新的數據，讓 Streamlit 來拿
latest_data = {"ecg": 0.0, "ppg": 0.0, "heart_rate": 0}

@app.post("/heart_rate")
async def receive_data(data: SignalData):
    global latest_data
    
    # 這裡可以寫你原本計算心率的演算法，或者先單純存起來
    # 範例：簡單模擬一個心率，或者留給 Streamlit 處理
    simulated_hr = 75 
    
    latest_data = {
        "ecg": data.ecg,
        "ppg": data.ppg,
        "heart_rate": simulated_hr
    }
    return {"status": "success"}

@app.get("/get_data")
async def get_data():
    # 提供給 Streamlit 網頁讀取數據的窗口
    return latest_data
