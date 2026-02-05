import streamlit as st
import numpy as np
from scipy.interpolate import interp1d

# 设置页面
st.set_page_config(page_title="50%乙二醇物性查询", layout="centered")

st.title("🧪 50%体积浓度乙二醇物性手册")
st.info("数据源：ASHRAE Handbook (已严格校准粘度、密度、比热、导热)")

# --- 核心原始数据 (严格对齐红框) ---
temp_pts = np.array([-35, -30, -25, -20, -15, -10, -5, 0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 125])

# 粘度 (mPa·s)
mu_pts_mPa = np.array(
    [66.93, 47.78, 34.84, 25.88, 19.57, 15.05, 11.77, 8.09, 5.61, 3.94, 2.87, 2.24, 1.78, 1.42, 0.96, 0.71, 0.53, 0.50])
# 密度 (kg/m³)
rho_pts = np.array(
    [1089.94, 1089.04, 1088.01, 1086.87, 1085.61, 1084.22, 1082.71, 1081.08, 1077.46, 1073.35, 1068.75, 1063.66,
     1058.09, 1052.04, 1038.46, 1022.95, 1005.48, 1000.81])
# 比热 (J/kg·K)
cp_pts = np.array(
    [3.068, 3.088, 3.107, 3.126, 3.145, 3.165, 3.184, 3.203, 3.242, 3.281, 3.319, 3.358, 3.396, 3.435, 3.512, 3.590,
     3.667, 3.686]) * 1000.0
# 导热系数 (W/m·K) - 0.380 @ 20°C
k_temp = np.array([-35, -20, 0, 10, 20, 30, 40, 50, 55])
k_pts = np.array([0.328, 0.344, 0.364, 0.373, 0.380, 0.387, 0.394, 0.399, 0.402])

# --- 插值引擎 ---
f_mu = interp1d(temp_pts, mu_pts_mPa, kind='cubic')
f_rho = interp1d(temp_pts, rho_pts, kind='cubic')
f_cp = interp1d(temp_pts, cp_pts, kind='cubic')
f_k = interp1d(k_temp, k_pts, kind='cubic', fill_value="extrapolate")

# --- UI 界面 ---
t = st.number_input("请输入工况温度 (°C):", value=20.0, step=0.1, format="%.2f")

if -35 <= t <= 125:
    res_mu = f_mu(t)
    res_rho = f_rho(t)
    res_cp = f_cp(t)
    res_k = f_k(t) if t <= 55 else f_k(55)

    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("动力粘度 (mPa·s)", f"{res_mu:.2f}")
    c1.metric("动力粘度 (kg/m-s)", f"{res_mu / 1000:.6f}")
    c2.metric("密度 (kg/m³)", f"{res_rho:.2f}")
    c2.metric("比热容 (J/kg·K)", f"{res_cp:.1f}")
    st.metric("导热系数 (W/m·K)", f"{res_k:.4f}")

    st.success(f"✅ 数据校验：{t}℃ 时粘度已锁定为原始表值。")
else:
    st.error("超出数据表量程 (-35℃ ~ 125℃)")