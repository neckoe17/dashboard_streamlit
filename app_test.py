# ======================================================
# IMPORT LIBRARY
# ======================================================

import streamlit as st
import pandas as pd
import plotly.express as px
# ======================================================
# ======================================================
# KONFIGURASI HALAMAN
# ======================================================

st.set_page_config(
    page_title="Dashboard Google Spreadsheet",
    page_icon="📊",
    layout="wide"
)
# ======================================================
# JUDUL DASHBOARD
# ======================================================

st.title("📊 Dashboard Data Google Spreadsheet")

st.markdown("""
Dashboard ini mengambil data langsung dari Google Spreadsheet
dan menampilkan visualisasi interaktif menggunakan Streamlit.
""")

# ======================================================
# LINK CSV GOOGLE SHEET
# ======================================================

sheet_id = "1wumyUK_I_1L6jAPs--7BfTxuDOaNWtwyeND-iICG-Q0"

sheet_name = "gabungan"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

# ======================================================
# MEMBACA DATA
# ======================================================

@st.cache_data
def load_data():
    df = pd.read_csv(url)
    return df

df = load_data()

# ======================================================
# MENAMPILKAN DATA
# ======================================================

st.subheader("📄 Data Spreadsheet")

st.dataframe(df, use_container_width=True)

# ======================================================
# INFORMASI DATA
# ======================================================

st.subheader("📌 Informasi Dataset")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Jumlah Baris", df.shape[0])

with col2:
    st.metric("Jumlah Kolom", df.shape[1])

with col3:
    st.metric("Total Data", df.size)

# ======================================================
# PILIH KOLOM NUMERIK
# ======================================================

numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

if len(numeric_columns) > 0:

    st.subheader("📈 Visualisasi Data")

    # Sidebar
    st.sidebar.header("Filter Dashboard")

    selected_column = st.sidebar.selectbox(
        "Pilih Kolom Numerik",
        numeric_columns
    )
    # ======================================================
    # HISTOGRAM
    # ======================================================

    fig_hist = px.histogram(
        df,
        x=selected_column,
        title=f"Distribusi {selected_column}",
        template="plotly_white"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    # ======================================================
    # BOXPLOT
    # ======================================================

    fig_box = px.box(
        df,
        y=selected_column,
        title=f"Boxplot {selected_column}",
        template="plotly_white"
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # ======================================================
    # BAR CHART
    # ======================================================

    if len(df.columns) >= 2:
        category_column = st.sidebar.selectbox(
            "Pilih Kolom Kategori",
            df.columns
        )

        fig_bar = px.bar(
            df,
            x=category_column,
            y=selected_column,
            title=f"{selected_column} berdasarkan {category_column}",
            template="plotly_white"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.warning("Tidak ada kolom numerik pada dataset.")

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")
st.caption("Dashboard dibuat menggunakan Streamlit & Google Spreadsheet")
