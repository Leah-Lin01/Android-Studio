import streamlit as st
import requests
import time
import pandas as pd

st.title("❤️ 區域網路即時心率監測儀")

# 🔗 連接本機 FastAPI 的網址 (因為都在同一台電腦，打 127.0.0.1 即可)
FASTAPI_URL = "http://127.0.0.1:8000"


# 初始化 Streamlit 的歷史紀錄儲存器（避免重刷網頁時不見）
if "hr_history" not in st.session_state:
    st.session_state.hr_history = []

# 建立兩個空畫布，用來填入即時變動的文字與圖表
metric_box = st.empty()
chart_box = st.empty()

print("Streamlit 開始即時監聽 FastAPI...")

# 🔄 無限循環：每秒跟 FastAPI 要一次資料
while True:
    try:
        # 向 FastAPI 發送 GET 請求
        response = requests.get(FASTAPI_URL)
        res_json = response.json()
        
        # 撈出心率數值
        current_bpm = res_json.get("heart_rate", 0)
        
        # 渲染畫面：大字級心率
        with metric_box.container():
            st.metric(label="目前即時心率", value=f"{current_bpm} 次/分")
        
        # 如果手機開始傳大於 0 的數據，就記錄下來畫折線圖
        if current_bpm > 0:
            now_time = time.strftime("%H:%M:%S", time.localtime())
            
            # 避免重複紀錄同一秒的資料
            if not st.session_state.hr_history or st.session_state.hr_history[-1]["時間"] != now_time:
                st.session_state.hr_history.append({"時間": now_time, "心率(BPM)": current_bpm})
                
                # 最多只保留最新 20 筆資料，避免網頁卡頓
                if len(st.session_state.hr_history) > 20:
                    st.session_state.hr_history.pop(0)
            
            # 渲染畫面：即時折線圖
            df = pd.DataFrame(st.session_state.hr_history)
            with chart_box.container():
                st.line_chart(df.set_index("時間")["心率(BPM)"])
                
    except Exception as e:
        st.error(f"連線至 FastAPI 失敗: {e}")
        
    # ⏱️ 每隔 1 秒鐘抓取一次
    time.sleep(1)
