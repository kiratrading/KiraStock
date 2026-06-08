import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
import sys
import glob
import pandas as pd
import json
import base64
import html

# --- Custom Modules ---
import styles
import utils
import education_page
import stock_page
import strategy_logic
import recap_page
import admin_page

maxMessageSize = 600

# Add Trade folder path
sys.path.append('Trade')
try:
    from Trade import trade_app
except ImportError:
    pass

# ==========================================
# 1. Page Configuration & CSS
# ==========================================
st.set_page_config(
    page_title="StockNote | Kira Trader",
    page_icon="📓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Language Setup ---
if 'language' not in st.session_state:
    st.session_state['language'] = 'zh'


def toggle_language():
    if st.session_state['language'] == 'zh':
        st.session_state['language'] = 'en'
    else:
        st.session_state['language'] = 'zh'


# 翻譯字典
translations = {
    "zh": {
        "slogan_title": "我是投資美股的夜神月",
        "slogan_sub": "夜晚我翻開這本筆記本，看透市場結構的底層邏輯",
        "intro_text": "傳統圖表只告訴你「過去」發生什麼，我的死神之眼看到<b>「未來」大戶想去哪裡</b>。",
        "tutorial": "📺 網站使用教學",
        "weekly_btn": "📊 偷看本週大戶部署 (Weekly Analysis)",
        "week_ahead": "🧠 Week Ahead Strategy",
        "expander_title": "📖 點擊展開：大市前瞻與劇本",
        "contact_btn": "聯絡 L (Contact Me)",
        "vip_promo_title": "👑 解鎖大戶底牌",
        "vip_promo_desc": "偷看機構持倉 (Insider)<br>& 聰明錢流向 (Flow)",
        "vip_join": "🚀 簽署契約 (Join Now)",
        "nav_title": "DEATH NOTE",
        "settings": "語言設定 / Settings",
        "profile_text": """我將專業數據簡單化，捕捉爆升股。
<br><br>
<b>死神的武器 (My Edge):</b><br>
• 👁️ <b>Stock Hunter:</b> 捕捉機構建倉股<br>
• ⚡ <b>Futures Scalping:</b> NQ/HSI/黃金短線<br>
• 🎯 <b>Option Flow:</b> 異動期權狙擊<br>"""
    },
    "en": {
        "slogan_title": "I am the Kira of Wall Street",
        "slogan_sub": "When night falls, I open this notebook and see the true structure of the market.",
        "intro_text": "Traditional charts only show you the 'Past'. The Shinigami Eyes reveal <b>where Smart Money is going in the 'Future'</b>.<br>Stop guessing. See their final destination.",
        "tutorial": "📺 Platform Tutorial",
        "weekly_btn": "📊 Weekly Institutional Analysis",
        "week_ahead": "🧠 Week Ahead Strategy",
        "expander_title": "📖 Click to Expand: Market Outlook",
        "contact_btn": "Contact L",
        "vip_promo_title": "👑 Unlock the Eyes",
        "vip_promo_desc": "Insider Holdings<br>& Smart Money Flow",
        "vip_join": "🚀 Make the Pact",
        "nav_title": "DEATH NOTE",
        "settings": "Settings",
        "profile_text": """Democratizing institutional data to help you avoid retail traps.
<br><br>
<b>My Weapons:</b><br>
• 👁️ <b>Stock Hunter:</b> Track Institutional Builds<br>
• ⚡ <b>Futures Scalper:</b> NQ/XAU Copier<br>
• 🎯 <b>Abnormal Option Detect:</b> Sniper Unusual Activity<br>"""
    }
}


def t(key):
    return translations[st.session_state['language']].get(key, key)


# Helper Function: Handle Submenu
def handle_submenu(key_name, options, icons, default_url_sub=None):
    default_sub_index = 0
    if default_url_sub and (default_url_sub in options):
        default_sub_index = options.index(default_url_sub)
    elif default_url_sub:
        matches = [i for i, opt in enumerate(options) if default_url_sub in opt]
        if matches: default_sub_index = matches[0]

    return option_menu(
        menu_title=None, options=options, icons=icons, default_index=default_sub_index,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "border": "1px solid #4a0000",
                          "border-radius": "0px"},
            "nav-link": {"font-size": "14px", "margin": "3px", "--hover-color": "#2a0000", "color": "#a39b8a"},
            "nav-link-selected": {"background-color": "#4a0000", "color": "#fff"}},
        key=key_name
    )


# ==========================================
# GOTHIC / DEATH NOTE CSS THEME
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Cormorant+Garamond:wght@400;600;700&display=swap');

    /* 全域純黑與羊皮紙色文字 */
    .stApp {
        background-color: #030303;
        background-image: radial-gradient(circle at 50% 50%, #0a0000 0%, #030303 80%);
        color: #d1c9b8;
        font-family: 'Cormorant Garamond', serif;
    }

    /* 隱藏預設的頂部白條 */
    header {visibility: hidden;}

    /* Sidebar 血腥/黑暗風格 */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 2px solid #6b0000 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
        color: #d1c9b8;
    }

    /* 標題改為古羅馬襯線體 + 血紅色 */
    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: #8b0000 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px 5px rgba(139, 0, 0, 0.5);
    }

    /* 銳利化所有按鈕 */
    div.stButton > button {
        background-color: transparent !important;
        color: #8b0000 !important;
        border: 1px solid #8b0000 !important;
        border-radius: 0px !important;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        transition: 0.3s;
        box-shadow: inset 0 0 5px rgba(139, 0, 0, 0.2);
    }
    div.stButton > button:hover {
        background-color: #8b0000 !important;
        color: #030303 !important;
        box-shadow: 0 0 15px #8b0000;
    }

    /* Tabs 和 Expander 樣式覆蓋 */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a39b8a;
        border-bottom: 2px solid #2a0000;
        font-family: 'Cinzel', serif;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #8b0000;
        border-bottom: 2px solid #8b0000;
        background-color: rgba(139, 0, 0, 0.05);
    }
    .streamlit-expanderHeader {
        background-color: #050505 !important;
        border: 1px solid #4a0000 !important;
        border-radius: 0px !important;
        color: #8b0000 !important;
        font-family: 'Cinzel', serif;
    }
    .streamlit-expanderContent {
        border-left: 1px solid #4a0000 !important;
        border-right: 1px solid #4a0000 !important;
        border-bottom: 1px solid #4a0000 !important;
        background-color: #0a0a0a !important;
        border-radius: 0px !important;
    }

    /* 分隔線 */
    hr {
        border-top: 1px solid #4a0000;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Main App Interface (Navigation)
# ==========================================

# --- Sidebar ---
with st.sidebar:
    col_lang1, col_lang2 = st.columns([1, 3])
    with col_lang1:
        st.write("🌐")
    with col_lang2:
        lang_choice = st.radio("Language", ["中文", "English"],
                               index=0 if st.session_state['language'] == 'zh' else 1,
                               horizontal=True, label_visibility="collapsed")
        new_lang = 'zh' if lang_choice == "中文" else 'en'
        if new_lang != st.session_state['language']:
            st.session_state['language'] = new_lang
            st.rerun()

    st.markdown("""
    <div style='padding: 20px 0px; text-align: center; border-bottom: 1px dashed #4a0000; margin-bottom: 20px;'>
        <h2 style='color: #8b0000; margin:0; letter-spacing: 4px; font-weight: 700; font-family:"Cinzel", serif;'>StockNote</h2>
        <p style='color: #a39b8a; font-size: 0.8em; margin-top:5px; font-family:"Cormorant Garamond", serif;'>K I R A  T R A D E R</p>
    </div>
    """, unsafe_allow_html=True)

    nav_map_zh = {
        "新世界大門": "新世界大門",
        "試用死神之眼": "死神之眼 (Trial)",
        "Ｌ的監控網": "Ｌ的監控網",
        "股票研究": "制裁名單 (Recap)",
        "股票名單": "實戰筆記 (Portfolio)",
        "美股獵捕": "名單獵捕 (Hunter)",
        "期權佈局": "期權佈局 (Flow)",
        "期貨量圖": "期貨陣型 (Futures)",
        "死神EA": "死神自動機 (EA)",
        "交易法則": "筆記規則 (Rules)"
    }

    nav_map_en = {
        "新世界大門": "The First Page",
        "試用死神之眼": "Shinigami Eyes (Trial)",
        "Ｌ的監控網": "L's Radar",
        "股票研究": "Judgement (Recap)",
        "股票名單": "The Note (Portfolio)",
        "美股獵捕": "Target Hunter",
        "期權佈局": "Option Flow",
        "期貨量圖": "Futures Formations",
        "死神EA": "Kira Automata (EA)",
        "交易法則": "How to Use It"
    }

    current_nav_map = nav_map_zh if st.session_state['language'] == 'zh' else nav_map_en
    display_options = list(current_nav_map.values())

    query_params = st.query_params
    url_main_page = query_params.get("page", "新世界大門")
    url_sub_page = query_params.get("sub_page", None)  # <--- ADD THIS LINE

    try:
        main_default_index = list(nav_map_zh.keys()).index(url_main_page)
    except ValueError:
        main_default_index = 0

    # 換成更符合主題的隱晦 Icon
    selected_display = option_menu(
        menu_title=t("nav_title"),
        options=display_options,
        icons=["book", "eye", "radar", "droplet", "pen", "crosshair", "layers", "bar-chart-steps", "cpu",
               "info-circle"],
        menu_icon="book-half",
        default_index=main_default_index,
        key="main_nav_key",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#a39b8a", "font-size": "15px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "2px 0", "color": "#d1c9b8",
                         "border-radius": "0", "font-family": "'Cormorant Garamond', serif",
                         "--hover-color": "#1a0000"},
            "nav-link-selected": {"background-color": "#1a0000", "color": "#8b0000", "font-weight": "700",
                                  "border-left": "4px solid #8b0000", "border-radius": "0"},
        }
    )

    selected_nav = [k for k, v in current_nav_map.items() if v == selected_display][0]

    if url_main_page == "SecretAdmin" and selected_nav == "新世界大門":
        target_page = "SecretAdmin"
    elif url_main_page == "Legal" and selected_nav == "新世界大門":
        target_page = "Legal"
    else:
        target_page = selected_nav
        if target_page != url_main_page:
            st.query_params["page"] = target_page

    if selected_nav == "死神EA":
        st.caption("AUTOMATED EXECUTION")
        ea_options_display = ["啟動協議"] if st.session_state['language'] == 'zh' else ["Initiate Protocol"]
        target_sub = handle_submenu("sub_ea", ea_options_display, ["cpu"], url_sub_page)
        if target_sub in ["Initiate Protocol", "啟動協議"]:
            target_page = "EA 介紹"

    st.markdown("---")

if url_main_page == "Legal" and selected_nav == "新世界大門":
    target_page = "Legal"

# ==========================================
# 3. Security Check
# ==========================================
locked_pages = []
if target_page in locked_pages:
    if not utils.check_access_or_show_teaser(target_page):
        st.stop()

# ==========================================
# 4. Content Routing
# ==========================================

if target_page == "SecretAdmin":
    admin_page.render_admin_console()

elif target_page == "新世界大門":
    # 徹底反轉排版與視覺：左邊是Kira檔案，右邊是主體。
    col_profile, col_main = st.columns([0.35, 0.65], gap="large")

    with col_profile:
        # 移除舊照，使用無面孔/純文字暗黑風格 Avatar
        img_src = "https://ui-avatars.com/api/?name=K&background=000000&color=8b0000&size=150&font-size=0.6&rounded=false"

        st.markdown(f"""
        <div style="background: #050505; border: 1px solid #4a0000; padding: 25px; box-shadow: 5px 5px 0px #1a0000;">
            <div style="text-align: center; border-bottom: 1px solid #2a0000; padding-bottom: 15px;">
                <img src="{img_src}" width="100" style="border: 2px solid #8b0000; filter: grayscale(100%) contrast(120%);">
                <h2 style="margin-top:15px; margin-bottom: 0; color:#8b0000; font-family:'Cinzel', serif;">KIRA</h2>
                <p style="color: #a39b8a; font-style: italic; font-size: 0.9em; margin-top:5px;">"Delete the noise."</p>
            </div>
            <div style="font-size: 1em; line-height: 1.8; color: #d1c9b8; margin-top: 15px; font-family:'Cormorant Garamond', serif;">
                {t('profile_text')}
            </div>
            <a href="https://t.me/kira_stocknote" target="_blank" style="text-decoration: none;">
                <div style="background-color: transparent; border: 1px solid #8b0000; color: #8b0000; text-align: center; padding: 10px; margin-top: 20px; font-family: 'Cinzel', serif; font-weight: bold; cursor: pointer; transition: 0.3s;" onmouseover="this.style.backgroundColor='#8b0000'; this.style.color='#000';" onmouseout="this.style.backgroundColor='transparent'; this.style.color='#8b0000';">
                    {t('contact_btn')}
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col_main:
        st.markdown(f"""
            <div style="border-left: 4px solid #8b0000; padding-left: 20px;">
                <h1 style='color:#8b0000; font-size: 2.8em; margin-bottom: 0;'>{t('slogan_title')}</h1>
                <h3 style='color:#a39b8a; font-size: 1.4em; font-family:"Cormorant Garamond", serif; font-style: italic; margin-top: 5px;'>{t('slogan_sub')}</h3>
                <p style='font-size: 1.2em; color: #d1c9b8; line-height: 1.8; margin-top: 20px; font-family:"Cormorant Garamond", serif;'>
                {t('intro_text')}
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='border-bottom: 1px solid #4a0000; padding-bottom: 10px;'>🩸 The Judgement Records</h3>",
                    unsafe_allow_html=True)
        st.caption("見證名字被寫下的瞬間 (Market Executions)")

        # 完全重構的 HTML 排版，不再使用圖片，改用「案卷 / 筆記規則」風格，徹底消除 ParisTrader 痕跡
        notebook_proof_html = """
<style>
.execution-list { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
.execution-row { background: #050505; border: 1px solid #2a0000; border-left: 4px solid #8b0000; padding: 15px 20px; display: flex; flex-direction: column; position: relative; }
.execution-row::before { content: ''; position: absolute; top: 0; right: 0; width: 30px; height: 30px; background: linear-gradient(225deg, #030303 50%, #1a0000 50%); border-bottom-left-radius: 4px; }
.exec-time { font-family: 'Courier New', monospace; color: #8b0000; font-size: 0.85rem; font-weight: bold; letter-spacing: 1px; }
.exec-target { font-family: 'Cinzel', serif; font-size: 1.3rem; color: #fff; margin: 5px 0; }
.exec-quote { font-family: 'Cormorant Garamond', serif; font-style: italic; color: #a39b8a; font-size: 1.1rem; border-left: 2px solid #4a0000; padding-left: 10px; margin-top: 10px; }
.exec-status { position: absolute; right: 20px; bottom: 15px; color: #4a0000; font-family: 'Cinzel', serif; font-size: 0.8rem; border: 1px solid #4a0000; padding: 2px 8px; text-transform: uppercase; }
</style>

<div class="execution-list">
<div class="execution-row">
<div class="exec-time">CASE 01 - PRE-EARNINGS INTERCEPT</div>
<div class="exec-target">NVIDIA (NVDA)</div>
<div class="exec-quote">「這速度太誇張了... 新聞發布前，大戶的期權流向早就寫好了劇本。直接捕獲。」</div>
<div class="exec-status">Executed</div>
</div>

<div class="execution-row">
<div class="exec-time">CASE 02 - FOMC REVERSAL</div>
<div class="exec-target">SPX 0DTE</div>
<div class="exec-quote">「死神Bot即時提示，精準避開假突破，把握 FOMC 殺機。」</div>
<div class="exec-status">Terminated</div>
</div>

<div class="execution-row">
<div class="exec-time">CASE 03 - TREND INITIATION</div>
<div class="exec-target">XAU/USD (GOLD)</div>
<div class="exec-quote">「執行力與紀律的展現 - 運用Ｌ的監控網，在血洗前成功捕捉波段起漲點。」</div>
<div class="exec-status">Purged</div>
</div>
</div>
"""
        st.markdown(notebook_proof_html, unsafe_allow_html=True)


elif target_page == "Market Dashboard":
    st.title("Market Dashboard")
    path = os.path.join("MarketDashboard", "main_auto", "output")
    html_content, filename = utils.get_latest_file_content(path)
    if html_content:
        components.html(html_content, height=2500, scrolling=True)
    else:
        st.warning(f"⚠️ No dashboard files found. Error: {filename}")

elif target_page == "股票研究":
    st.title("⚖️ 判決紀錄 (Daily Recap)")
    if utils.check_access_or_show_teaser("股票研究", description="此為契約者專屬。解鎖每日死亡名單與深度解析。"):
        recap_page.render_recap_page(utils.load_markdown_with_images)

elif target_page == "試用死神之眼":
    st.title("👁️ 獨家指標試用與教學")
    st.caption("透過量化指標，看透莊家成本線")

    html_content = utils.load_html_file(os.path.join("Community", "indicator.html"))
    if "File not found" not in html_content:
        st.html(html_content)
    else:
        st.error("⚠️ 找不到 indicator.html。")

elif target_page == "Ｌ的監控網":
    st.title("📡 L's Radar (Ｌ的監控網)")
    st.caption("識別市場轉勢訊號 | Detect Market Reversals")
    tab_risk, tab_breadth, tab_cftc = st.tabs(["🩸 恐慌指數 Risk Meter", "🌊 市場寬度 Breadth", "🐋 莊家持倉 COT"])

    is_vip = st.session_state.get("authentication_status", False)

    with tab_risk:
        st.subheader("Market Implied Risk")
        html_content, _ = utils.get_latest_file_content("ImpliedParameters")
        if html_content:
            fix_style = "<style>body {display: block !important; height: auto !important; min-height: 100vh; padding-top: 50px; background-color: #030303 !important;} .card { margin: 0 auto !important; }</style>"
            final_html = html_content.replace("<head>", "<head>" + fix_style)
            if is_vip:
                components.html(final_html, height=2200, scrolling=True)
            else:
                st.info("👁️ 你的權限不足 (Preview Mode)")
                components.html(final_html, height=800, scrolling=False)
                utils.check_access_or_show_teaser("Risk Meter Full Access", description="簽訂契約以解鎖完整數據。")
        else:
            st.warning("⚠️ 查無檔案。")

    with tab_breadth:
        st.subheader("Market Breadth")
        html_content, _ = utils.get_latest_file_content(os.path.join("MarketDashboard", "MarketBreadth"),
                                                        "market_breadth_*.html")
        if html_content:
            if is_vip:
                components.html(html_content, height=2200, scrolling=True)
            else:
                st.info("👁️ 你的權限不足 (Preview Mode)")
                components.html(html_content, height=800, scrolling=False)
        else:
            st.warning("⚠️ 查無檔案。")

    with tab_cftc:
        st.subheader("CFTC Institutional Positioning")
        html_content, _ = utils.get_latest_file_content("MarketDashboard", "cftc_pro_report*.html")
        if html_content:
            if is_vip:
                components.html(html_content, height=2200, scrolling=True)
            else:
                st.info("👁️ 你的權限不足 (Preview Mode)")
                components.html(html_content, height=800, scrolling=False)
        else:
            st.warning("⚠️ 查無檔案。")

elif target_page == "美股獵捕":
    stock_page.render_stock_page()

elif target_page == "期權佈局":
    st.title("🎯 Options Flow Analytics")
    st.caption("跟蹤聰明錢異動 | Track Smart Money Flow")
    tab_us, tab_strat, tab_hk = st.tabs(["🇺🇸 美股期權異動", "🛠️ 策略模擬器 Strategy", "🇭🇰 港股期權佈局"])
    with tab_us:
        if utils.check_access_or_show_teaser("美股期權 US Option", description="Follow the Smart Money."):
            html, _ = utils.get_latest_file_content("Option", "option_strike_*.html")
            if html: components.html(html, height=2000, scrolling=True)
    with tab_strat:
        if utils.check_access_or_show_teaser("期權策略 Strategy"):
            st.info("請輸入代碼建立策略。")
            # 策略器UI省略細節，延續既有邏輯
            pass
    with tab_hk:
        html_str, _ = utils.get_latest_file_content("Option", "HK_Option_Market_*.html")
        if html_str: components.html(html_str, height=2000, scrolling=True)

elif target_page == "期貨量圖":
    st.title("🎢 Futures Formations")
    st.caption("短線波幅與牛熊重貨區 | Volatility & Heavy Zones")
    tab_vol, tab_vp, tab_cbbc = st.tabs(["⚡ 日內波幅 (Volatility)", "📊 成交分佈 (Volume Profile)", "🐻 牛熊陣型 (CBBC)"])

    with tab_vol:
        # Replace with your actual folder and file pattern for Volatility
        html_str, _ = utils.get_latest_file_content("MarketDashboard", "Intraday_Volatility*.html")
        if html_str:
            components.html(html_str, height=1200, scrolling=True)
        else:
            st.warning("⚠️ Volatility report not found.")

    with tab_vp:
        # Replace with your actual folder and file pattern for Volume Profile
        html_str, _ = utils.get_latest_file_content("VP", "volume_profile_*.html")
        if html_str:
            components.html(html_str, height=1200, scrolling=True)
        else:
            st.warning("⚠️ Volume Profile report not found.")

    with tab_cbbc:
        # Replace with your actual folder and file pattern for CBBC
        html_str, _ = utils.get_latest_file_content("MarketDashboard", "HSI_CBBC*.html")
        if html_str:
            components.html(html_str, height=1200, scrolling=True)
        else:
            st.warning("⚠️ CBBC report not found.")

elif target_page == "股票名單":
    st.title("📓 The Note (實戰倉位)")
    path = "Trade"
    tab1, tab2 = st.tabs(["📉 Stock Journal", "📊 Option Desk"])
    is_vip = st.session_state.get("authentication_status", False)
    with tab1:
        html_content, filename = utils.get_latest_file_content(path, "trade_record_*.html")
        if html_content:
            st.caption(f"📅 Report: {filename}")
            if is_vip:
                components.html(html_content, height=1200, scrolling=True)
            else:
                st.info("👁️ Preview Mode")
                components.html(html_content, height=800, scrolling=False)
    with tab2:
        pass

elif target_page == "EA 介紹":
    st.title("🤖 Kira Automata (EA)")
    html_content = utils.load_html_file(os.path.join("MT5EA", "ea_marketing.html"))
    if "File not found" not in html_content:
        st.html(html_content)
    else:
        st.warning("⚠️ Content not found.")

elif target_page == "交易法則":
    st.title("📜 筆記規則 (How to Use It)")
    if utils.check_access_or_show_teaser("交易法則", description="只有契約者能閱讀這些規則。"):
        education_page.render_education_page(utils.check_access_or_show_teaser, utils.load_markdown_with_images)

# Footer
st.markdown("""
<div style="margin-top: 50px; padding: 20px; border-top: 1px solid #2a0000; text-align: center; font-family: 'Cormorant Garamond', serif;">
    <p style="color: #6B7280; font-size: 0.9em; margin-bottom: 5px;">© 2026 StockNote. "Delete the noise."<br><span style="font-size: 0.75rem;">Not financial advice. The apple is a symbol.</span></p>
    <p><a href="https://t.me/kira_stocknote" target="_blank" style="color: #8b0000; text-decoration: none;">@kira_stocknote</a> | <a href="?page=Legal" target="_self" style="color: #4a0000; text-decoration: none;">Legal</a></p>
</div>
""", unsafe_allow_html=True)
