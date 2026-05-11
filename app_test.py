# ======================================================
# IMPORT LIBRARY
# ======================================================
import base64
import streamlit as st
import pandas as pd
import plotly.express as px
# ======================================================

# ======================================================
# MEMBUAT BACKGROUND LAYAR
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
# IMPORT
# ======================================================

import streamlit as st
import base64

# ======================================================
# FUNCTION BACKGROUND + CUSTOM CSS
# ======================================================

def add_bg_from_local(image_file):

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(
            image.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        /* =====================================================
           GLOBAL STYLE
        ===================================================== */

        html, body, [class*="css"] {{
            font-family: 'Segoe UI', sans-serif;
            color: #111111;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: #111111 !important;
            font-weight: 700 !important;
        }}

        p, label, div {{
            color: #222222 !important;
        }}

        /* =====================================================
           BACKGROUND IMAGE BLUR
        ===================================================== */

        .stApp::before {{

            content: "";

            position: fixed;

            top: 0;
            left: 0;

            width: 100%;
            height: 100%;

            background: url("data:image/png;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;

            filter: blur(3px) brightness(0.92);

            transform: scale(1.03);

            z-index: -1;
        }}

        .stApp {{
            background: transparent;
        }}

        /* =====================================================
           MAIN CONTAINER
        ===================================================== */

        .block-container {{

            background: rgba(255,255,255,0.28);

            backdrop-filter: blur(14px);

            border-radius: 25px;

            padding: 2rem;

            border: 1px solid rgba(255,255,255,0.25);

            box-shadow:
                0 8px 32px rgba(0,0,0,0.15);

        }}

        /* =====================================================
           TITLE
        ===================================================== */

        .stTitle {{
            font-size: 42px !important;
            font-weight: 800 !important;
            color: #0f172a !important;
        }}

        /* =====================================================
           SUBHEADER
        ===================================================== */

        .stSubheader {{
            color: #111827 !important;
            font-weight: 700 !important;
            font-size: 28px !important;
        }}

        /* =====================================================
           METRIC CARD
        ===================================================== */

        [data-testid="metric-container"] {{

            background: rgba(255,255,255,0.55);

            border-radius: 20px;

            padding: 22px;

            border: 1px solid rgba(255,255,255,0.35);

            backdrop-filter: blur(10px);

            box-shadow:
                0 4px 20px rgba(0,0,0,0.10);

            transition: 0.3s;
        }}

        [data-testid="metric-container"]:hover {{
            transform: translateY(-3px);
            box-shadow:
                0 8px 24px rgba(0,0,0,0.15);
        }}

        /* =====================================================
           DATAFRAME
        ===================================================== */

        [data-testid="stDataFrame"] {{

            background: rgba(255,255,255,0.45);

            border-radius: 18px;

            padding: 12px;

            backdrop-filter: blur(8px);

            border: 1px solid rgba(255,255,255,0.3);

            box-shadow:
                0 4px 18px rgba(0,0,0,0.08);

        }}

        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {{

            background: rgba(255,255,255,0.35);

            backdrop-filter: blur(18px);

            border-right:
                1px solid rgba(255,255,255,0.25);

        }}

        section[data-testid="stSidebar"] * {{
            color: #111111 !important;
        }}

        /* =====================================================
           BUTTON
        ===================================================== */

        .stButton > button {{

            background: linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            );

            color: white !important;

            border-radius: 12px;

            border: none;

            padding: 0.6rem 1.2rem;

            font-weight: 600;

            transition: 0.3s;
        }}

        .stButton > button:hover {{

            background: linear-gradient(
                135deg,
                #1d4ed8,
                #1e40af
            );

            transform: scale(1.02);
        }}

        /* =====================================================
           SELECTBOX
        ===================================================== */

        .stSelectbox > div > div {{

            background: rgba(255,255,255,0.55);

            border-radius: 12px;

        }}

        /* =====================================================
           PLOTLY CHART
        ===================================================== */

        .js-plotly-plot {{

            background: rgba(255,255,255,0.35);

            border-radius: 20px;

            padding: 10px;

            backdrop-filter: blur(8px);

            box-shadow:
                0 4px 20px rgba(0,0,0,0.08);

        }}

        /* =====================================================
           SCROLLBAR
        ===================================================== */

        ::-webkit-scrollbar {{
            width: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.2);
        }}

        ::-webkit-scrollbar-thumb {{
            background: rgba(0,0,0,0.25);
            border-radius: 10px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# PANGGIL FUNCTION
# ======================================================

add_bg_from_local("MRAP12.jpg")

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

template='plotly_white'

fig_pie.update_layout(
    height=500,
    title_x=0.5,
    font=dict(size=14) = px.pie(
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
