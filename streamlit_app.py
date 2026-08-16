import streamlit as st
import requests
import time
import pandas as pd

st.title("❤️ 區域網路即時心率監測儀")

# 🔗 確保精準對準 FastAPI 的 /heart_rate
FASTAPI_URL = "http://192.168.0.46:8000/heart_rate"

# 🔄 核心修正：使用 Streamlit 官方計時器，每 1000 毫秒 (1秒) 自動重刷網頁
# 這樣可以完美取代卡死網頁的 while True，讓畫面每秒動態刷新！
st.logo("❤️" if int(time.time()) % 2 == 0 else "🖤") # 小彩蛋：讓愛心閃爍代表有在重新整理
st_fragments = st.empty() 

# 初始化 Streamlit 的歷史紀錄儲存器
if "hr_history" not in st.session_state:
    st.session_state.hr_history = []

# 建立畫布
metric_box = st.empty()
chart_box = st.empty()
error_box = st.empty()

# 📥 向 FastAPI 發送 GET 請求獲取最新心率
try:
    response = requests.get(FASTAPI_URL, timeout=0.8) # 加上 timeout 避免連線卡死
    
    if response.status_code == 200:
        res_json = response.json()
        error_box.empty()  # 連線成功，清空錯誤
        
        # 撈出心率數值
        current_bpm = res_json.get("heart_rate", 0)
        
        # 渲染大字級心率
        with metric_box.container():
            st.metric(label="目前即時心率", value=f"{current_bpm} 次/分")
        
        # 如果手機開始傳大於 0 的數據，就記錄下來畫折線圖
        if current_bpm > 0:
            now_time = time.strftime("%H:%M:%S", time.localtime())
            
            # 避免重複紀錄同一秒的資料
            if not st.session_state.hr_history or st.session_state.hr_history[-1]["時間"] != now_time:
                st.session_state.hr_history.append({"時間": now_time, "心率(BPM)": current_bpm})
                
                # 最多只保留最新 20 筆資料
                if len(st.session_state.hr_history) > 20:
                    st.session_state.hr_history.pop(0)
            
            # 渲染即時折線圖
            df = pd.DataFrame(st.session_state.hr_history)
            with chart_box.container():
                st.line_chart(df.set_index("時間")["心率(BPM)"])
        else:
            with chart_box.container():
                st.info("⏳ 正在等待手機發送心率數據...")
    else:
        with error_box.container():
            st.error(f"FastAPI 回傳錯誤代碼: {response.status_code}")
            
except Exception as e:
    with error_box.container():
        st.error(f"連線至 FastAPI 失敗 (請確認 FastAPI 有開啟): {e}")

# ⏱️ 觸發 Streamlit 原生重新整理（等同於每秒自動幫使用者按 R 鍵）
time.sleep(1)
st.rerun()
