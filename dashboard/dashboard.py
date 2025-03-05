import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st # type: ignore
from babel.numbers import format_currency # type: ignore
sns.set(style='dark')
from datetime import datetime

# Konfigurasi Style
sns.set(style='darkgrid')

# Load Data
df = pd.read_csv("dashboard/all_data.csv")

# Konversi Kolom ke Format Datetime
df["dteday"] = pd.to_datetime(df["dteday"])

# Sidebar untuk Rentang Tanggal
min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")  # Ganti dengan logo jika ada
    start_date, end_date = st.date_input("Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter Data Berdasarkan Rentang Tanggal
main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

# Judul Dashboard
st.title("🚲 Bike Sharing Dashboard")
st.caption("Analisis data peminjaman sepeda berdasarkan berbagai faktor.")

# -- VISUALISASI 1: Peminjaman Sepeda per Jam --
st.subheader("Distribusi Peminjaman Sepeda Berdasarkan Jam")

hourly_df = main_df.groupby("hr")["cnt_hour"].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x="hr", y="cnt_hour", data=hourly_df, marker="o", color="#90CAF9", linewidth=2, ax=ax)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah Peminjaman Sepeda", fontsize=12)
ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Jam", fontsize=14)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Jumlah peminjaman sepeda meningkat pada jam sibuk, terutama di pagi dan sore hari saat orang berangkat dan pulang kerja.")

# -- VISUALISASI 2: Pengaruh Musim terhadap Peminjaman --
st.subheader("Pengaruh Musim terhadap Peminjaman Sepeda")

season_df = main_df.groupby("season_hour")["cnt_hour"].mean().reset_index()
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_df["season_hour"] = season_df["season_hour"].map(season_labels)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season_hour", y="cnt_hour", data=season_df, palette="coolwarm", ax=ax)
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Rata-rata Peminjaman Sepeda", fontsize=12)
ax.set_title("Rata-rata Peminjaman Sepeda Berdasarkan Musim", fontsize=14)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Musim gugur memiliki tingkat peminjaman tertinggi, sedangkan musim semi memiliki tingkat peminjaman terendah.")

# -- VISUALISASI 3: Hubungan Suhu dan Peminjaman Sepeda --
st.subheader("Hubungan Antara Suhu dan Peminjaman Sepeda")

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x="temp_hour", y="cnt_hour", data=main_df, alpha=0.5, color="#FFA07A", ax=ax)
ax.set_xlabel("Suhu (Normalized)", fontsize=12)
ax.set_ylabel("Jumlah Peminjaman Sepeda", fontsize=12)
ax.set_title("Hubungan Suhu dan Peminjaman Sepeda", fontsize=14)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Semakin tinggi suhu, semakin banyak sepeda yang dipinjam. Namun, pada suhu ekstrem, peminjaman cenderung berkurang.")

# -- VISUALISASI 4: Peminjaman Sepeda di Hari Kerja vs Hari Libur --
st.subheader("Peminjaman Sepeda di Hari Kerja vs Hari Libur")

workingday_df = main_df.groupby("workingday_hour")["cnt_hour"].mean().reset_index()
workingday_labels = {0: "Hari Libur", 1: "Hari Kerja"}
workingday_df["workingday_hour"] = workingday_df["workingday_hour"].map(workingday_labels)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="workingday_hour", y="cnt_hour", data=workingday_df, palette="viridis", ax=ax)
ax.set_xlabel("Jenis Hari", fontsize=12)
ax.set_ylabel("Rata-rata Peminjaman Sepeda", fontsize=12)
ax.set_title("Peminjaman Sepeda di Hari Kerja vs Hari Libur", fontsize=14)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Lebih banyak sepeda dipinjam pada hari kerja dibandingkan hari libur, menunjukkan bahwa banyak orang menggunakan sepeda untuk keperluan transportasi.")

# -- VISUALISASI 5: Pengaruh Kecepatan Angin terhadap Peminjaman --
st.subheader("Pengaruh Kecepatan Angin terhadap Peminjaman Sepeda")

fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x="windspeed_hour", y="cnt_hour", data=main_df, alpha=0.5, color="#32CD32", ax=ax)
ax.set_xlabel("Kecepatan Angin (Normalized)", fontsize=12)
ax.set_ylabel("Jumlah Peminjaman Sepeda", fontsize=12)
ax.set_title("Hubungan Kecepatan Angin dan Peminjaman Sepeda", fontsize=14)
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Kecepatan angin yang tinggi dapat mengurangi jumlah peminjaman sepeda, karena kondisi berkendara menjadi lebih sulit.")

from datetime import datetime

# --RFM ANALYSIS--
st.subheader("📊 RFM Analysis untuk Bike Sharing")

# Menentukan tanggal referensi (maksimum tanggal dalam dataset)
reference_date = main_df["dteday"].max()

# RFM Calculation
rfm_df = main_df.groupby("dteday").agg(
    Recency=("dteday", lambda x: (reference_date - x.max()).days),
    Frequency=("cnt_day", "sum"),  # Total peminjaman per hari
    Monetary=("cnt_day", "sum")  # Menggunakan jumlah peminjaman sebagai proxy Monetary
).reset_index()

# Normalisasi Data RFM agar lebih mudah dianalisis
rfm_scaled = rfm_df[["Recency", "Frequency", "Monetary"]]
rfm_scaled = (rfm_scaled - rfm_scaled.min()) / (rfm_scaled.max() - rfm_scaled.min())

# Scatter Plot: Recency vs Frequency
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=rfm_scaled["Recency"], y=rfm_scaled["Frequency"], alpha=0.7, color="blue", ax=ax)
ax.set_xlabel("Recency (Normalized)")
ax.set_ylabel("Frequency (Normalized)")
ax.set_title("Hubungan Recency dan Frequency dalam RFM Analysis")
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Pelanggan dengan Frequency tinggi tetapi Recency rendah adalah pengguna aktif yang baru-baru ini menggunakan layanan sepeda.")

# Scatter Plot: Frequency vs Monetary
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(x=rfm_scaled["Frequency"], y=rfm_scaled["Monetary"], alpha=0.7, color="red", ax=ax)
ax.set_xlabel("Frequency (Normalized)")
ax.set_ylabel("Monetary (Normalized)")
ax.set_title("Hubungan Frequency dan Monetary dalam RFM Analysis")
st.pyplot(fig)

st.write("🔍 **Kesimpulan:** Semakin sering seseorang menggunakan layanan ini, semakin besar total peminjaman yang mereka lakukan, sesuai dengan pola loyalitas pengguna.")

#terakhir
st.caption("Copyright (c) 2025 - Bike Sharing Dashboard by [Margohan] 🚲")

