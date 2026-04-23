import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import hashlib

# ==================== 1. PREMIUM INTERFACE CONFIG (CSS) ====================
def apply_premium_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #E2E8F0;
    }
    
    .stApp {
        background: radial-gradient(circle at 20% 10%, #1e1b4b 0%, #0f172a 100%);
    }

    /* Glassmorphism Card */
    .premium-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .premium-card:hover {
        border: 1px solid rgba(0, 229, 160, 0.3);
    }

    /* Glowing Metrics */
    .metric-title {
        color: #94A3B8;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #fff, #94A3B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Custom Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00E5A0 0%, #00b894 100%);
        color: #0f172a !important;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 14px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 229, 160, 0.4);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* Status Badges */
    .badge-premium {
        background: linear-gradient(135deg, #FFD700, #B8860B);
        color: black;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== 2. INITIALIZATION & SECURITY ====================
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False
if "demo_mode" not in st.session_state: st.session_state["demo_mode"] = False
if "demo_start_time" not in st.session_state: st.session_state["demo_start_time"] = None
if "demo_analysis_count" not in st.session_state: st.session_state["demo_analysis_count"] = 0
if "demo_generator_count" not in st.session_state: st.session_state["demo_generator_count"] = 0
if "products" not in st.session_state: st.session_state["products"] = []
if "demo_history" not in st.session_state: st.session_state["demo_history"] = {}

ADMIN_USERNAME = "arkidigital"
ADMIN_PASSWORD = "Arkidigital2026"
[span_8](start_span)CHECKOUT_LINK = "https://muhammad-masruri.myscalev.com/checkout-pageku"[span_8](end_span)

def get_fingerprint():
    ua = st.context.headers.get('User-Agent', 'unknown')
    ip = st.context.headers.get('X-Forwarded-For', 'unknown')
    [span_9](start_span)return hashlib.md5(f"{ua}_{ip}".encode()).hexdigest()[span_9](end_span)

def is_demo_expired():
    if not st.session_state.get("demo_mode", False): return False
    start = st.session_state.get("demo_start_time")
    if start is None: return True
    [span_10](start_span)return (datetime.now() - start) > timedelta(minutes=5)[span_10](end_span)

# ==================== 3. LOGIN & ONBOARDING ====================
def show_login_page():
    apply_premium_ui()
    st.markdown("""
        <div style="text-align:center; padding-top: 50px;">
            <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 10px;">🩺 DOCTOR <span style="color:#00E5A0;">ADS</span></h1>
            <p style="color: #94A3B8; font-size: 1.2rem;">Predictive Analytics & AI Copywriting for Scale</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Member Access")
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")
        if st.button("UNLOCK PREMIUM"):
            if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
                st.session_state["authenticated"] = True
                st.session_state["demo_mode"] = False
                [span_11](start_span)st.rerun()[span_11](end_span)
            else: st.error("Invalid Credentials")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("### 🎁 Trial Portal")
        st.write("Experience full features with 5-minute limited access.")
        if st.button("LAUNCH FREE TRIAL"):
            st.session_state["demo_mode"] = True
            st.session_state["demo_start_time"] = datetime.now()
            [span_12](start_span)st.rerun()[span_12](end_span)
        st.markdown('</div>', unsafe_allow_html=True)

# ==================== 4. MAIN APPLICATION ====================
def main():
    st.set_page_config(page_title="Doctor Ads Premium", page_icon="🩺", layout="wide")
    apply_premium_ui()

    if not st.session_state["authenticated"] and not st.session_state["demo_mode"]:
        show_login_page()
        st.stop()

    if is_demo_expired():
        st.warning("⚠️ Trial Session Expired")
        [span_13](start_span)st.markdown(f'<a href="{CHECKOUT_LINK}" target="_blank" style="text-decoration:none;"><div class="stButton"><button>Upgrade to Premium Monthly</button></div></a>', unsafe_allow_html=True)[span_13](end_span)
        st.stop()

    # --- SIDEBAR & PRODUCT DATABASE ---
    with st.sidebar:
        st.markdown('## 🩺 DOCTOR <span style="color:#00E5A0;">ADS</span>', unsafe_allow_html=True)
        if st.session_state["authenticated"]:
            st.markdown('<span class="badge-premium">💎 PREMIUM ACCOUNT</span>', unsafe_allow_html=True)
        else:
            rem = max(0, 300 - int((datetime.now() - st.session_state["demo_start_time"]).total_seconds()))
            [span_14](start_span)st.markdown(f"⏳ Trial ends in: **{rem//60}:{rem%60:02d}**")[span_14](end_span)
        
        st.markdown("---")
        st.markdown("### 📦 Inventory Lab")
        
        # Product Logic (Minimalized for Performance)
        with st.expander("➕ New Product"):
            name = st.text_input("Name", key="p_name")
            hj = st.number_input("Selling Price", value=150000, step=5000)
            cost = st.number_input("COGS / Modal", value=80000, step=5000)
            if st.button("Save to Cloud"):
                [span_15](start_span)st.session_state.products.append({"name": name, "hj": hj, "cost": cost})[span_15](end_span)
                st.success("Product Saved")

    # --- DASHBOARD START ---
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.title("📊 Advertising Intelligence")
    st.markdown("Input your ad performance data for instant AI-driven recommendations.")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        impressions = st.number_input("👁️ Impressions", value=25000, step=1000)
        clicks = st.number_input("🖱️ Clicks", value=800, step=50)
    with col_b:
        spent = st.number_input("💸 Spent (Rp)", value=250000, step=10000)
        sales = st.number_input("💰 Sales Revenue (Rp)", value=1200000, step=50000)
    with col_c:
        orders = st.number_input("📦 Orders", value=12, step=1)
        platform = st.selectbox("📱 Platform", ["TikTok Ads", "Shopee Ads", "Meta Ads"])
    
    analyze_btn = st.button("RUN DEEP ANALYSIS")
    st.markdown('</div>', unsafe_allow_html=True)

    if analyze_btn:
        # [span_16](start_span)Metrics Calculation[span_16](end_span)
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = spent / clicks if clicks > 0 else 0
        roas = sales / spent if spent > 0 else 0
        
        # UI Metrics Display
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="premium-card"><div class="metric-title">CTR</div><div class="metric-value">{ctr:.2f}%</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="premium-card"><div class="metric-title">CPC</div><div class="metric-value">Rp{cpc:,.0f}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="premium-card"><div class="metric-title">ROAS</div><div class="metric-value" style="color:#00E5A0;">{roas:.2f}x</div></div>', unsafe_allow_html=True)
        with m4:
            profit = sales - spent
            st.markdown(f'<div class="premium-card"><div class="metric-title">NET PROFIT</div><div class="metric-value">Rp{profit:,.0f}</div></div>', unsafe_allow_html=True)

        # [span_17](start_span)[span_18](start_span)[span_19](start_span)Recommendation Engine[span_17](end_span)[span_18](end_span)[span_19](end_span)
        st.markdown("### 🧠 AI Strategic Recommendation")
        if roas > 5:
            st.success("🟢 **SCALE IDENTIFIED**: High ROAS detected. Increase budget by 25% every 48 hours.")
        elif roas < 2:
            st.error("🔴 **STOP LOSS**: ROAS below threshold. Audit creative hook & landing page immediately.")
        else:
            st.warning("🟡 **OPTIMIZE**: Stable performance. Test 3 new creative variations to lower CPC.")

    # --- AI COPYWRITER LAB ---
    st.markdown("---")
    st.subheader("✨ AI Copywriting Lab")
    tab1, tab2 = st.tabs(["🛍️ Marketplace (Shopee)", "🎥 Content Viral (TikTok)"])
    
    with tab1:
        prod_shopee = st.text_input("Product Name", key="shopee_name")
        if st.button("GENERATE SEO TITLE"):
            [span_20](start_span)st.code(f"🔥 BEST SELLER {prod_shopee.upper()} - Kualitas Premium & Garansi 100%", language="markdown")[span_20](end_span)

    with tab2:
        prod_tiktok = st.text_input("Product Name", key="tiktok_name")
        if st.button("GENERATE VIRAL HOOK"):
            [span_21](start_span)st.info(f"🎬 Hook: 'Jangan beli {prod_tiktok} sebelum liat video ini sampai habis! 😱'")[span_21](end_span)

    # --- FOOTER ---
    st.markdown(f"""
        <div style="text-align:center; padding: 40px; color: #64748B; font-size: 0.8rem;">
            © 2026 ARKIDIGITAL PREMIER - BUILT FOR PERFORMANCE<br>
            <a href="{CHECKOUT_LINK}" style="color:#00E5A0; text-decoration:none;">Upgrade to Elite Member</a>
        </div>
    [span_22](start_span)""", unsafe_allow_html=True)[span_22](end_span)

if __name__ == "__main__":
    main()
