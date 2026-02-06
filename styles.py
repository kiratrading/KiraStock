import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500;700&display=swap');

        .stApp {
            background: transparent !important;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', 'Segoe UI', 'Microsoft JhengHei', sans-serif;
            color: #e2e8f0;
        }

        /* Navigation Font Optimization */
        [data-testid="stSidebarNav"] span {
            font-size: 14px !important;
            white-space: nowrap;
        }
        .nav-link {
            font-size: 14px !important;
            padding: 8px 10px !important;
        }

        /* Responsive Header Hiding */
        @media (min-width: 768.1px) {
            header { visibility: hidden !important; }
            [data-testid="stSidebarCollapseButton"] { display: none !important; }
            section[data-testid="stSidebar"] button { display: none !important; }
            [data-testid="stToolbar"], [data-testid="stHeaderActionElements"] { visibility: hidden !important; display: none !important; }
            #MainMenu { visibility: hidden !important; display: none !important; }
        }

        @media (max-width: 768px) {
            header { visibility: visible !important; background: transparent !important; }
            header button[kind="header"] {
                background-color: rgba(17, 24, 39, 0.6) !important;
                color: white !important;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 8px;
            }
            .block-container {
                padding-top: 3rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            h1 { font-size: 1.8rem !important; }
            h2 { font-size: 1.5rem !important; }
            h3 { font-size: 1.2rem !important; }
        }

        footer { visibility: hidden !important; display: none !important; }
        div[data-testid="stDecoration"] { display: none !important; }

        /* Background Effects */
        .fixed-bg {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            z-index: -1; 
            background-color: #020617;
            background-image: 
                linear-gradient(to right, rgba(255, 255, 255, 0.05) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
            background-size: 50px 50px;
            mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
            -webkit-mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
        }

        .fixed-blobs {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
            z-index: -1;
            background: 
                radial-gradient(circle at 10% 10%, rgba(79, 70, 229, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 20%, rgba(14, 165, 233, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 30% 90%, rgba(16, 185, 129, 0.1) 0%, transparent 40%);
            filter: blur(60px); pointer-events: none;
        }

        /* Sidebar & Cards */
        section[data-testid="stSidebar"] {
            background-color: #111827; 
            border-right: 1px solid #374151;
            z-index: 999999 !important;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            color: #F3F4F6 !important;
        }

        .profile-card {
            background: rgba(17, 24, 39, 0.7); backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px;
            padding: 25px; text-align: center;
        }

        .custom-footer {
            margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center; color: #94a3b8; font-size: 0.8rem;
        }
        .custom-footer a { color: #60a5fa; text-decoration: none; margin: 0 10px; }
        .custom-footer a:hover { text-decoration: underline; }
    </style>

    <div class="fixed-bg"></div>
    <div class="fixed-blobs"></div>
    """, unsafe_allow_html=True)