import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# DESAIN DAN JUDUL HALAMAN STREAMLIT
# ==========================================
st.set_page_config(page_title="Simulasi Monte Carlo UGD", layout="wide")

st.title(" Simulasi Monte Carlo: Estimasi Waktu Tunggu Layanan UGD")
st.write("""
Aplikasi ini digunakan untuk mengestimasi probabilitas rata-rata waktu tunggu pasien di Unit Gawat Darurat (UGD) 
melampaui Batas Standar Operasional Prosedur (SOP) Rumah Sakit menggunakan **Simulasi Monte Carlo**.
""")

st.markdown("---")

# ==========================================
# SIDEBAR: INPUT PARAMETER SIMULASI
# ==========================================
st.sidebar.header(" Parameter Simulasi")

# Input NIM untuk Seed Pembangkit Angka Acak
nim_input = st.sidebar.number_input("Masukkan NIM (sebagai Seed)", value=301230043, step=1)

# Input Parameter Distribusi Data Historis
st.sidebar.subheader("Parameter Data Historis")
mu_input = st.sidebar.number_input("Rata-Rata Waktu Tunggu / Mean (μ) [Menit]", value=26.50, step=0.1)
sigma_input = st.sidebar.number_input("Standar Deviasi / Std Dev (σ) [Menit]", value=7.20, step=0.1)

# Input Parameter Simulasi
st.sidebar.subheader("Skenario Simulasi")
num_simulations = st.sidebar.slider("Jumlah Iterasi Simulasi", min_value=1000, max_value=20000, value=10000, step=1000)
pasien_per_hari = st.sidebar.number_input("Jumlah Pasien Per Hari", value=100, step=10)

# Input Threshold SOP
sop_threshold = st.sidebar.number_input("Batas Maksimum SOP Waktu Tunggu (Menit)", value=30.00, step=0.5)

# ==========================================
# PROSES SIMULASI MONTE CARLO
# ==========================================
# Setting Random Seed
np.random.seed(int(nim_input))

# Generasi sampel acak waktu tunggu (Simulasi)
simulated_wait_times = np.random.normal(mu_input, sigma_input, (num_simulations, pasien_per_hari))

# Menghitung Rata-rata Waktu Tunggu Harian per Skenario
daily_avg_wait_time = np.mean(simulated_wait_times, axis=1)

# Analisis Risiko: Berapa kali rata-rata harian melebihi SOP
exceeded_scenarios = np.sum(daily_avg_wait_time > sop_threshold)
probability_exceeded = (exceeded_scenarios / num_simulations) * 100

# ==========================================
# TAMPILAN METRIK DAN HASIL ANALISIS
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📊 Total Skenario Simulasi", value=f"{num_simulations:,}")

with col2:
    st.metric(label="🚨 Skenario Melampaui SOP", value=f"{exceeded_scenarios:,}")

with col3:
    st.metric(label="⚠️ Probabilitas Terlambat (> SOP)", value=f"{probability_exceeded:.2f}%")

st.markdown("---")

# ==========================================
# VISUALISASI HISTOGRAM GRAPH
# ==========================================
st.subheader("📈 Visualisasi Distribusi Hasil Simulasi")

fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(daily_avg_wait_time, bins=40, kde=True, color='crimson', ax=ax)

# Garis ambang batas SOP
ax.axvline(x=sop_threshold, color='black', linestyle='--', linewidth=2, 
           label=f'Batas Maksimum SOP ({sop_threshold} Menit)')

ax.set_title(f"Distribusi Rata-Rata Waktu Tunggu UGD ({num_simulations:,} Iterasi)", fontsize=12)
ax.set_xlabel("Rata-Rata Waktu Tunggu Harian (Menit)")
ax.set_ylabel("Frekuensi Skenario")
ax.legend(loc="upper right")
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

# Kesimpulan Analisis Risiko
if probability_exceeded > 10.0:
    st.error(f"**Kesimpulan Risiko:** Probabilitas keterlambatan layanan tinggi ({probability_exceeded:.2f}%). Diperlukan penambahan alokasi tenaga medis UGD.")
else:
    st.success(f"**Kesimpulan Risiko:** Risiko keterlambatan tergolong rendah ({probability_exceeded:.2f}%). Operasional UGD berjalan sesuai standar SOP.")