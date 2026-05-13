# ======================================================
# IMPORT LIBRARY
# ======================================================
import base64
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime

# ======================================================
# FUNCTION BACKGROUND + ELEGANT UI
# ======================================================
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        /* GLOBAL STYLE */
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
        /* BACKGROUND IMAGE */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(rgba(255,255,255,0.35), rgba(255,255,255,0.35)),
                        url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            filter: blur(2px) brightness(1.08) saturate(1.1);
            transform: scale(1.02);
            z-index: -1;
        }}
        .stApp {{
            background: transparent;
        }}
        /* MAIN CONTAINER */
        .block-container {{
            background: rgba(255,255,255,0.58);
            backdrop-filter: blur(18px);
            border-radius: 28px;
            padding: 2.5rem;
            border: 1px solid rgba(255,255,255,0.35);
            box-shadow: 0 10px 40px rgba(15,23,42,0.10);
        }}
        /* TITLE */
        .stTitle {{
            font-size: 46px !important;
            font-weight: 800 !important;
            color: #0f172a !important;
            letter-spacing: 0.5px;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.4);
        }}
        /* SUBHEADER */
        .stSubheader {{
            font-size: 28px !important;
            color: #1e293b !important;
            font-weight: 700 !important;
            margin-top: 20px;
        }}
        /* METRIC CARD */
        [data-testid="metric-container"] {{
            background: rgba(255,255,255,0.72);
            border-radius: 22px;
            padding: 24px;
            border: 1px solid rgba(255,255,255,0.4);
            backdrop-filter: blur(12px);
            box-shadow: 0 6px 22px rgba(15,23,42,0.08);
            transition: all 0.3s ease;
        }}
        [data-testid="metric-container"]:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 28px rgba(15,23,42,0.12);
        }}
        /* DATAFRAME */
        [data-testid="stDataFrame"] {{
            background: rgba(255,255,255,0.68);
            border-radius: 22px;
            padding: 14px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.35);
            box-shadow: 0 6px 20px rgba(15,23,42,0.08);
        }}
        /* SIDEBAR */
        section[data-testid="stSidebar"] {{
            background: rgba(255,255,255,0.45);
            backdrop-filter: blur(18px);
            border-right: 1px solid rgba(255,255,255,0.25);
        }}
        section[data-testid="stSidebar"] * {{
            color: #0f172a !important;
        }}
        /* BUTTON */
        .stButton > button {{
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            color: white !important;
            border-radius: 14px;
            border: none;
            padding: 0.65rem 1.4rem;
            font-weight: 600;
            box-shadow: 0 4px 14px rgba(37,99,235,0.25);
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            transform: scale(1.03);
            box-shadow: 0 8px 22px rgba(37,99,235,0.35);
        }}
        /* INPUT & SELECTBOX */
        .stSelectbox > div > div,
        .stTextInput > div > div > input {{
            background: rgba(255,255,255,0.78);
            border-radius: 14px;
            border: 1px solid rgba(203,213,225,0.7);
        }}
        /* PLOTLY CHART */
        .js-plotly-plot {{
            background: rgba(255,255,255,0.55);
            border-radius: 24px;
            padding: 12px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 24px rgba(15,23,42,0.08);
        }}
        /* SCROLLBAR */
        ::-webkit-scrollbar {{
            width: 10px;
        }}
        ::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.3);
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(100,116,139,0.4);
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# PANGGIL FUNCTION BACKGROUND
# ======================================================
add_bg_from_local("MRAP12.jpg")

# ======================================================
# JUDUL DASHBOARD
# ======================================================
st.title("📊 Dashboard Layanan Jenis LPK Pekanbaru")
st.markdown("""
Dashboard ini mengambil data langsung dari Google Spreadsheet
dan menampilkan visualisasi interaktif menggunakan Streamlit.
""")

# ======================================================
# LINK CSV GOOGLE SHEET
# ======================================================
sheet_id = "1wumyUK_I_1L6jAPs--7BfTxuDOaNWtwyeND-iICG-Q0"
gid = "1353375041"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

# ======================================================
# MEMBACA DATA
# ======================================================
@st.cache_data
def load_data():
    df = pd.read_csv(url)
    # Pastikan kolom Jumlah PNBP numerik
    if 'Jumlah PNBP' in df.columns:
        df['Jumlah PNBP'] = pd.to_numeric(df['Jumlah PNBP'], errors='coerce')
    return df

df = load_data()

# ======================================================
# PERSIAPAN FILTER BULAN (deteksi kolom bulan atau tanggal)
# ======================================================
bulan_col = None
df['bulan_filter_display'] = None  # untuk keperluan filter

# Cek apakah ada kolom bernama 'Bulan' (case insensitive)
for col in df.columns:
    if col.lower() == 'bulan':
        bulan_col = col
        # Gunakan nilai asli dari kolom tersebut sebagai display
        df['bulan_filter_display'] = df[col].astype(str)
        break

# Jika tidak ada, cari kolom tanggal
if bulan_col is None:
    for col in df.columns:
        if 'tanggal' in col.lower() or 'date' in col.lower() or 'tgl' in col.lower() or 'periode' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                if df[col].notna().any():
                    # Buat kolom display dengan format "Jan 2024" (atau sesuai)
                    df['bulan_filter_display'] = df[col].dt.strftime('%b %Y')  # contoh: "Jan 2024"
                    bulan_col = col
                    break
            except:
                continue

# Jika masih tidak ada, beri pesan bahwa filter bulan tidak tersedia
filter_bulan_tersedia = bulan_col is not None

# ======================================================
# SIDEBAR FILTER
# ======================================================
st.sidebar.header("🔍 Filter Data")

# 1. Filter Jenis Layanan (dropdown single select)
jenis_layanan_options = ["Semua"] + sorted(df['Jenis Layanan'].dropna().unique().tolist())
selected_layanan = st.sidebar.selectbox(
    "📋 Jenis Layanan",
    options=jenis_layanan_options,
    index=0
)

# 2. Filter Jenis Ikan (dropdown single select)
jenis_ikan_options = ["Semua"] + sorted(df['Jenis Ikan'].dropna().unique().tolist())
selected_ikan = st.sidebar.selectbox(
    "🐟 Jenis Ikan",
    options=jenis_ikan_options,
    index=0
)

# 3. Filter Wilker (dropdown single select)
wilker_options = ["Semua"] + sorted(df['Wilker'].dropna().astype(str).unique().tolist())
selected_wilker = st.sidebar.selectbox(
    "📍 Wilker",
    options=wilker_options,
    index=0
)

# 4. Filter Bulan (dropdown single select) - menggunakan kolom bulan_filter_display
if filter_bulan_tersedia:
    # Ambil nilai unik yang tidak null dari bulan_filter_display
    bulan_values = sorted(df['bulan_filter_display'].dropna().unique().tolist())
    bulan_options = ["Semua"] + bulan_values
    selected_bulan = st.sidebar.selectbox(
        "📅 Bulan",
        options=bulan_options,
        index=0
    )
else:
    selected_bulan = "Semua"
    st.sidebar.info("Tidak ditemukan kolom bulan atau tanggal. Filter bulan tidak tersedia.")

# 5. Pilihan Kolom Numerik untuk Visualisasi (dropdown)
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
if 'Jumlah PNBP' in numeric_columns:
    default_numeric = 'Jumlah PNBP'
else:
    default_numeric = numeric_columns[0] if numeric_columns else None

selected_numeric = st.sidebar.selectbox(
    "📊 Pilih Kolom Numerik untuk Visualisasi",
    options=numeric_columns if numeric_columns else ['Tidak ada kolom numerik'],
    index=0 if numeric_columns else 0,
    disabled=not numeric_columns
)

# ======================================================
# APLIKASI FILTER KE DATAFRAME
# ======================================================
df_filtered = df.copy()

# Filter Jenis Layanan (jika bukan "Semua")
if selected_layanan != "Semua":
    df_filtered = df_filtered[df_filtered['Jenis Layanan'] == selected_layanan]

# Filter Jenis Ikan (jika bukan "Semua")
if selected_ikan != "Semua":
    df_filtered = df_filtered[df_filtered['Jenis Ikan'] == selected_ikan]

# Filter Wilker (jika bukan "Semua")
if selected_wilker != "Semua":
    df_filtered = df_filtered[df_filtered['Wilker'].astype(str) == selected_wilker]

# Filter Bulan (jika filter tersedia dan pilihan bukan "Semua")
if filter_bulan_tersedia and selected_bulan != "Semua":
    df_filtered = df_filtered[df_filtered['bulan_filter_display'] == selected_bulan]

# ======================================================
# MENAMPILKAN DATA YANG SUDAH DIFILTER
# ======================================================
st.subheader("📄 Data Layanan LPK Pekanbaru (Terfilter)")
st.dataframe(df_filtered, use_container_width=True)

# ======================================================
# INFORMASI UMUM (berdasarkan data terfilter)
# ======================================================
st.subheader("📌 Informasi Umum Layanan Jenis LPK Pekanbaru")

jumlah_jenis_layanan = df_filtered['Jenis Layanan'].nunique()
jumlah_jenis_ikan = df_filtered['Jenis Ikan'].nunique()
jumlah_dokumen = len(df_filtered)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Jumlah Jenis Layanan", jumlah_jenis_layanan)
with col2:
    st.metric("Jumlah Jenis Ikan", jumlah_jenis_ikan)
with col3:
    st.metric("Jumlah Dokumen Diterbitkan", jumlah_dokumen)

# ======================================================
# PETA SUMATERA DENGAN GRADASI WARNA (CHOROPLETH ATAU MARKER)
# ======================================================
st.markdown("## 🗺️ Sebaran Data Layanan per Provinsi di Sumatera")

try:
    import requests
    import json
    import plotly.express as px
    import plotly.graph_objects as go

    # ------------------------------------------------------------------
    # 1. Mapping Wilker ke provinsi
    # ------------------------------------------------------------------
    wilker_to_provinsi = {
        "aceh": "Aceh",
        "sumatera utara": "Sumatera Utara",
        "sumut": "Sumatera Utara",
        "sumatera barat": "Sumatera Barat",
        "sumbar": "Sumatera Barat",
        "riau": "Riau",
        "kepulauan riau": "Kepulauan Riau",
        "kepri": "Kepulauan Riau",
        "tanjungpinang": "Kepulauan Riau",
        "batam": "Kepulauan Riau",
        "anambas": "Kepulauan Riau",
        "natuna": "Kepulauan Riau",
        "letung": "Kepulauan Riau",
        "jambi": "Jambi",
        "sumatera selatan": "Sumatera Selatan",
        "sumsel": "Sumatera Selatan",
        "bengkulu": "Bengkulu",
        "bangka belitung": "Kepulauan Bangka Belitung",
        "babel": "Kepulauan Bangka Belitung",
        "lampung": "Lampung",
    }

    def map_wilker(wilker_name):
        if pd.isna(wilker_name):
            return None
        nama = str(wilker_name).lower().strip()
        for key, prov in wilker_to_provinsi.items():
            if key in nama:
                return prov
        return None

    df_filtered['provinsi'] = df_filtered['Wilker'].apply(map_wilker)
    prov_counts = df_filtered[df_filtered['provinsi'].notna()].groupby('provinsi').size().reset_index(name='jumlah')
    if prov_counts.empty:
        st.warning("Tidak ada data provinsi yang cocok.")
    else:
        total = prov_counts['jumlah'].sum()
        prov_counts['persen'] = (prov_counts['jumlah'] / total) * 100

        # Koordinat pusat provinsi (lat, lon) untuk fallback marker
        prov_center = {
            "Aceh": (4.6951, 96.7494),
            "Sumatera Utara": (2.1154, 99.5451),
            "Sumatera Barat": (-0.7399, 100.8000),
            "Riau": (0.2933, 101.7068),
            "Kepulauan Riau": (0.9000, 104.4500),
            "Jambi": (-1.6101, 103.6131),
            "Sumatera Selatan": (-3.3194, 103.9144),
            "Bengkulu": (-3.7928, 102.2608),
            "Lampung": (-4.5585, 105.4068),
            "Kepulauan Bangka Belitung": (-2.7410, 106.4406),
        }
        prov_counts['lat'] = prov_counts['provinsi'].map(lambda p: prov_center.get(p, (0,0))[0])
        prov_counts['lon'] = prov_counts['provinsi'].map(lambda p: prov_center.get(p, (0,0))[1])

        # ------------------------------------------------------------------
        # 2. Coba tampilkan choropleth dengan GeoJSON
        # ------------------------------------------------------------------
        use_choropleth = False
        geojson_data = None
        # Daftar URL GeoJSON alternatif
        geojson_urls = [
            "https://raw.githubusercontent.com/alfarisi/indonesia-geojson/master/geojson/indonesia-province-simple.geojson",
            "https://raw.githubusercontent.com/putuwaw/indonesia-geojson/master/geojson/provinces.json",
            "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.geojson"
        ]
        for url in geojson_urls:
            try:
                resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                if resp.status_code == 200:
                    geojson_data = resp.json()
                    # Cek apakah ada properti 'name'
                    if 'features' in geojson_data and len(geojson_data['features']) > 0:
                        if 'properties' in geojson_data['features'][0] and 'name' in geojson_data['features'][0]['properties']:
                            use_choropleth = True
                            break
            except:
                continue

        if use_choropleth and geojson_data:
            # Filter fitur untuk Sumatera
            sumatera_prov = list(prov_center.keys())
            features = [f for f in geojson_data['features'] if f['properties'].get('name') in sumatera_prov]
            if features:
                geojson_sumatera = {"type": "FeatureCollection", "features": features}
                fig = px.choropleth_mapbox(
                    prov_counts,
                    geojson=geojson_sumatera,
                    locations='provinsi',
                    featureidkey="properties.name",
                    color='persen',
                    color_continuous_scale='Oranges',
                    range_color=(0, prov_counts['persen'].max()),
                    mapbox_style="carto-positron",
                    zoom=5.3,
                    center={"lat": -1.5, "lon": 102.5},
                    opacity=0.8,
                    labels={'persen': 'Persentase (%)'}
                )
                fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=600)
                st.plotly_chart(fig, use_container_width=True)
            else:
                use_choropleth = False

        if not use_choropleth:
            # Fallback: peta marker dengan gradasi warna
            fig = px.scatter_geo(
                prov_counts,
                lat='lat',
                lon='lon',
                color='persen',
                size=[20] * len(prov_counts),
                color_continuous_scale='Oranges',
                hover_name='provinsi',
                hover_data={'jumlah': ':,.0f', 'persen': ':.2f', 'lat': False, 'lon': False},
                title="Persentase per Provinsi (Marker)",
                projection='mercator'
            )
            fig.update_geos(
                showcoastlines=True, coastlinecolor='gray',
                showland=True, landcolor='lightgray',
                showocean=True, oceancolor='azure',
                lataxis_range=[-6, 7], lonaxis_range=[95, 110],
                resolution=50
            )
            fig.update_layout(height=600, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.info("GeoJSON tidak tersedia, ditampilkan peta marker dengan gradasi warna.")

        with st.expander("📋 Tabel Persentase per Provinsi"):
            st.dataframe(prov_counts[['provinsi', 'jumlah', 'persen']].sort_values('persen', ascending=False))

except Exception as e:
    st.error(f"Gagal menampilkan peta: {e}")

# ======================================================
# VISUALISASI PERBANDINGAN DENGAN KOLOM NUMERIK PILIHAN
# ======================================================
if numeric_columns and selected_numeric != 'Tidak ada kolom numerik':
    st.subheader(f"📊 Perbandingan {selected_numeric} Berdasarkan Kategori")

    # Tab untuk perbandingan
    tab1, tab2, tab3 = st.tabs(["Berdasarkan Jenis Layanan", "Berdasarkan Jenis Ikan", "Berdasarkan Bulan (jika ada)"])

    with tab1:
        # Group by Jenis Layanan
        agg_data = df_filtered.groupby('Jenis Layanan')[selected_numeric].sum().reset_index()
        agg_data = agg_data.sort_values(selected_numeric, ascending=False)
        fig = px.bar(agg_data, x='Jenis Layanan', y=selected_numeric,
                     text=selected_numeric,
                     title=f"Total {selected_numeric} per Jenis Layanan",
                     template='plotly_white',
                     color=selected_numeric, color_continuous_scale='Blues')
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(height=500, xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Group by Jenis Ikan
        agg_data = df_filtered.groupby('Jenis Ikan')[selected_numeric].sum().reset_index()
        agg_data = agg_data.sort_values(selected_numeric, ascending=False)
        fig = px.bar(agg_data, x='Jenis Ikan', y=selected_numeric,
                     text=selected_numeric,
                     title=f"Total {selected_numeric} per Jenis Ikan",
                     template='plotly_white',
                     color=selected_numeric, color_continuous_scale='Blues')
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(height=500, xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if filter_bulan_tersedia:
            # Gunakan kolom bulan_filter_display untuk grouping
            if 'bulan_filter_display' in df_filtered.columns:
                agg_data = df_filtered.groupby('bulan_filter_display')[selected_numeric].sum().reset_index()
                agg_data = agg_data.sort_values('bulan_filter_display')
                fig = px.line(agg_data, x='bulan_filter_display', y=selected_numeric,
                              markers=True,
                              title=f"Trend {selected_numeric} per Bulan",
                              template='plotly_white',
                              color_discrete_sequence=['#3b82f6'])
                fig.update_traces(line=dict(width=3), marker=dict(size=8))
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Tidak ada data bulan untuk ditampilkan.")
        else:
            st.info("Tidak ada kolom bulan atau tanggal yang valid.")

# ======================================================
# JUMLAH DOKUMEN PER JENIS LAYANAN (bar chart)
# ======================================================
st.markdown("## 📊 Jumlah Setiap Jenis Layanan (Terfilter)")
layanan_count = df_filtered['Jenis Layanan'].value_counts().reset_index()
layanan_count.columns = ['Jenis Layanan', 'Jumlah']
fig_layanan = px.bar(layanan_count, x='Jenis Layanan', y='Jumlah', text='Jumlah',
                     title='Jumlah Dokumen per Jenis Layanan', template='plotly_white',
                     color='Jumlah', color_continuous_scale='Blues')
fig_layanan.update_traces(textposition='outside')
fig_layanan.update_layout(height=500, xaxis_tickangle=-25)
st.plotly_chart(fig_layanan, use_container_width=True)

# ======================================================
# TOTAL PNBP PER JENIS LAYANAN (jika kolom tersedia)
# ======================================================
if 'Jumlah PNBP' in df_filtered.columns:
    st.markdown("## 💰 Total PNBP per Jenis Layanan (Terfilter)")
    try:
        pnbp_layanan = df_filtered.groupby('Jenis Layanan')['Jumlah PNBP'].sum().reset_index()
        fig_pnbp = px.bar(pnbp_layanan, x='Jenis Layanan', y='Jumlah PNBP', text='Jumlah PNBP',
                          title='Total PNBP Berdasarkan Jenis Layanan', template='plotly_white',
                          color='Jumlah PNBP', color_continuous_scale='Blues')
        fig_pnbp.update_traces(texttemplate='Rp %{text:,.0f}', textposition='outside')
        fig_pnbp.update_layout(height=500, xaxis_tickangle=-25)
        st.plotly_chart(fig_pnbp, use_container_width=True)
    except Exception as e:
        st.error(f"Terjadi error pada chart PNBP: {e}")

# ======================================================
# DOWNLOAD DATA (terfilter)
# ======================================================
st.markdown("### 📥 Download Data")
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(label="⬇️ Download Data Filter (.CSV)", data=csv,
                   file_name='data_layanan_lpk_pekanbaru_filtered.csv', mime='text/csv')

# ======================================================
# FOOTER
# ======================================================
st.markdown("---")
st.caption("Loka Pengelolaan Kelautan Pekanbaru")

if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()
