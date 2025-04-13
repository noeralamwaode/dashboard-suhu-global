import streamlit as st
import pandas as pd
import plotly.express as px

# ===========================
# 🎯 Judul dan Deskripsi
# ===========================
st.set_page_config(page_title="Dashboard Suhu", layout="wide")
st.title("🌡️ Dashboard Suhu Global")
st.write("Analisis suhu rata-rata berdasarkan waktu dengan filter kota dan negara.")

# ===========================
# 📥 Load Data
# ===========================
df = pd.read_csv("temperatures.csv")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # Untuk Arrow compatibility

# ===========================
# 🧭 Sidebar Filter
# ===========================
st.sidebar.header("🔍 Filter Data")
selected_city = st.sidebar.selectbox("Pilih Kota", options=sorted(df['city'].unique()))
available_countries = df[df['city'] == selected_city]['country'].unique()
selected_country = st.sidebar.selectbox("Pilih Negara", options=sorted(available_countries))

# ===========================
# 🔍 Filtered Dataset
# ===========================
filtered_df = df[(df['city'] == selected_city) & (df['country'] == selected_country)]

# ===========================
# 📊 Statistik Deskriptif
# ===========================
st.subheader("📊 Statistik Deskriptif")
st.write(f"Data untuk kota: **{selected_city}**, negara: **{selected_country}**")
st.dataframe(filtered_df.describe())

# ===========================
# 📈 Grafik Rata-rata Suhu Bulanan
# ===========================
st.subheader("📉 Rata-rata Suhu Bulanan")
monthly_avg = filtered_df.groupby('month')['avg_temp_c'].mean().reset_index()
fig1 = px.line(
    monthly_avg, x='month', y='avg_temp_c', markers=True,
    title=f"Rata-rata Suhu Bulanan di {selected_city}, {selected_country}",
    labels={'month': 'Bulan', 'avg_temp_c': 'Suhu (°C)'}
)
st.plotly_chart(fig1, use_container_width=True)

# ===========================
# 📦 Boxplot Distribusi Suhu
# ===========================
st.subheader("📦 Distribusi Suhu Bulanan")
fig2 = px.box(
    filtered_df, x='month', y='avg_temp_c',
    title=f"Distribusi Suhu di {selected_city}, {selected_country}",
    labels={'month': 'Bulan', 'avg_temp_c': 'Suhu (°C)'}
)
st.plotly_chart(fig2, use_container_width=True)
