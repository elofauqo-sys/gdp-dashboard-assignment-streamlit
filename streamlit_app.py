import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Employee Survey Analysis",
    page_icon="👩‍💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/employee_survey.csv")
    return df

df = load_data()

# --- APP TITLE AND DESCRIPTION ---
st.title("👩‍💼 Employee Survey Data Analysis")
st.markdown("""
Dashboard ini melakukan exploratory data analysis (EDA) sederhana pada data survey karyawan.
Gunakan filter di sidebar untuk mengeksplorasi data.
""")

# --- SIDEBAR FOR FILTERS ---
st.sidebar.header("Filter Data Karyawan")

# Filter Departemen
departments = st.sidebar.multiselect(
    "Pilih Departemen",
    options=df["dept"].unique()
)

# Filter Gender
genders = st.sidebar.multiselect(
    "Pilih Gender",
    options=df["gender"].unique()
)

# Filter Job Role
job_roles = st.sidebar.multiselect(
    "Pilih Job Level",
    options=df["job_level"].unique()
)

# Filter Usia
age_min, age_max = int(df["age"].min()), int(df["age"].max())
age_slider = st.sidebar.slider(
    "Pilih Rentang Usia",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, age_max)
)

# --- FILTERING DATA ---
df_selection = df.copy()

if departments:
    df_selection = df_selection[df_selection["dept"].isin(departments)]
if genders:
    df_selection = df_selection[df_selection["gender"].isin(genders)]
if job_roles:
    df_selection = df_selection[df_selection["job_level"].isin(job_roles)]

df_selection = df_selection[
    (df_selection["age"] >= age_slider[0]) &
    (df_selection["age"] <= age_slider[1])
]

if df_selection.empty:
    st.warning("Tidak ada data untuk filter yang dipilih. Silakan ubah filter.")
    st.stop()

# --- MAIN PAGE CONTENT ---
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Karyawan", value=df_selection.shape[0])
with col2:
    avg_age = round(df_selection["age"].mean(), 1)
    st.metric(label="Rata-rata Usia", value=f"{avg_age} tahun")
with col3:
    if "MonthlyIncome" in df_selection.columns:
        avg_income = round(df_selection["MonthlyIncome"].mean(), 0)
        st.metric(label="Rata-rata Income", value=f"Rp {avg_income:,.0f}")

st.markdown("---")

# --- VISUALISASI ---
st.subheader("📈 Visualisasi")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("Distribusi Usia")
    st.bar_chart(df_selection["age"].value_counts().sort_index())

with viz_col2:
    if "WorkLifeBalance" in df_selection.columns:
        st.subheader("Rata-rata Work Life Balance per Departemen")
        avg_wlb = df_selection.groupby("dept")["WorkLifeBalance"].mean().round(1)
        st.bar_chart(avg_wlb)

# --- DISPLAY RAW DATA ---
with st.expander("Lihat Data Mentah"):
    st.dataframe(df_selection)
    st.markdown(f"**Dimensi Data:** {df_selection.shape[0]} baris, {df_selection.shape[1]} kolom")
