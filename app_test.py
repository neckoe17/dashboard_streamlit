# ======================================================
# IMPORT LIBRARY
# ======================================================

import streamlit as st
import pandas as pd
import plotly.express as px
# ======================================================

# ======================================================
# MEMBUAT BACKGROUND LAYAR
# ======================================================
# ======================================================
# BACKGROUND GRADIENT
# ======================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            to right,
            #dfe9f3,
            #ffffff
        );
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
#https://docs.google.com/spreadsheets/d/1wumyUK_I_1L6jAPs--7BfTxuDOaNWtwyeND-iICG-Q0/edit?gid=1353375041#gid=1353375041#
sheet_id = "1wumyUK_I_1L6jAPs--7BfTxuDOaNWtwyeND-iICG-Q0"

#sheet_name = "gabungan"

#url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

gid = "1353375041"   # ganti dengan gid sheet gabungan

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
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

#st.subheader("📌 Informasi Dataset")

#col1, col2, col3 = st.columns(3)

#with col1:
    #st.metric("Jumlah Baris", df.shape[0])

#with col2:
    #st.metric("Jumlah Kolom", df.shape[1])

#with col3:
    #st.metric("Total Data", df.size)
# ======================================================
# INFORMASI DATA
# ======================================================

st.subheader("📌 Informasi Dataset")

# Menghitung jumlah data
jumlah_jenis_layanan = df['Jenis Layanan'].nunique()

jumlah_jenis_ikan = df['Jenis Ikan'].nunique()

jumlah_dokumen = len(df)

# Membuat kolom metric
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Jumlah Jenis Layanan",
        jumlah_jenis_layanan
    )

with col2:
    st.metric(
        "Jumlah Jenis Ikan",
        jumlah_jenis_ikan
    )

with col3:
    st.metric(
        "Jumlah Dokumen Diterbitkan",
        jumlah_dokumen
    )
# ======================================================
# PILIH KOLOM NUMERIK
# ======================================================

#numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

# if len(numeric_columns) > 0:

#     st.subheader("📈 Visualisasi Data")

#     # Sidebar
#     st.sidebar.header("Filter Dashboard")

#     selected_column = st.sidebar.selectbox(
#         "Pilih Kolom Numerik",
#         numeric_columns
#     )
#     # ======================================================
#     # HISTOGRAM
#     # ======================================================

#     fig_hist = px.histogram(
#         df,
#         x=selected_column,
#         title=f"Distribusi {selected_column}",
#         template="plotly_white"
#     )

#     st.plotly_chart(fig_hist, use_container_width=True)

#     # ======================================================
#     # BOXPLOT
#     # ======================================================

#     fig_box = px.box(
#         df,
#         y=selected_column,
#         title=f"Boxplot {selected_column}",
#         template="plotly_white"
#     )
#     st.plotly_chart(fig_box, use_container_width=True)

#     # ======================================================
#     # BAR CHART
#     # ======================================================

#     if len(df.columns) >= 2:
#         category_column = st.sidebar.selectbox(
#             "Pilih Kolom Kategori",
#             df.columns
#         )

#         fig_bar = px.bar(
#             df,
#             x=category_column,
#             y=selected_column,
#             title=f"{selected_column} berdasarkan {category_column}",
#             template="plotly_white"
#         )

#         st.plotly_chart(fig_bar, use_container_width=True)

# else:
#     st.warning("Tidak ada kolom numerik pada dataset.")
# ======================================================
# VISUALISASI DATA
# ======================================================

st.subheader("📈 Visualisasi Dashboard")

# ======================================================
# PERSIAPAN DATA
# ======================================================

# Pastikan kolom PNBP bertipe numerik
df['Jumlah PNBP'] = pd.to_numeric(df['Jumlah PNBP'], errors='coerce')

# ======================================================
# PIE CHART WILKER
# ======================================================

st.markdown("## 🥧 Persentase Layanan Wilker")

wilker_count = (
    df['Wilker']
    .value_counts()
    .reset_index()
)

wilker_count.columns = ['Wilker', 'jumlah']

fig_pie = px.pie(
    wilker_count,
    names='Wilker',
    values='jumlah',
    title='Persentase Dokumen Yang Dikeluarkan per Wilker',
    hole=0.3
)

fig_pie.update_traces(
    textinfo='percent+label'
)

st.plotly_chart(fig_pie, use_container_width=True)

# ======================================================
# BAR CHART JENIS LAYANAN
# ======================================================

st.markdown("## 📊 Jumlah Setiap Jenis Layanan")

layanan_count = (
    df['Jenis Layanan']
    .value_counts()
    .reset_index()
)

layanan_count.columns = ['Jenis Layanan', 'jumlah']

fig_layanan = px.bar(
    layanan_count,
    x='Jenis Layanan',
    y='jumlah',
    text='jumlah',
    title='Jumlah Dokumen per Jenis Layanan',
    template='plotly_white'
)

fig_layanan.update_traces(
    textposition='outside'
)

st.plotly_chart(fig_layanan, use_container_width=True)

# ======================================================
# TOTAL PNBP PER JENIS LAYANAN
# ======================================================

st.markdown("## 💰 Total PNBP per Jenis Layanan")

pnbp_layanan = (
    df.groupby('Jenis Layanan')['Jumlah PNBP']
    .sum()
    .reset_index()
)

fig_pnbp = px.bar(
    pnbp_layanan,
    x='Jenis Layanan',
    y='Jumlah PNBP',
    text='Jumlah PNBP',
    title='Total PNBP Berdasarkan Jenis Layanan',
    template='plotly_white'
)

fig_pnbp.update_traces(
    texttemplate='Rp %{text:,.0f}',
    textposition='outside'
)

st.plotly_chart(fig_pnbp, use_container_width=True)

# ======================================================
# GRAFIK WAKTU LAYANAN
# ======================================================

# st.markdown("## 📅 Tren Waktu Jenis Layanan")

# try:

#     # Konversi tanggal
#     df['Tanggal Terbit Saji atau Rekom'] = pd.to_datetime(
#         df['Tanggal Terbit Saji atau Rekom'],
#         errors='coerce'
#     )

#     # Hapus data tanggal kosong
#     df_waktu = df.dropna(
#         subset=['Tanggal Terbit Saji atau Rekom']
#     )

#     # Grouping data
#     waktu_layanan = (
#         df_waktu.groupby([
#             df_waktu['Tanggal Terbit Saji atau Rekom'].dt.date,
#             'Jenis Layanan'
#         ])
#         .size()
#         .reset_index(name='Jumlah')
#     )

#     # Rename kolom tanggal
#     waktu_layanan.columns = [
#         'Tanggal',
#         'Jenis Layanan',
#         'Jumlah'
#     ]

#     # Membuat line chart
#     fig_time = px.line(
#         waktu_layanan,
#         x='Tanggal',
#         y='Jumlah',
#         color='Jenis Layanan',
#         markers=True,
#         title='Tren Waktu Jenis Layanan',
#         template='plotly_white'
#     )

#     # Tampilkan chart
#     st.plotly_chart(
#         fig_time,
#         use_container_width=True
#     )

# except Exception as e:

#     st.error(f"Terjadi error pada grafik waktu: {e}")
# # ======================================================
# # GRAFIK WAKTU PER JENIS LAYANAN
# # ======================================================

# st.markdown("## 📅 Waktu Pelayanan per Jenis Layanan")

# # # Pastikan kolom tanggal berbentuk datetime
# # df['tanggal'] = pd.to_datetime(
# #     df['tanggal'],
# #     errors='coerce'
# # )

# #Pastikan kolom tanggal berbentuk datetime
# df['Tanggal Terbit Saji atau Rekom'] = pd.to_datetime(
#     df['Tanggal Terbit Saji atau Rekom'],
#     errors='coerce'
# )

# waktu_layanan = (
#     df.groupby([
#         df['tanggal'].dt.date,
#         'Jenis Layanan'
#     ])
#     .size()
#     .reset_index(name='jumlah')
# )

# fig_time = px.line(
#     waktu_layanan,
#     x='Tanggal Terbit Saji atau Rekom',
#     y='jumlah',
#     color='Jenis Layanan',
#     markers=True,
#     title='Tren Waktu Jenis Layanan',
#     template='plotly_white'
# )

#st.plotly_chart(fig_time, use_container_width=True)
# ======================================================
# FOOTER
# ======================================================

st.markdown("---")
st.caption("Loka Pengelolaan Kelautan Pekanbaru")

if st.button("Refresh Data"):
    st.cache_data.clear()
