import streamlit as st
import requests
import time

st.title("💖 即時生理訊號監測網頁")

# 建立畫面的外框
ecg_metric = st.empty()
ppg_metric = st.empty()
hr_metric = st.empty()

# 進入無窮迴圈，每 0.1 秒向 FastAPI 抓一次最新數據
while True:
    try:
        # 讀取本機 FastAPI 的暫存資料
        response = requests.get("http://127.0.0.46:8000", timeout=1)
        if response.status_code == 200:
            data = response.json()
            
            # 把數據即時顯示在網頁畫面上！
            hr_metric.metric(label="📊 當前心率 (BPM)", value=f"{data['heart_rate']} 次/分")
            ecg_metric.write(f"📈 ECG 心電訊號數值: {data['ecg']}")
            ppg_metric.write(f"📉 PPG 脈搏波數值: {data['ppg']}")
            
    except Exception as e:
        st.error(f"無法讀取後端數據: {e}")
        
    time.sleep(0.1) # 每 0.1 秒刷新一次網頁數據
