# ======================================================
# DASHBOARD LPK PEKANBARU
# ======================================================

# ======================================================
# IMPORT LIBRARY
# ======================================================

import base64
import pandas as pd
import plotly.express as px
import streamlit as st


# ======================================================
# KONFIGURASI HALAMAN
# ======================================================

st.set_page_config(
    page_title="Dashboard LPK Pekanbaru",
    page_icon="📊",
    layout="wide"
)


# ======================================================
# FUNCTION : BACKGROUND & UI STYLE
# ======================================================

def add_bg_from_local(image_file):

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(
            image.read()
        ).decode()

    st.markdown(
        f"""
        <style>

        /* ======================================================
           GLOBAL STYLE
        ====================================================== */

        html, body, [class*="css"] {{
            font-family: 'Poppins', sans-serif;
            color: #000000;
        }}

        p, div, label {{
            color: #334155 !important;
            font-size: 15px;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: #0f172a !important;
            font-weight: 700 !important;
        }}

        /* ======================================================
           BACKGROUND
        ====================================================== */

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;

            width: 100%;
            height: 100%;

            background:
                linear-gradient(
                    rgba(255,255,255,0.35),
                    rgba(255,255,255,0.35)
                ),
                url("data:image/png;base64,{encoded}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;

            filter:
                blur(2px)
                brightness(1.08)
                saturate(1.1);

            transform: scale(1.02);

            z-index: -1;
        }}

        .stApp {{
            background: transparent;
        }}

        /* ======================================================
           MAIN CONTAINER
        ====================================================== */

        .block-container {{
            background: rgba(255,255,255,0.58);

            backdrop-filter: blur(18px);

            border-radius: 28px;

            padding: 2.5rem;

            border:
                1px solid rgba(255,255,255,0.35);

            box-shadow:
                0 10px 40px rgba(15,23,42,0.10);
        }}

        /* ======================================================
           METRIC CARD
        ====================================================== */

        [data-testid="metric-container"] {{
            background: rgba(255,255,255,0.72);

            border-radius: 22px;

            padding: 24px;

            border:
                1px solid rgba(255,255,255,0.4);

            backdrop-filter: blur(12px);

            box-shadow:
                0 6px 22px rgba(15,23,42,0.08);
        }}

        /* ======================================================
           SIDEBAR
        ====================================================== */

        section[data-testid="stSidebar"] {{
            background: rgba(255,255,255,0.45);

            backdrop-filter: blur(18px);
        }}

        /* ======================================================
           BUTTON
        ====================================================== */

        .stButton > button {{
            background:
                linear-gradient(
                    135deg,
                    #2563eb,
                    #3b82f6
                );

            color: white !important;

            border-radius: 14px;

            border: none;

            padding:
                0.65rem 1.4rem;

            font-weight: 600;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ======================================================
# LOAD BACKGROUND
# ======================================================

add_bg_from_local("MRAP12.jpg")


# ======================================================
# GOOGLE SHEET CONFIG
# ======================================================

SHEET_ID = "1wumyUK_I_1L6jAPs--7BfTxuDOaNWtwyeND-iICG-Q0"
GID = "1353375041"

URL = (
    f"https://docs.google.com/spreadsheets/d/"
    f"{SHEET_ID}/export?format=csv&gid={GID}"
)


# ======================================================
# FUNCTION : LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    df = pd.read_csv(URL)

    return df


# ======================================================
# LOAD DATAFRAME
# ======================================================

df = load_data()


# ======================================================
# DATA PREPROCESSING
# ======================================================

df['Jumlah PNBP'] = pd.to_numeric(
    df['Jumlah PNBP'],
    errors='coerce'
)


# ======================================================
# HEADER DASHBOARD
# ======================================================

st.title("📊 Dashboard Layanan Jenis LPK Pekanbaru")

st.markdown("""
Dashboard ini mengambil data langsung dari Google Spreadsheet
dan menampilkan visualisasi interaktif menggunakan Streamlit.
""")


# ======================================================
# SIDEBAR FILTER
# ======================================================

st.sidebar.header("⚙️ Filter Dashboard")

# ======================================================
# COPY DATAFRAME
# ======================================================

filtered_df = df.copy()

# ======================================================
# LOOP SELURUH KOLOM
# ======================================================

for column in df.columns:

    # ==========================================
    # FILTER KOLOM OBJECT / CATEGORY
    # ==========================================

    if df[column].dtype == 'object':

        # Ambil unique value
        unique_values = (
            df[column]
            .dropna()
            .unique()
            .tolist()
        )

        unique_values.sort()

        selected_values = st.sidebar.multiselect(
            f"Pilih {column}",
            unique_values
        )

        # Filter jika ada pilihan
        if selected_values:

            filtered_df = filtered_df[
                filtered_df[column].isin(selected_values)
            ]

    # ==========================================
    # FILTER KOLOM NUMERIK
    # ==========================================

    elif df[column].dtype in ['int64', 'float64']:

        min_value = float(df[column].min())
        max_value = float(df[column].max())

        selected_range = st.sidebar.slider(
            f"Range {column}",
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value)
        )

        filtered_df = filtered_df[
            (filtered_df[column] >= selected_range[0]) &
            (filtered_df[column] <= selected_range[1])
        ]

# ======================================================
# HASIL FILTER
# ======================================================

st.subheader("📄 Data Setelah Filter")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ======================================================
# TAMPILKAN DATAFRAME
# ======================================================

st.subheader("📄 Data Layanan")

st.dataframe(
    df,
    use_container_width=True
)


# ======================================================
# METRIC INFORMASI
# ======================================================

st.subheader("📌 Informasi Umum")

jumlah_jenis_layanan = filtered_df['Jenis Layanan'].nunique()

jumlah_jenis_ikan = filtered_df['Jenis Ikan'].nunique()

jumlah_dokumen = len(filtered_df)

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
        "Jumlah Dokumen",
        jumlah_dokumen
    )


# ======================================================
# FUNCTION : PIE CHART WILKER
# ======================================================

def create_wilker_chart(dataframe):

    wilker_count = (
        dataframe['Wilker']
        .astype(str)
        .value_counts()
        .reset_index()
    )

    wilker_count.columns = [
        'Wilker',
        'Jumlah'
    ]

    fig = px.pie(
        wilker_count,
        names='Wilker',
        values='Jumlah',
        hole=0.45,
        title='Persentase Wilker',
        template='plotly_white'
    )

    fig.update_traces(
        textinfo='percent+label'
    )

    return fig


# ======================================================
# PIE CHART WILKER
# ======================================================

st.subheader("🥧 Persentase Wilker")

fig_pie = create_wilker_chart(filtered_df)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)


# ======================================================
# FUNCTION : BAR CHART JENIS LAYANAN
# ======================================================

def create_layanan_chart(dataframe):

    layanan_count = (
        dataframe['Jenis Layanan']
        .value_counts()
        .reset_index()
    )

    layanan_count.columns = [
        'Jenis Layanan',
        'Jumlah'
    ]

    fig = px.bar(
        layanan_count,
        x='Jenis Layanan',
        y='Jumlah',
        text='Jumlah',
        title='Jumlah Dokumen per Jenis Layanan',
        template='plotly_white',
        color='Jumlah',
        color_continuous_scale='Blues'
    )

    return fig


# ======================================================
# BAR CHART JENIS LAYANAN
# ======================================================

st.subheader("📊 Jumlah Jenis Layanan")

fig_layanan = create_layanan_chart(filtered_df)

st.plotly_chart(
    fig_layanan,
    use_container_width=True
)


# ======================================================
# FUNCTION : CHART PNBP
# ======================================================

def create_pnbp_chart(dataframe):

    pnbp_layanan = (
        dataframe.groupby('Jenis Layanan')['Jumlah PNBP']
        .sum()
        .reset_index()
    )

    fig = px.bar(
        pnbp_layanan,
        x='Jenis Layanan',
        y='Jumlah PNBP',
        text='Jumlah PNBP',
        title='Total PNBP Berdasarkan Jenis Layanan',
        template='plotly_white',
        color='Jumlah PNBP',
        color_continuous_scale='Blues'
    )

    fig.update_traces(
        texttemplate='Rp %{text:,.0f}',
        textposition='outside'
    )

    return fig


# ======================================================
# CHART TOTAL PNBP
# ======================================================

st.subheader("💰 Total PNBP")

fig_pnbp = create_pnbp_chart(filtered_df)

st.plotly_chart(
    fig_pnbp,
    use_container_width=True
)


# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption("Loka Pengelolaan Kelautan Pekanbaru")


# ======================================================
# BUTTON REFRESH
# ======================================================

if st.button("🔄 Refresh Data"):

    st.cache_data.clear()

    st.rerun()
st.download_button()
