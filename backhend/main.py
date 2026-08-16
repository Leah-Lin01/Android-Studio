from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware  # 🔄 新增：允許跨來源連線

app = FastAPI()

# 🌐 修正 1：允許所有來源連接（防範 Streamlit 的跨埠/來源封鎖）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許任何網頁連進來抓資料
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 全域字典，用來暫存最新收到的心率
data_store = {"heart_rate": 0}

# 定義手機傳過來的資料格式
class HeartRateInput(BaseModel):
    heart_rate: int

# 🛡️ 修正 2：幫大門口補上通道！消滅一直在 CMD 狂跳的 404 Not Found 錯誤
@app.get("/")
def home_gate():
    return {
        "status": "alive", 
        "msg": "你成功連到 FastAPI 的大門口了！即時心率請改走 /heart_rate 通道喔！"
    }

# 📥 1. 接收 Android 手機訊息的通道 (POST)
@app.post("/heart_rate")
def receive_from_android(data: HeartRateInput):
    global data_store
    data_store["heart_rate"] = data.heart_rate  # 更新暫存的數值
    print(f"【FastAPI 收到手機資料】: {data.heart_rate} BPM")
    return {"status": "success", "msg": "Data received"}

# 📤 2. 提供給 Streamlit 讀取訊息的通道 (GET)
@app.get("/heart_rate")
def send_to_streamlit():
    global data_store
    return data_store  # 把目前的最新心率倒給 Streamlit
