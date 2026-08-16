import streamlit as st
import requests
import time
import pandas as pd

st.title("❤️ 即時心率監測儀表板")

# 這裡因為都在你電腦本地執行，網址打 localhost 或 127.0.0.1 即可！
FASTAPI_GET_URL = "http://127.0.0"

# 初始化 Streamlit 的歷史紀錄儲存器
if "history" not in st.session_state:
    st.session_state.history = []

# 建立即時更新的畫面區塊
metric_slot = st.empty()
chart_slot = st.empty()

while True:
    try:
        # 向 FastAPI 要最新的心率資料
        response = requests.get(FASTAPI_GET_URL)
        data = response.json()
        
        bpm = data.get("heart_rate", 0)
        
        # 顯示在網頁上
        with metric_slot.container():
            st.metric(label="目前心率 (BPM)", value=f"{bpm} 次/分")
        
        # 紀錄歷史資料畫圖（只在心率大於 0 時紀錄）
        if bpm > 0:
            current_time = time.strftime("%H:%M:%S", time.localtime())
            # 避免同一秒重複塞資料
            if not st.session_state.history or st.session_state.history[-1]["time"] != current_time:
                st.session_state.history.append({"time": current_time, "bpm": bpm})
                if len(st.session_state.history) > 20: # 最多保留 20 筆
                    st.session_state.history.pop(0)
            
            df = pd.DataFrame(st.session_state.history)
            with chart_slot.container():
                st.line_chart(df.set_index("time")["bpm"])
                
    except Exception as e:
        st.error(f"無法從 FastAPI 讀取資料: {e}")
        
    time.sleep(1) # 每秒重刷一次
