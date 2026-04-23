import streamlit as st
from datetime import datetime, timedelta
import random

# ================= CONFIG =================
st.set_page_config(page_title="ADS Intelligence System", layout="wide")

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"

DEMO_DURATION = 5
MAX_DEMO_ANALYSIS = 2
MAX_DEMO_GENERATOR = 2

# ================= STYLE =================
st.markdown("""
<style>
body, .main {background: radial-gradient(circle,#0B0F19,#020617); color:white;}
.card {
background: rgba(255,255,255,0.04);
border-radius:18px;
padding:1.2rem;
margin-bottom:1rem;
border:1px solid rgba(255,255,255,0.08);
}
.metric {font-size:1.8rem;font-weight:700;}
.gradient {
background: linear-gradient(90deg,#00E5A0,#00C2FF);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}
.btn {
background: linear-gradient(90deg,#00E5A0,#00C2FF);
padding:12px;border-radius:999px;text-align:center;font-weight:700;color:#020617;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "auth" not in st.session_state: st.session_state.auth=False
if "demo" not in st.session_state: st.session_state.demo=False
if "start" not in st.session_state: st.session_state.start=None
if "analysis" not in st.session_state: st.session_state.analysis=0
if "gen" not in st.session_state: st.session_state.gen=0
if "products" not in st.session_state: st.session_state.products=[]

# ================= DEMO =================
def start_demo():
    st.session_state.demo=True
    st.session_state.start=datetime.now()
    st.session_state.analysis=0
    st.session_state.gen=0

# ================= LOGIN =================
if not st.session_state.auth and not st.session_state.demo:
    st.title("ADS INTELLIGENCE SYSTEM™")
    col1,col2=st.columns(2)
    with col1:
        u=st.text_input("Username")
        p=st.text_input("Password",type="password")
        if st.button("Login"):
            if u==ADMIN_USERNAME and p==ADMIN_PASSWORD:
                st.session_state.auth=True
                st.rerun()
    with col2:
        if st.button("Demo 5 Menit"):
            start_demo()
            st.rerun()
    st.markdown(f'<a href="{CHECKOUT_LINK}"><div class="btn">Unlock Premium</div></a>',unsafe_allow_html=True)
    st.stop()

# ================= SIDEBAR =================
menu = st.sidebar.radio("Menu", ["📊 Dashboard","🧠 Decision Engine","✨ Generator","📦 Produk"])

# ================= HEADER =================
st.markdown('<div class="card"><h2 class="gradient">ADS INTELLIGENCE SYSTEM™</h2></div>', unsafe_allow_html=True)

# ================= DATABASE PRODUK =================
if menu=="📦 Produk":
    st.subheader("Database Produk")

    nama=st.text_input("Nama Produk")
    harga=st.number_input("Harga Jual",1000,1000000,100000)
    modal=st.number_input("Modal",500,500000,60000)
    admin=st.slider("Admin %",5,30,20)

    if st.button("Simpan Produk"):
        laba = harga - modal - (harga*admin/100)
        roas_bep = harga/laba if laba>0 else 999
        st.session_state.products.append({
            "nama":nama,
            "harga":harga,
            "modal":modal,
            "admin":admin,
            "laba":laba,
            "roas_bep":roas_bep
        })
        st.success("Tersimpan")

    for p in st.session_state.products:
        st.write(p["nama"],"| ROAS BEP:",round(p["roas_bep"],1))

# ================= DASHBOARD =================
if menu=="📊 Dashboard":

    st.subheader("Input Iklan")

    col1,col2=st.columns(2)
    with col1:
        imp=st.number_input("Impression",0,1000000,10000)
        click=st.number_input("Click",0,100000,300)
        spend=st.number_input("Spend",0,10000000,100000)
    with col2:
        sales=st.number_input("Omset",0,10000000,600000)
        order=st.number_input("Order",0,1000,6)
        target=st.number_input("Target ROAS",1.0,20.0,5.0)

    produk_list=[p["nama"] for p in st.session_state.products]
    pilih=st.selectbox("Pilih Produk",["Manual"]+produk_list)

    if pilih!="Manual":
        prod=next(p for p in st.session_state.products if p["nama"]==pilih)
        roas_bep=prod["roas_bep"]
        laba_produk=prod["laba"]
    else:
        roas_bep=3
        laba_produk=20000

    if st.button("Analisa"):

        ctr = (click/imp*100) if imp else 0
        roas = sales/spend if spend else 0
        profit = (laba_produk*order)-spend

        st.session_state.last=(roas,ctr,profit,roas_bep)

        colA,colB,colC,colD=st.columns(4)

        colA.markdown(f'<div class="card"><p>ROAS</p><div class="metric gradient">{roas:.1f}x</div></div>',unsafe_allow_html=True)
        colB.markdown(f'<div class="card"><p>CTR</p><div class="metric">{ctr:.1f}%</div></div>',unsafe_allow_html=True)
        colC.markdown(f'<div class="card"><p>Profit</p><div class="metric">{profit:,.0f}</div></div>',unsafe_allow_html=True)
        colD.markdown(f'<div class="card"><p>ROAS BEP</p><div class="metric">{roas_bep:.1f}x</div></div>',unsafe_allow_html=True)

# ================= DECISION ENGINE =================
if menu=="🧠 Decision Engine":

    if "last" not in st.session_state:
        st.warning("Analisa dulu di dashboard")
    else:
        roas,ctr,profit,roas_bep=st.session_state.last

        if roas < roas_bep:
            action="STOP / PERBAIKI PRODUK"
        elif roas > roas_bep*1.2:
            action="SCALE"
        else:
            action="OPTIMASI"

        insight = []

        if ctr < 2:
            insight.append("CTR rendah → masalah di kreatif")
        if roas < roas_bep:
            insight.append("Belum profit → jangan scale")
        if profit < 0:
            insight.append("Rugi → hentikan sementara")

        st.markdown(f'<div class="card"><h2 class="gradient">{action}</h2></div>',unsafe_allow_html=True)

        for i in insight:
            st.warning(i)

# ================= GENERATOR =================
if menu=="✨ Generator":

    mode=st.selectbox("Mode",["Shopee SEO","TikTok Viral"])
    nama=st.text_input("Nama Produk")

    if st.button("Generate"):
        if mode=="Shopee SEO":
            hasil=[
                f"{nama} Premium Terlaris Diskon",
                f"{nama} Best Seller Murah",
                f"{nama} Kualitas Import Promo"
            ]
        else:
            hasil=[
                f"STOP! Jangan beli {nama}",
                f"{nama} viral banget",
                f"{nama} solusi masalah kamu"
            ]

        for h in hasil:
            st.markdown("- "+h)

# ================= CTA =================
st.markdown(f'<a href="{CHECKOUT_LINK}"><div class="btn">Upgrade Premium</div></a>',unsafe_allow_html=True)
