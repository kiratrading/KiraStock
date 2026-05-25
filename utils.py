import streamlit as st
import os
import glob
import base64
import re
import time


# ==========================================
# 🔐 Security Login System
# ==========================================
def check_access_or_show_teaser(page_name, teaser_image_url=None, description=None):
    """
    If logged in -> Returns True.
    If not -> Shows teaser + Login button -> Returns False.
    """
    if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
        return True

    # --- Teaser UI ---
    st.markdown(f"""
    <div style="text-align: center; padding: 40px 20px; background: rgba(17, 24, 39, 0.6); border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.3);">
        <h2 style="color: #60a5fa;">🔒 Locked Feature: {page_name}</h2>
        <p style="font-size: 1.2em; color: #e2e8f0; max-width: 600px; margin: 0 auto;">
            {description if description else "This institutional-grade tool is reserved for VIP members."}
        </p>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 30px 0;">
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🔑 Member Login")
        with st.form(f"login_form_{page_name}"):
            email_input = st.text_input("Email", key=f"email_{page_name}")
            password_input = st.text_input("Password", type="password", key=f"pw_{page_name}")
            submit = st.form_submit_button("Login to Access", type="secondary", use_container_width=True)

            if submit:
                login_success = False
                try:
                    valid_emails = st.secrets["allowed_users"]["emails"]
                    correct_password = st.secrets["access_password"]
                    if email_input in valid_emails and password_input == correct_password:
                        st.session_state["authentication_status"] = True
                        st.session_state["user_email"] = email_input
                        st.success("Access Granted.")
                        login_success = True
                    else:
                        st.error("Invalid Credentials")
                except Exception as e:
                    st.error(f"System Config Error: {e}")

                if login_success:
                    time.sleep(0.5)
                    st.rerun()
    with c2:
        st.markdown("#### 🚀 Not a Member?")
        st.markdown("""
        <div style="background: rgba(37, 99, 235, 0.1); padding: 20px; border-radiushttps://t.me/kira_stocknote: 10px; border: 1px solid #2563EB;">
            <p style="font-size: 0.9em; margin-bottom: 15px;">
                Unlock this tool and get full access to Stock DNA, Option Flows, and my personal trade portfolio.
            </p>
            <a href="https://t.me/kira_stocknote" target="_blank" style="text-decoration: none;">
                <button style="width: 100%; background-color: #fbbf24; color: black; border: none; padding: 10px; border-radius: 5px; font-weight: bold; cursor: pointer;">
                    Get VIP Access Now
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if teaser_image_url:
        st.image(teaser_image_url, caption="Preview of Tool (Blur)", use_column_width=True)

    return False


# ==========================================
# 📂 File Loading Helpers
# ==========================================

def load_markdown_with_images(file_path):
    if not os.path.exists(file_path):
        return f"<div style='color:red'>⚠️ File not found: {file_path}</div>"

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')

    def replace_image_link(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        if not image_path.startswith('http') and os.path.exists(image_path):
            try:
                with open(image_path, "rb") as img_file:
                    b64_string = base64.b64encode(img_file.read()).decode()
                    ext = image_path.split('.')[-1].lower()
                    mime_type = f"image/{ext}"
                    if ext == 'svg': mime_type = "image/svg+xml"

                    return (
                        f'<div style="width:100%; text-align: center; margin: 20px 0;">'
                        f'<img src="data:{mime_type};base64,{b64_string}" alt="{alt_text}" '
                        f'style="max-width: 100%; max-height: 800px; width: auto; height: auto; '
                        f'border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">'
                        f'</div>'
                    )
            except Exception as e:
                return f"⚠️ Image Load Error: {str(e)}"
        return match.group(0)

    return image_pattern.sub(replace_image_link, content)


def load_weekly_analysis():
    file_path = os.path.join("WeeklyContent", "latest_analysis.md")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return "⚠️ Weekly analysis not uploaded yet."


def load_html_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return f"<div style='padding:20px; color:red;'>⚠️ File not found: {file_path}</div>"


def load_stock_dna_with_injection(base_dir):
    """
    Loads Stock DNA HTML and injects CSV data.
    base_dir should be passed from app.py using os.path.dirname(__file__)
    """
    html_path = os.path.join(base_dir, "FamaFrench", "index.html")
    csv_factor_path = os.path.join(base_dir, "FamaFrench", "stock_factor_data.csv")
    csv_returns_path = os.path.join(base_dir, "FamaFrench", "stock_returns_data.csv")

    if not os.path.exists(html_path):
        return f"<div style='color:red'>HTML not found: {html_path}</div>"

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Inject Factor Data
    if os.path.exists(csv_factor_path):
        with open(csv_factor_path, 'r', encoding='utf-8') as f:
            csv_data = f.read().replace('`', '')
        injection_js = f"""var csvData = `{csv_data}`; Papa.parse(csvData, {{ download: false, """
        target_str = 'Papa.parse("stock_factor_data.csv", {'
        if target_str in html_content:
            html_content = html_content.replace(target_str, injection_js)

    # Inject Returns Data
    if os.path.exists(csv_returns_path):
        with open(csv_returns_path, 'r', encoding='utf-8') as f:
            returns_data = f.read().replace('`', '')
        injection_js_ret = f"""var returnsCSVData = `{returns_data}`; Papa.parse(returnsCSVData, {{ download: false, """
        target_str_ret = 'Papa.parse("stock_returns_data.csv", {'
        if target_str_ret in html_content:
            html_content = html_content.replace(target_str_ret, injection_js_ret)

    html_content = html_content.replace('download: true,', '')
    return html_content


def get_latest_file_content(folder_path, pattern="*.html"):
    if not os.path.exists(folder_path):
        return None, f"Directory not found: {folder_path}"

    search_pattern = os.path.join(folder_path, pattern)
    list_of_files = glob.glob(search_pattern)

    if not list_of_files:
        return None, f"No files found matching {pattern}."

    latest_file = max(list_of_files, key=os.path.getctime)

    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return f.read(), os.path.basename(latest_file)
    except Exception as e:
        return None, str(e)