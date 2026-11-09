import streamlit as st
import pandas as pd

# 1. Page Configuration & Styling
st.set_page_config(page_title="SheetToSocial | Deeyaro Digital", page_icon="📈", layout="centered")
st.title("📈 SheetToSocial")
st.caption("A premium digital utility by Deeyaro Digital")
st.subheader("Transform messy spreadsheets into gorgeous, ready-to-post social media text instantly.")

# 2. Premium / Sidebar Management
st.sidebar.title("🔐 License Validation")
license_key = st.sidebar.text_input("Enter Premium License Key", type="password", help="Leave blank for Free Version (2 rows limit)")

is_premium = (license_key == "GROWBUSINESS2027")

if is_premium:
    st.sidebar.success("Premium Mode Active! Unlimited Rows unlocked.")
else:
    st.sidebar.info("Free Version Active: Limited to processing 2 rows.")

# 3. File Upload & Processing Logic
uploaded_file = st.file_uploader("Upload your product Excel or CSV sheet", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("File uploaded successfully!")
        
        # Apply row restrictions if not premium
        if not is_premium:
            df = df.head(2)
            st.warning("Showing first 2 rows. Upgrade to Premium to format your entire sheet instantly!")
        
        # Dynamic Column Mapping
        columns = df.columns.tolist()
        st.write("### Map Your Columns")
        title_col = st.selectbox("Select Product Title / Name column", columns)
        price_col = st.selectbox("Select Price column", columns)
        desc_col = st.selectbox("Select Description/Features column", columns)
        link_col = st.selectbox("Select Product Link column (Optional)", ["None"] + columns)
        
        if st.button("✨ Generate Social Posts"):
            st.write("### 📝 Your Ready-to-Post Copy")
            
            for index, row in df.iterrows():
                p_name = row[title_col]
                p_price = row[price_col]
                p_desc = row[desc_col]
                p_link = "" if link_col == "None" else f"🔗 Shop Here: {row[link_col]}"
                
                # Beautiful Omnichannel Social Copy Structure
                post_template = f"""🔥 *{p_name}* 🔥

💰 *Price:* {p_price}
📝 *Details:* {p_desc}
{p_link}

📦 DM to Order | Fast Shipping Available! ✨"""
                
                st.text_area(f"Post {index + 1}", value=post_template, height=180)
                st.divider()
                
    except Exception as e:
        st.error(f"Error reading file: {e}")
