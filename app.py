import streamlit as st
import pandas as pd
import os

# 1. Page Configuration & Styling
st.set_page_config(page_title="SheetToSocial | Deeyaro Digital", page_icon="🌐", layout="centered")

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

# 2. Premium / Sidebar Management
st.sidebar.title("🔐 License Validation")

# AGENCY BRANDING: Displays your official DEEYARO DIGITAL logo inside the sidebar
agency_logo = "logo.png"  
if os.path.exists(agency_logo):
    st.sidebar.image(agency_logo, use_container_width=True)
else:
    st.sidebar.markdown("### 🏢 **DEEYARO DIGITAL**")

license_key = st.sidebar.text_input("Enter Premium License Key", type="password", help="Leave blank for Free Version (Copy Protection Active)")

# SECURE SECRETS ENGINE: Dynamically fetches the validation key from your private dashboard settings
try:
    SECRET_KEY = st.secrets["PREMIUM_LICENSE_KEY"]
except KeyError:
    # Fail-safe backup value if dashboard panel setup is pending
    SECRET_KEY = "GROWBUSINESS2027" 

is_premium = (license_key == SECRET_KEY)

if is_premium:
    st.sidebar.success("🎉 SheetToSocial Premium Active! Copy Mode Unlocked.")
else:
    st.sidebar.info("Free Version Active: Copying text is restricted.")

# Premium Marketing Feature inside the Sidebar to drive sales
if not is_premium:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚀 Unlock Copy & Unlimited Rows")
    st.sidebar.markdown("Remove text copy protection, unlock full sheet conversions, and grab clean copy-ready outputs.")
    st.sidebar.markdown("[👉 Get Your Lifetime License Key Here](https://gumroad.com)") # Paste your actual Gumroad link here

# AIRTIGHT ANTI-COPY ENGINE: Complete selection and clipboard lockdown for unpaid tier
if not is_premium:
    st.markdown("""
        <style>
        /* Disables all text selection mechanisms across the output containers */
        div[data-testid="stTextArea"] {
            user-select: none !important;
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            pointer-events: none !important; /* Disables right clicks and text highlighting completely */
        }
        textarea {
            user-select: none !important;
            -webkit-user-select: none !important;
            -moz-user-select: none !important;
            -ms-user-select: none !important;
            pointer-events: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

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
