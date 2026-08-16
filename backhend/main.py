from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 🧠 關鍵：建立一個全域字典，用來暫存最新收到的心率
data_store = {"heart_rate": 0}

# 定義手機傳過來的資料格式
class HeartRateInput(BaseModel):
    heart_rate: int

# 📥 1. 接收 Android 手機訊息的通道 (POST)
@app.post("/heart_rate")
def receive_from_android(data: HeartRateInput):
    global data_store
    data_store["heart_rate"] = data.heart_rate  # 更新暫存的數值
    print(f"【FastAPI 收到手機資料】: {data.heart_rate} BPM")
    return {"status": "success", "msg": "Data received"}

# 📤 2. 提供給 Streamlit 讀取訊息的通道 (GET) ——— 新增這個！
@app.get("/heart_rate")
def send_to_streamlit():
    global data_store
    return data_store  # 把目前的最新心率倒給 Streamlit
