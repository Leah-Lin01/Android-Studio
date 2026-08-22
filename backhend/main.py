from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. 🔴 關鍵對齊點：這裡規定手機傳過來的欄位名字叫做 heart_rate
class HeartRateData(BaseModel):
    heart_rate: int

# 2. 建立一個全域變數，用來在記憶體中暫存最新的心率數值
latest_data = {"heart_rate": 0}

# 3. 接收手機傳來資料的通道
@app.post("/heart_rate")
async def receive_heart_rate(data: HeartRateData):
    global latest_data
    # 接收手機傳來的心率，並存進記憶體
    latest_data["heart_rate"] = data.heart_rate
    print(f"📥 成功收到手機心率: {data.heart_rate} BPM")
    return {"status": "success"}

# 4. 讓 Streamlit 網頁來拿資料的通道
@app.get("/get_data")
async def get_data():
    return latest_data
