# ======================================================
# IMPORT LIBRARY
# ======================================================

import base64
import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# CONFIG PAGE
# ======================================================

st.set_page_config(
    page_title="Dashboard LPK Pekanbaru",
    layout="wide"
)

# ======================================================
# FUNCTION BACKGROUND + UI
# ======================================================

def add_bg_from_local(image_file):

    with open(image_file, "rb") as image:
        encoded = base64.b64encode(
            image.read()
        ).decode()

    st.markdown(
        f"""
        <style>

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

        .block-container {{
            background: rgba(255,255,255,0.58);
            backdrop-filter: blur(18px);
            border-radius: 28px;
            padding: 2.5rem;
            border: 1px solid rgba(255,255,255,0.35);
            box-shadow: 0 10px 40px rgba(15,23,42,0.10);
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
# TITLE
# ======================================================

st.title("📊 Dashboard Layanan Jenis LPK Pekanbaru")

st.markdown("""
Dashboard ini mengambil data langsung dari Google Spreadsheet
dan menampilkan visualisasi interaktif menggunakan Streamlit.
""")

# ======================================================
# GOOGLE SHEET
# ======================================================

sheet_id = "1wumyUK_I_1L6jAPs--7BfTxuDOaNWtwyeND-iICG-Q0"

gid = "1353375041"

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    df = pd.read_csv(url)

    # Bersihkan nama kolom
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# ======================================================
# COPY DATAFRAME
# ======================================================

filtered_df = df.copy()

# ======================================================
# SIDEBAR FILTER
# ======================================================

st.sidebar.header("⚙️ Filter Dashboard")

# ======================================================
# FILTER NUMERIK
# ======================================================

st.sidebar.subheader("📊 Filter Data Numerik")

numeric_columns = filtered_df.select_dtypes(
    include=['int64', 'float64']
).columns.tolist()

for column in numeric_columns:

    try:

        min_value = float(filtered_df[column].min())
        max_value = float(filtered_df[column].max())

        selected_range = st.sidebar.slider(
            column,
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value)
        )

        filtered_df = filtered_df[
            (filtered_df[column] >= selected_range[0]) &
            (filtered_df[column] <= selected_range[1])
        ]

    except:
        pass

# ======================================================
# FILTER KATEGORI
# ======================================================

st.sidebar.subheader("🗂️ Filter Data Kategori")

non_numeric_columns = filtered_df.select_dtypes(
    exclude=['int64', 'float64']
).columns.tolist()

for column in non_numeric_columns:

    try:

        unique_values = (
            filtered_df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        unique_values.sort()

        selected_values = st.sidebar.multiselect(
            column,
            unique_values
        )

        if selected_values:

            filtered_df = filtered_df[
                filtered_df[column]
                .astype(str)
                .isin(selected_values)
            ]

    except:
        pass

# ======================================================
# KONVERSI NUMERIK
# ======================================================

if 'Jumlah PNBP' in filtered_df.columns:

    filtered_df['Jumlah PNBP'] = pd.to_numeric(
        filtered_df['Jumlah PNBP'],
        errors='coerce'
    )

# ======================================================
# DATAFRAME
# ======================================================

st.subheader("📄 Data Layanan LPK Pekanbaru")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ======================================================
# METRIC
# ======================================================

st.subheader("📌 Informasi Umum Layanan")

jumlah_jenis_layanan = (
    filtered_df['Jenis Layanan'].nunique()
    if 'Jenis Layanan' in filtered_df.columns
    else 0
)

jumlah_jenis_ikan = (
    filtered_df['Jenis Ikan'].nunique()
    if 'Jenis Ikan' in filtered_df.columns
    else 0
)

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
# PIE CHART WILKER
# ======================================================

st.markdown("## 🥧 Persentase Wilker")

if 'Wilker' in filtered_df.columns:

    wilker_count = (
        filtered_df['Wilker']
        .astype(str)
        .value_counts()
        .reset_index()
    )

    wilker_count.columns = [
        'Wilker',
        'Jumlah'
    ]

    fig_pie = px.pie(
        wilker_count,
        names='Wilker',
        values='Jumlah',
        hole=0.45,
        template='plotly_white'
    )

    fig_pie.update_traces(
        textinfo='percent+label'
    )

    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )

# ======================================================
# BAR CHART LAYANAN
# ======================================================

st.markdown("## 📊 Jumlah Setiap Jenis Layanan")

if 'Jenis Layanan' in filtered_df.columns:

    layanan_count = (
        filtered_df['Jenis Layanan']
        .value_counts()
        .reset_index()
    )

    layanan_count.columns = [
        'Jenis Layanan',
        'Jumlah'
    ]

    fig_layanan = px.bar(
        layanan_count,
        x='Jenis Layanan',
        y='Jumlah',
        text='Jumlah',
        color='Jumlah',
        color_continuous_scale='Blues',
        template='plotly_white'
    )

    fig_layanan.update_traces(
        textposition='outside'
    )

    st.plotly_chart(
        fig_layanan,
        use_container_width=True
    )

# ======================================================
# PNBP CHART
# ======================================================

st.markdown("## 💰 Total PNBP per Jenis Layanan")

if (
    'Jenis Layanan' in filtered_df.columns and
    'Jumlah PNBP' in filtered_df.columns
):

    pnbp_layanan = (
        filtered_df.groupby('Jenis Layanan')['Jumlah PNBP']
        .sum()
        .reset_index()
    )

    fig_pnbp = px.bar(
        pnbp_layanan,
        x='Jenis Layanan',
        y='Jumlah PNBP',
        text='Jumlah PNBP',
        color='Jumlah PNBP',
        color_continuous_scale='Blues',
        template='plotly_white'
    )

    fig_pnbp.update_traces(
        texttemplate='Rp %{text:,.0f}',
        textposition='outside'
    )

    st.plotly_chart(
        fig_pnbp,
        use_container_width=True
    )

# ======================================================
# DOWNLOAD
# ======================================================

st.markdown("### 📥 Download Data")

csv = filtered_df.to_csv(
    index=False
).encode('utf-8')

st.download_button(
    label="⬇️ Download Data Filter (.CSV)",
    data=csv,
    file_name='data_layanan_lpk_pekanbaru.csv',
    mime='text/csv'
)

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")
st.caption("Loka Pengelolaan Kelautan Pekanbaru")

if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()
