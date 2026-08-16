import streamlit as st
import requests
import time
import pandas as pd

# 設定網頁標題
st.title("❤️ 即時心率監測儀表板")

# Firebase 的資料網址（結尾一樣要加 .json）
FIREBASE_URL = "http://127.0.0.1:8000/docs"

# 用來放歷史數據的容器
if "history" not in st.session_state:
    st.session_state.history = []

# 建立畫面的區塊
metric_slot = st.empty()
chart_slot = st.empty()

# 無限循環，每秒去抓一次新資料
while True:
    try:
        # 向 Firebase 要資料
        response = requests.get(FIREBASE_URL)
        data = response.json()
        
        if data:
            bpm = data.get("bpm", 0)
            timestamp = data.get("timestamp", 0)
            
            # 顯示目前的大數字心率
            with metric_slot.container():
                st.metric(label="目前心率 (BPM)", value=f"{bpm} 次/分")
            
            # 將歷史資料存起來畫圖
            # 避免重複塞入同一秒的數據
            if not st.session_state.history or st.session_state.history[-1]["time"] != timestamp:
                st.session_state.history.append({"time": timestamp, "bpm": bpm})
                # 只保留最近 20 筆資料
                if len(st.session_state.history) > 20:
                    st.session_state.history.pop(0)
            
            # 繪製即時折線圖
            df = pd.DataFrame(st.session_state.history)
            with chart_slot.container():
                st.line_chart(df.set_index("time")["bpm"])
                
    except Exception as e:
        st.error(f"讀取資料失敗: {e}")
        
    # 每 1 秒刷新一次
    time.sleep(1)
