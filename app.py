import streamlit as st
import pandas as pd
import os

# 1. Page Configuration & Styling (Changed icon from 📈 to 🌐)
st.set_page_config(page_title="SheetToSocial | Deeyaro Digital", page_icon="🌐", layout="centered")

# PRODUCT BRANDING: Displays the SheetToSocial logo at the top center
product_logo = "sheet_logo.png"
if os.path.exists(product_logo):
    st.image(product_logo, width=150)
else:
    st.markdown("### 🌐 **SheetToSocial**")

# REMOVED STOCK CHART EMOJI: Changed title emoji to a clean digital world icon
st.title("🌐 SheetToSocial")
st.caption("An exclusive high-leverage utility developed by DEEYARO DIGITAL")
st.subheader("Transform messy spreadsheets into gorgeous, ready-to-post social media text instantly.")

# 2. Premium / Sidebar Management
st.sidebar.title("🔐 License Validation")

# AGENCY BRANDING: Displays your official DEEYARO DIGITAL logo inside the sidebar
agency_logo = "logo.png"  
if os.path.exists(agency_logo):
    st.sidebar.image(agency_logo, use_container_width=True)
else:
    st.sidebar.markdown("### 🏢 **DEEYARO DIGITAL**")

license_key = st.sidebar.text_input("Enter Premium License Key", type="password", help="Leave blank for Free Version (2 rows limit)")

is_premium = (license_key == "GROWBUSINESS2027")

if is_premium:
    st.sidebar.success("🎉 SheetToSocial Premium Active! Unlimited Rows unlocked.")
else:
    st.sidebar.info("Free Version Active: Limited to processing 2 rows.")

# Premium Marketing Feature inside the Sidebar to drive sales
if not is_premium:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🚀 Unlock Unlimited Rows")
    st.sidebar.markdown("Process hundreds of products at once and unlock premium templates inside SheetToSocial.")
    st.sidebar.markdown("[👉 Get Your Lifetime License Key Here](https://gumroad.com)") # Paste your actual Gumroad link here

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
            st.warning("Showing first 2 rows. Upgrade to SheetToSocial Premium to format your entire sheet instantly!")
        
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
