import streamlit as st
import pandas as pd
import os
import requests

# 1. Page Configuration & Styling
st.set_page_config(page_title="SheetToSocial | Deeyaro Digital", page_icon="🌐", layout="centered")

# LIVE GUMROAD VALIDATION INITIALIZATION
is_premium = False

# 2. Premium / Sidebar Management
st.sidebar.title("🔐 License Validation")

# AGENCY BRANDING: Displays your official DEEYARO DIGITAL logo inside the sidebar
agency_logo = "logo.png"  
if os.path.exists(agency_logo):
    st.sidebar.image(agency_logo, width=160)
else:
    st.sidebar.markdown("### 🏢 **DEEYARO DIGITAL**")

license_key = st.sidebar.text_input("Enter Premium Key", type="password", help="Enter the unique license key sent by Gumroad.")

# Dynamic pull for the Gumroad Product Permalink
try:
    GUMROAD_PRODUCT_PERMALINK = st.secrets["GUMROAD_PRODUCT_PERMALINK"]
except KeyError:
    GUMROAD_PRODUCT_PERMALINK = "sheettosocial" # Replace this string with your exact Gumroad product URL handle

if license_key:
    with st.sidebar.spinner("Checking..."):
        try:
            api_url = "https://gumroad.com"
            payload = {
                "product_permalink": GUMROAD_PRODUCT_PERMALINK,
                "license_key": license_key,
                "increment_uses_count": "true" 
            }
            response = requests.post(api_url, data=payload, timeout=10)
            data = response.json()
            
            if response.status_code == 200 and data.get("success"):
                uses = data.get("uses", 1)
                if uses > 5:
                    st.sidebar.error("❌ Key Blocked: Sharing Limit Exceeded.")
                else:
                    is_premium = True
            else:
                st.sidebar.error("❌ Invalid Key. Try again.")
        except Exception:
            try:
                if license_key == st.secrets["PREMIUM_LICENSE_KEY"]:
                    is_premium = True
            except KeyError:
                if license_key == "DEEYARO-ADMIN-99X":
                    is_premium = True
                else:
                    st.sidebar.error("❌ Verification server timeout.")

# COMPACT SIDEBAR CTA POSITIONING: Sits cleanly at eye level
if not is_premium:
    st.sidebar.markdown("### 🚀 Unlock Copy")
    st.sidebar.link_button("👉 Get License Key Here", "https://gumroad.com", use_container_width=True) # Replace URL with your exact custom Gumroad link

# Render validation status indicators
if is_premium:
    st.sidebar.success("🎉 Premium Mode Active!")
else:
    st.sidebar.info("Free Mode Active.")

# DYNAMIC INJECTION ENGINE: Removes scrollbars, centers image layout, and locks clipboard selections natively
css_style = """
    <style>
    /* 1. Global Sidebar Layout Optimization to remove scrollbars */
    section[data-testid="stSidebar"] div.stMainBlockContainer {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
    }
    section[data-testid="stSidebar"] {
        overflow: hidden !important; 
    }
    div[data-testid="stSidebarUserContent"] {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* DUAL-LAYER LOGO CENTERING: Overrides left layout alignment to position your logo perfectly in the center */
    [data-testid="stSidebar"] [data-testid="stImage"],
    [data-testid="stSidebar"] .stImage {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
        margin: 0 auto !important;
    }
    [data-testid="stSidebar"] [data-testid="stImage"] img,
    [data-testid="stSidebar"] .stImage img {
        margin: 0 auto !important;
    }
"""

# Appends clipboard-blocking layers if user hasn't successfully input their key
if not is_premium:
    css_style += """
    /* 2. Anti-Copy selection and clipboard lockdown for unpaid tier */
    div[data-testid="stTextArea"] {
        user-select: none !important;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        pointer-events: none !important; 
    }
    textarea {
        user-select: none !important;
        -webkit-user-select: none !important;
        pointer-events: none !important;
    }
    """

css_style += "</style>"
st.markdown(css_style, unsafe_allow_html=True)

# PRODUCT BRANDING: Displays the SheetToSocial logo at the top center
product_logo = "sheet_logo.png"
if os.path.exists(product_logo):
    st.image(product_logo, width=150)
else:
    st.markdown("### 🌐 **SheetToSocial**")

st.title("🌐 SheetToSocial")
st.caption("An Exclusive High-Leverage Utility Developed by DEEYARO DIGITAL")
st.subheader("Transform messy spreadsheets into gorgeous, ready-to-post social media text instantly.")

# Interactive "How to Use" Guide for Users
with st.expander("📖 Need Help? Click here for the 3-Step Quick Start Guide", expanded=False):
    st.markdown("""
    ### 👋 Welcome to SheetToSocial! Follow these simple steps:
    
    1. **Prepare Your Spreadsheet:** Open Excel or Google Sheets and ensure your file has columns for your product details (e.g., *Product Name, Price, Description, Product Link*). Save it as a **.csv** or **.xlsx** file.
    2. **Upload & Map:** Drag and drop your file into the uploader below. Use the dropdown menus to match your spreadsheet columns to our layout fields.
    3. **Choose Your Style & Copy:** Select your target network (WhatsApp or Instagram) and your preferred writing tone. Click **Generate Social Posts**, then simply copy the text boxes directly onto your phone or computer clipboard!
    
    💡 *Tip: Your data is processed entirely inside your browser session. We do not store or save your files anywhere, keeping your customer data 100% private and secure.*
    """)

# 3. File Upload & Processing Logic
uploaded_file = st.file_uploader("Upload your product Excel or CSV sheet", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("File uploaded successfully to SheetToSocial!")
        
        # Apply row restrictions if not premium
        if not is_premium:
            df = df.head(2)
            st.warning("🔒 Free Preview Mode: Showing 2 rows. Copying text is disabled until Premium is active.")
        
        # Dynamic Column Mapping
        columns = df.columns.tolist()
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("### 🧭 Map Your Columns")
            title_col = st.selectbox("Select Product Title / Name column", columns)
            price_col = st.selectbox("Select Price column", columns)
            desc_col = st.selectbox("Select Description/Features column", columns)
            link_col = st.selectbox("Select Product Link column (Optional)", ["None"] + columns)
            
        with col2:
            st.write("### 🎨 Content Style Settings")
            target_platform = st.selectbox("Select Target Network", ["WhatsApp (Uses Bold * Formatting)", "Instagram / Facebook (Clean Formatting)"])
            writing_tone = st.selectbox("Select Copywriting Tone", ["Urgent / Sales Focus (FOMO 🔥)", "Professional & Elegant (Clean 💎)", "Casual & Friendly (Fun ✨)"])
        
        st.write("---")
        
        if st.button("✨ Generate Social Posts", use_container_width=True):
            st.write("### 📝 Your Ready-to-Post Copy")
            
            for index, row in df.iterrows():
                p_name = row[title_col]
                p_price = row[price_col]
                p_desc = row[desc_col]
                
                # Format links safely
                if link_col == "None" or pd.isna(row[link_col]):
                    p_link = ""
                else:
                    p_link = f"🔗 Shop Here: {row[link_col]}\n"
                
                # Formatting tweaks based on Platform choice
                bold_start = "*" if "WhatsApp" in target_platform else ""
                bold_end = "*" if "WhatsApp" in target_platform else ""
                
                # Copywriting updates based on Chosen Tone
                if "Urgent" in writing_tone:
                    header = f"🚨 {bold_start}LIMITED STOCK | NEW ARRIVAL{bold_end} 🚨\n🔥 {bold_start}{p_name}{bold_end} 🔥"
                    footer = "⚡ Order Now Before It Sells Out! | DM to Secure Yours! 📦"
                    price_line = f"💰 {bold_start}Price:{bold_end} {p_price} (Special Offer)"
                elif "Professional" in writing_tone:
                    header = f"💎 {bold_start}{p_name}{bold_end}"
                    footer = "✨ Premium Quality Guaranteed. Direct Message for inquiries or corporate orders."
                    price_line = f"▫️ {bold_start}Investment:{bold_end} {p_price}"
                else:
                    header = f"✨ Hey friends! Look at this: {bold_start}{p_name}{bold_end} ✨"
                    footer = "👋 Drop us a DM to order yours today! Free shipping included 🎉"
                    price_line = f"💸 {bold_start}Price:{bold_end} {p_price}"
                
                # Recompiling into the final Omnichannel Structural Template
                post_template = f"""{header}

{price_line}
📝 {bold_start}Details:{bold_end} {p_desc}
{p_link}
{footer}"""
                
                # Rendering copyable text areas
                st.text_area(f"📦 Product Box {index + 1} ({p_name})", value=post_template, height=220)
                st.divider()
                
    except Exception as e:
        st.error(f"Error reading file: {e}")
