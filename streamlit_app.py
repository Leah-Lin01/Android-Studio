import streamlit as st

from hrv_analysis import (
    calculate_basic_hrv,
    calculate_frequency_domain
)


st.set_page_config(
    page_title="HRV Analysis",
    page_icon="❤️"
)

st.title("❤️ HRV 心率變異分析系統")

st.write(
    "輸入 RR Interval 資料，進行 HRV 與頻域分析。"
)


# =========================
# 輸入資料
# =========================

rr_text = st.text_area(
    "請輸入 RR Interval（ms），以逗號分隔",
    placeholder="833, 822, 800, 811, 845, 830"
)


if st.button("開始分析", type="primary"):

    try:

        rr_intervals = [
            float(x.strip())
            for x in rr_text.split(",")
            if x.strip()
        ]

        if len(rr_intervals) < 10:
            st.warning(
                "RR Interval 資料太少，至少需要 10 筆以上。"
            )

        else:

            # 基本 HRV
            basic_result = calculate_basic_hrv(
                rr_intervals
            )

            # 頻域分析
            frequency_result = calculate_frequency_domain(
                rr_intervals
            )

            # =========================
            # 顯示結果
            # =========================

            st.subheader("基本 HRV")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "平均心率",
                f"{basic_result['mean_hr']:.1f} BPM"
            )

            col2.metric(
                "SDNN",
                f"{basic_result['sdnn']:.2f} ms"
            )

            col3.metric(
                "RMSSD",
                f"{basic_result['rmssd']:.2f} ms"
            )

            st.subheader("頻域分析")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "LF",
                f"{frequency_result['LF']:.2f}"
            )

            col2.metric(
                "HF",
                f"{frequency_result['HF']:.2f}"
            )

            col3.metric(
                "LF/HF",
                f"{frequency_result['LF_HF']:.2f}"
            )

    except Exception as e:

        st.error(
            f"分析失敗：{e}"
        )
