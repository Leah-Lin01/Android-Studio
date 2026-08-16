import numpy as np
from scipy.signal import welch


def calculate_basic_hrv(rr_intervals):
    """
    計算基本 HRV 指標
    rr_intervals 單位：毫秒
    """

    rr = np.asarray(rr_intervals, dtype=float)

    if len(rr) < 2:
        raise ValueError("RR Interval 資料不足")

    # 平均 RR
    mean_rr = np.mean(rr)

    # SDNN
    sdnn = np.std(rr, ddof=1)

    # RMSSD
    differences = np.diff(rr)

    rmssd = np.sqrt(
        np.mean(differences ** 2)
    )

    # 平均心率
    mean_hr = 60000 / mean_rr

    return {
        "mean_hr": float(mean_hr),
        "mean_rr": float(mean_rr),
        "sdnn": float(sdnn),
        "rmssd": float(rmssd)
    }


def calculate_frequency_domain(rr_intervals):
    """
    進行頻域 HRV 分析
    LF: 0.04 ~ 0.15 Hz
    HF: 0.15 ~ 0.40 Hz

    注意：
    RR Interval 是不等時間序列，
    正式分析前需要進行適當的重新取樣。
    """

    rr = np.asarray(rr_intervals, dtype=float)

    if len(rr) < 10:
        raise ValueError("RR Interval 資料不足，無法進行頻域分析")

    # RR 轉換成秒
    rr_seconds = rr / 1000.0

    # 建立累積時間
    time = np.cumsum(rr_seconds)

    # 去除第一筆造成的時間偏移
    time = time - time[0]

    # 重新取樣到 4 Hz
    sampling_rate = 4.0

    new_time = np.arange(
        0,
        time[-1],
        1 / sampling_rate
    )

    interpolated_rr = np.interp(
        new_time,
        time,
        rr
    )

    # 去平均值
    interpolated_rr = (
        interpolated_rr -
        np.mean(interpolated_rr)
    )

    # Welch PSD
    frequencies, power = welch(
        interpolated_rr,
        fs=sampling_rate,
        nperseg=min(
            256,
            len(interpolated_rr)
        )
    )

    # LF
    lf_mask = (
        (frequencies >= 0.04) &
        (frequencies < 0.15)
    )

    # HF
    hf_mask = (
        (frequencies >= 0.15) &
        (frequencies <= 0.40)
    )

    lf = np.trapezoid(
        power[lf_mask],
        frequencies[lf_mask]
    )

    hf = np.trapezoid(
        power[hf_mask],
        frequencies[hf_mask]
    )

    if hf > 0:
        lf_hf = lf / hf
    else:
        lf_hf = np.nan

    return {
        "LF": float(lf),
        "HF": float(hf),
        "LF_HF": float(lf_hf)
    }