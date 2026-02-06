import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import os
import sys
import glob

# --- Custom Modules ---
import styles  # CSS Logic
import utils  # Helper functions (File loading, Security)
import education_page  # Education Page Logic
import stock_page  # Stock Page Logic
import strategy_logic  # Option Strategy Math & Charts

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
    page_title="ParisTrader - Quant Trading & Market Analysis | 2026香港投資銀行學習",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS from styles.py
styles.apply_custom_css()

# ==========================================
# 2. Main App Interface (Navigation)
# ==========================================

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0px; text-align: center; border-bottom: 1px solid #374151; margin-bottom: 20px;'>
        <h2 style='color: #F3F4F6; margin:0; letter-spacing: 1px; font-weight: 700;'>ParisTrader</h2>
        <p style='color: #9CA3AF; font-size: 0.85em; margin-top:5px;'>Quant Research</p>
    </div>
    """, unsafe_allow_html=True)


    # --- Navigation Logic ---
    def on_nav_change(key):
        if "main_nav_key" in st.session_state:
            st.query_params["page"] = st.session_state["main_nav_key"]
            if "sub" in st.query_params:
                del st.query_params["sub"]


    query_params = st.query_params
    url_main_page = query_params.get("page", "首頁 Home")
    url_sub_page = query_params.get("sub", None)

    main_options = [
        "首頁 Home", "研究專欄 Research", "大市情報 Intelligence", "實戰持倉 Portfolio",
        "美股數據 Stock", "期權分析 Option", "期貨/牛熊 Future",
        "自動交易 MT5 EA", "交易學院 Education", "交易社群 Community",
        "工具資源 Resources", "升級會員 VIP"
    ]

    try:
        main_default_index = main_options.index(url_main_page)
    except ValueError:
        matches = [i for i, opt in enumerate(main_options) if url_main_page in opt]
        main_default_index = matches[0] if matches else 0

    selected_nav = option_menu(
        menu_title="Navigation",
        options=main_options,
        icons=["house", "globe", "search", "briefcase", "list-task", "layers",
               "graph-up-arrow", "robot", "mortarboard", "people-fill", "collection", "gem"],
        menu_icon="compass",
        default_index=main_default_index,
        key="main_nav_key",
        on_change=on_nav_change,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#9CA3AF", "font-size": "15px"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "5px", "color": "#D1D5DB",
                         "--hover-color": "#1F2937"},
            "nav-link-selected": {"background-color": "#2563EB", "color": "#FFFFFF", "font-weight": "600"},
        }
    )

    # --- Submenu Handling ---
    target_page = selected_nav


    def handle_submenu(key_name, options, icons):
        default_sub_index = 0
        if (url_main_page in selected_nav) and (url_sub_page in options):
            default_sub_index = options.index(url_sub_page)
        elif (url_main_page in selected_nav) and url_sub_page:
            matches = [i for i, opt in enumerate(options) if url_sub_page in opt]
            if matches: default_sub_index = matches[0]

        return option_menu(
            menu_title=None, options=options, icons=icons, default_index=default_sub_index,
            styles={"container": {"padding": "0!important", "background-color": "rgba(255,255,255,0.03)",
                                  "border-radius": "10px"},
                    "nav-link": {"font-size": "14px", "margin": "3px", "--hover-color": "#374151"},
                    "nav-link-selected": {"background-color": "#4B5563"}},
            key=key_name
        )


    # Note: Stock, Intelligence, Future, Option submenus are removed (handled by Tabs in main area)
    if selected_nav == "自動交易 MT5 EA":
        st.caption("AUTOMATED TRADING")
        target_page = handle_submenu("sub_ea", ["EA 介紹 Introduction"], ["robot"])

    # Update URL for deep linking
    if selected_nav != target_page:
        if url_main_page != selected_nav or url_sub_page != target_page:
            st.query_params["page"] = selected_nav
            st.query_params["sub"] = target_page

    st.markdown("---")

    # VIP Button
    st.markdown("""
        <div class="vip-promo-card" style="background: linear-gradient(135deg, #B45309 0%, #F59E0B 50%, #D97706 100%); padding: 15px; border-radius: 12px; text-align: center; margin-bottom: 20px; border: 1px solid #FCD34D;">
            <h3 style="color: #FFFFFF; margin:0; font-size: 18px; font-weight: 800;">👑 升級 VIP 會員</h3>
            <p style="color: #FEF3C7; font-size: 12px; margin: 8px 0;">解鎖機構級數據 (Stock DNA)<br>& 實戰倉位 (Portfolio)</p>
            <a href="?page=升級會員 VIP" target="_self" style="display: block; width: 100%; background: #FFFFFF; color: #B45309; padding: 10px; border-radius: 6px; font-weight: 800; text-decoration: none;">🚀 立即加入 (Join Now)</a>
        </div>
    """, unsafe_allow_html=True)

if url_main_page == "Legal" and selected_nav == "首頁 Home":
    target_page = "Legal"

# ==========================================
# 3. Security Check for Standalone Pages
# ==========================================
locked_pages = []  # Currently handled inside tabs
if target_page in locked_pages:
    # We call the util function for security check
    if not utils.check_access_or_show_teaser(target_page):
        st.stop()

# ==========================================
# 4. Content Routing
# ==========================================

# [PAGE] HOME
if target_page == "首頁 Home":
    col_main, col_profile = st.columns([0.7, 0.3], gap="large")
    with col_main:
        st.markdown(
            "<h1 style='color:white;'>Ex-Ibanker開發-首個機構級黑科技</h1><h3 style='color:#94a3b8;'>美股期權策略|NQ HSI 金期貨自動交易EA </h3>",
            unsafe_allow_html=True)
        st.markdown("---")
        components.html("""
        <div class="tradingview-widget-container"><div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
        {"symbols": [{"proName": "FOREXCOM:SPXUSD", "title": "S&P 500"}, {"proName": "FOREXCOM:NSXUSD", "title": "US 100"}, {"description": "Gold", "proName": "OANDA:XAUUSD"}],
        "showSymbolLogo": true, "colorTheme": "dark", "isTransparent": true, "displayMode": "adaptive", "locale": "en"}</script></div>""",
                        height=100)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📺 網站使用教學")
        st.video("https://www.youtube.com/watch?v=qb3XtEPj8cA")
        st.markdown("<br>", unsafe_allow_html=True)

        st.link_button(label="📊 點擊閱讀：下周大市分析 (Weekly Market Analysis)",
                       url="https://parisprogram.uk/zh/member/post/RPT-20260131182122129?hash=e71209296eb426dd311b01d899a5615e5c858f30f34d39be3e589d137227761f",
                       type="primary", use_container_width=True)
        st.markdown("---")
        st.subheader("🧠 Week Ahead")
        with st.container():
            analysis_content = utils.load_weekly_analysis()
            with st.expander("📖 Click to expand/collapse full analysis", expanded=True):
                st.markdown(analysis_content)

    with col_profile:
        img_path = "static/profile.jpg"
        img_src = img_path if os.path.exists(
            img_path) else "https://ui-avatars.com/api/?name=Paris+Trader&background=0D8ABC&color=fff&size=150"
        st.markdown(f'<div class="profile-card"><img src="{img_src}" width="120" style="border-radius:50%;">',
                    unsafe_allow_html=True)
        st.markdown(
            """<h3 style="margin-top:10px; color:#F3F4F6;">Paris Trader</h3><p style="color: #9CA3AF; font-size: 0.9em;">Ex-Ibank Quantitative Trader</p><hr style="margin: 15px 0; border-top: 1px solid rgba(255,255,255,0.1);"><p style="text-align: left; font-size: 0.9em; line-height: 1.6; color: #e2e8f0;">專注於量化因子挖掘與程式化交易。<br><br><b>擅長策略 Core Strategies:</b><br>• 美股多因子長短倉<br>• 期貨NQ黃金HSI Scalping<br>• 美股期權異動簍略</p><a href="https://t.me/ParisTrader" target="_blank"><button style="background-color:#2563EB; color:white; border:none; padding:10px 20px; border-radius:6px; cursor:pointer; width:100%; margin-top:10px; font-weight:bold;">Contact Me</button></a></div>""",
            unsafe_allow_html=True)

# [PAGE] Market Dashboard
elif target_page == "Market Dashboard":
    st.title("Market Dashboard")
    path = os.path.join("MarketDashboard", "main_auto", "output")
    html_content, filename = utils.get_latest_file_content(path)
    if html_content:
        components.html(html_content, height=2500, scrolling=True)
    else:
        st.warning(f"⚠️ No dashboard files found. Error: {filename}")

# [PAGE] Research
elif target_page == "研究專欄 Research":
    st.title("🦅 Research Paper from Paris")
    st.caption("Institutional Perspectives on Daily Flows")
    files = sorted(glob.glob(os.path.join("DailyInsights", "*.md")), reverse=True)

    if not files:
        st.info("No insights published yet.")
    else:
        for i, file_path in enumerate(files):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            lines = content.split('\n')
            title = lines[0].replace('# ', '')
            date_display = "Recent"
            body_start_index = 1
            for idx, line in enumerate(lines):
                if "**Date:**" in line:
                    date_display = line.replace("**Date:**", "").strip()
                    body_start_index = idx + 1
                    break
            body = "\n".join(lines[body_start_index:])

            with st.container():
                c1, c2 = st.columns([1, 5])
                c1.markdown(
                    f"<div style='background: rgba(37,99,235,0.2); padding:5px; border-radius:5px; text-align:center;'>{date_display}</div>",
                    unsafe_allow_html=True)
                with c2.expander(f"📄 {title}", expanded=(i == 0)):
                    st.markdown(body)
                    st.markdown("---")

# [PAGE] Intelligence (Tabs)
elif target_page == "大市情報 Intelligence":
    st.title("📡 Market Intelligence")
    st.caption("Risk Metrics, Market Breadth & Positioning")
    tab_risk, tab_breadth, tab_cftc = st.tabs(["⚠️ Market Risk", "🌊 Market Breadth", "🐋 CFTC Position"])

    with tab_risk:
        st.subheader("Market Implied Risk")
        html_content, _ = utils.get_latest_file_content("ImpliedParameters")
        if html_content:
            fix_style = "<style>body {display: block !important; height: auto !important; min-height: 100vh; padding-top: 50px; background-color: #020617 !important;} .card { margin: 0 auto !important; }</style>"
            components.html(html_content.replace("<head>", "<head>" + fix_style), height=2200, scrolling=True)
        else:
            st.warning("⚠️ No risk reports found.")

    with tab_breadth:
        st.subheader("Market Breadth")
        html_content, _ = utils.get_latest_file_content(os.path.join("MarketDashboard", "MarketBreadth"),
                                                        "market_breadth_*.html")
        if html_content:
            components.html(html_content, height=2200, scrolling=True)
        else:
            st.warning("⚠️ Market Breadth report not found.")

    with tab_cftc:
        st.subheader("CFTC Institutional Positioning")
        html_content, _ = utils.get_latest_file_content("MarketDashboard", "cftc_pro_report*.html")
        if html_content:
            components.html(html_content, height=2200, scrolling=True)
        else:
            st.warning("⚠️ CFTC Report not found.")

# [PAGE] Stock Analytics (Refactored to external module)
elif target_page == "美股數據 Stock":
    stock_page.render_stock_page()

# [PAGE] Reddit Sentiment
elif target_page == "Reddit Sentiment":
    path = "Rddt"
    html_content, filename = utils.get_latest_file_content(path, "reddit_scanner_*.html")
    if html_content:
        st.caption(f"📅 Report Date: {filename}")
        components.html(html_content, height=2000, scrolling=True)
    else:
        st.warning("⚠️ No Reddit reports found.")

# [PAGE] Options (Tabs)
elif target_page == "期權分析 Option":
    st.title("🎯 Options Analytics")
    st.caption("Flows, Heatmaps & Strategy Builder")
    tab_hk, tab_us, tab_strat = st.tabs(["🇭🇰 HK Option", "🇺🇸 US Option", "🛠️ Strategy"])

    with tab_hk:
        st.subheader("HK Option Market Analysis")
        html, _ = utils.get_latest_file_content("Option", "HK_Option_Market_*.html")
        if html:
            components.html(html, height=2000, scrolling=True)
        else:
            st.warning("⚠️ No HK reports found.")

    with tab_us:
        st.subheader("US Option Strike Analysis")
        if utils.check_access_or_show_teaser("美股期權 US Option", description="Real-time unusual options activity."):
            html, _ = utils.get_latest_file_content("Option", "option_strike_*.html")
            if html:
                components.html(html, height=2000, scrolling=True)
            else:
                st.warning("⚠️ No US reports found.")

    with tab_strat:
        st.subheader("Interactive Option Strategy Builder")
        if utils.check_access_or_show_teaser("期權策略 Strategy", description="Quantitative Analysis."):
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                ticker = c1.text_input("Ticker", "NVDA", key="strat_ticker").upper()
                width = c2.number_input("Width ($)", 5, key="strat_width")
                call_otm = c3.number_input("Call OTM %", 1.03, step=0.01, key="strat_call")
                put_itm = c4.number_input("Put ITM %", 0.97, step=0.01, key="strat_put")
                if st.button("🚀 Generate", type="primary", use_container_width=True, key="strat_btn"):
                    with st.status(f"Processing {ticker}...", expanded=True) as status:
                        # Use strategy_logic module
                        try:
                            _, _, date = strategy_logic.get_local_data(ticker)
                            status.write(f"✅ Loaded data: {date}")
                            html, msg = strategy_logic.generate_strategy_html(ticker, width, call_otm, put_itm)
                            if html:
                                status.update(label="Done!", state="complete")
                                components.html(html, height=1400, scrolling=True)
                            else:
                                status.update(label="Failed", state="error")
                                st.error(msg)
                        except Exception as e:
                            st.error(f"Error: {e}")

# [PAGE] Future (Tabs)
elif target_page == "期貨/牛熊 Future":
    st.title("🎢 Futures & Trends")
    st.caption("Volatility, Volume & Heavy Zones")
    tab_vol, tab_vp, tab_cbbc = st.tabs(["⚡ Intraday Volatility", "📊 Volume Profile", "🐻 CBBC Ladder"])

    with tab_vol:
        st.subheader("Intraday Volatility Analysis")
        html = utils.load_html_file(os.path.join("MarketDashboard", "Intraday_Volatility.html"))
        if "File not found" not in html:
            components.html(html, height=1200, scrolling=True)
        else:
            st.warning("⚠️ Report not found")

    with tab_vp:
        st.subheader("Volume Profile Analysis")
        if utils.check_access_or_show_teaser("成交分佈 Volume Profile"):
            html, _ = utils.get_latest_file_content("VP")
            if html:
                components.html(html, height=1000, scrolling=True)
            else:
                st.warning("⚠️ No VP reports found")

    with tab_cbbc:
        st.subheader("HSI CBBC Heavy Zone")
        if utils.check_access_or_show_teaser("牛熊重貨區 CBBC Ladder"):
            html = utils.load_html_file(os.path.join("MarketDashboard", "HSI_CBBC_Ladder.html"))
            if "File not found" not in html:
                components.html(html, height=1200, scrolling=True)
            else:
                st.warning("⚠️ Report not found")

# [PAGE] Portfolio
elif target_page == "實戰持倉 Portfolio":
    st.title("💼 Paris Picks")
    path = "Trade"
    tab1, tab2 = st.tabs(["📉 Stock Journal", "📊 Option Desk"])
    is_vip = st.session_state.get("authentication_status", False)

    with tab1:
        html, filename = utils.get_latest_file_content(path, "trade_record_*.html")
        if html:
            st.caption(f"📅 Report: {filename}")
            if is_vip:
                components.html(html, height=1200, scrolling=True)
            else:
                st.info("👀 Preview Mode")
                components.html(html, height=600, scrolling=False)
                utils.check_access_or_show_teaser("Stock Journal Full Access", description="Unlock full journal.")
        else:
            st.warning("⚠️ Report not found.")

    with tab2:
        if utils.check_access_or_show_teaser("Option Desk"):
            html, filename = utils.get_latest_file_content(path, "option_record_*.html")
            if html:
                components.html(html, height=1200, scrolling=True)
            else:
                st.warning("⚠️ Report not found.")

# [PAGE] MT5 EA
elif target_page == "EA 介紹 Introduction":
    st.title("🤖 MT5 Expert Advisor")
    html = utils.load_html_file(os.path.join("MT5EA", "ea_marketing.html"))
    if "File not found" not in html:
        components.html(html, height=3000, scrolling=True)
    else:
        st.warning("⚠️ Content not found.")

# [PAGE] Education (External Module)
elif target_page == "交易學院 Education":
    education_page.render_education_page(utils.check_access_or_show_teaser, utils.load_markdown_with_images)

# [PAGE] Legal
elif target_page == "Legal":
    st.title("📜 Legal & Compliance")
    t1, t2, t3 = st.tabs(["Disclaimer", "Privacy", "Terms"])
    with t1:
        st.html(utils.load_html_file(os.path.join("Legal", "disclaimer.html")))
    with t2:
        st.html(utils.load_html_file(os.path.join("Legal", "privacy.html")))
    with t3:
        st.html(utils.load_html_file(os.path.join("Legal", "terms.html")))

# [PAGE] Resources
elif target_page == "工具資源 Resources":
    st.title("🔗 Trading Resources")
    html = utils.load_html_file(os.path.join("Resources", "external_links.html"))
    if "File not found" not in html:
        components.html(html, height=1000, scrolling=True)
    else:
        st.warning("⚠️ Content not found.")

# [PAGE] Community
elif target_page == "交易社群 Community":
    html = utils.load_html_file(os.path.join("Community", "community_promo.html"))
    if "File not found" not in html:
        components.html(html, height=1200, scrolling=True)
    else:
        st.error("⚠️ Content not found")

# [PAGE] Membership
elif target_page == "升級會員 VIP":
    st.title("💎 升級機構級數據")
    html = utils.load_html_file(os.path.join("Community", "membership_pricing.html"))
    if "File not found" not in html:
        components.html(html, height=1100, scrolling=True)
    else:
        st.error("⚠️ Content not found")

# Footer
st.markdown("""
<div class="custom-footer">
    <p>© 2026 Paris Trader. All rights reserved.<br><span style="font-size: 0.75rem; color: #6B7280;">Not financial advice.</span></p>
    <p><a href="https://t.me/algoparistrader" target="_blank">@ParisTrader on TG</a> | <a href="?page=Legal" target="_self" style="color: #6B7280; text-decoration: none;">Legal</a></p>
</div>
""", unsafe_allow_html=True)