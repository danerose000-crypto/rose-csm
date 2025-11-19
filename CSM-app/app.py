import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(layout="wide")

# -------------------------
# 📌 HEADER BAR (Logo + Title)
# -------------------------
header_col1, header_col2 = st.columns([1, 4])

with header_col1:
    logo_path = Path(__file__).parent / "rose_logo.png"
    st.image(str(logo_path), width=120)


with header_col2:
    st.markdown(
        "<h1 style='margin-top: 20px; color:#C62828;'>Rose CSM Dashboard</h1>",
        unsafe_allow_html=True
    )
    st.write("Welcome to your AI-powered Customer Success workspace.")


# -------------------------
# 📁 Data: your book of business (initial)
# -------------------------
data = {
    "Customer": [
        "Summit Ridge Financial",
        "Pioneer Analytics Group",
        "Evergreen Capital Advisors",
        "BluePeak Holdings",
        "SilverLine Investment Partners"
    ],
    "ARR": [120000, 89000, 76000, 105000, 94000],
    "CSM": ["Dane", "Dane", "Dane", "Dane", "Dane"],
    "Health Score": [8.4, 7.1, 9.0, 6.8, 8.2],
    "Email": [
        "contact@summitridgefinancial.com",
        "ops@pioneeranalytics.com",
        "service@evergreencapital.com",
        "info@bluepeakholdings.com",
        "clientcare@silverlineinvest.com"
    ],
    "Phone": [
        "(208) 555-1010",
        "(208) 555-2020",
        "(208) 555-3030",
        "(208) 555-4040",
        "(208) 555-5050"
    ],
    "Address": [
        "123 Ridge Way, Boise, ID",
        "450 Pioneer Ave, Meridian, ID",
        "780 Evergreen Ln, Eagle, ID",
        "62 BluePeak Dr, Boise, ID",
        "19 Silverline Blvd, Nampa, ID"
    ]
}

required_cols = ["Customer", "ARR", "CSM", "Health Score", "Email", "Phone", "Address"]

# Use session_state so updates persist while the app is running
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(data)
else:
    # If old df is missing new columns, reset it
    if any(col not in st.session_state.df.columns for col in required_cols):
        st.session_state.df = pd.DataFrame(data)

if "notes" not in st.session_state:
    st.session_state.notes = {name: "" for name in data["Customer"]}

df = st.session_state.df

# -------------------------
# 📁 Customer List (Top only)
# -------------------------
st.subheader("📁 Customer List")

df_display = df.copy()
df_display.index = df_display.index + 1    # show index starting at 1
df_display["ARR"] = df_display["ARR"].apply(lambda x: f"${x:,.0f}")  # format ARR as $###
st.dataframe(df_display)

# -------------------------
# 📌 Customer Details
# -------------------------
st.subheader("📌 Customer Details")

selected_customer = st.selectbox(
    "Select a customer to view details:",
    df["Customer"]
)

customer_data = df[df["Customer"] == selected_customer].iloc[0]

st.write("### Basic Details")

col1, col2, col3 = st.columns([1, 2, 2])





# LEFT COLUMN — Customer + CSM
with col1:
    st.write(f"**Customer:** {selected_customer}")
    st.write(f"**Customer Success Manager:** {customer_data['CSM']}")

# MIDDLE COLUMN — ARR (bigger and bold)
with col2:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <div style="font-size: 18px; font-weight: bold; color: #555;">
                ARR
            </div>
            <div style="font-size: 26px; font-weight: 600; margin-top: 4px;">
                ${customer_data['ARR']:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



# RIGHT COLUMN — Contact Info
with col3:
    st.write("**Contact Information**")
    st.write(f"📧 {customer_data['Email']}")
    st.write(f"📞 {customer_data['Phone']}")
    st.write(f"📍 {customer_data['Address']}")


# -------------------------
# 📊 Update Health Score with sliders + Save button
# -------------------------
st.subheader("📊 Update Health Score")

st.write(
    f"Current stored Health Score for **{selected_customer}**: "
    f"**{customer_data['Health Score']:.1f} / 10**"
)

usage = st.slider("Product Usage Level", 1.0, 10.0, 5.0, 0.1)
st.caption("How actively the customer uses the platform day-to-day (1 = barely using it, 10 = heavy, consistent usage).")

tickets = st.slider("Support Ticket Load (higher = worse)", 0.0, 10.0, 2.0, 0.1)
st.caption("How heavy their support demand is (0 = no issues, 10 = constant high-volume issues or escalations).")

nps = st.slider("NPS Score (1–10 simplified)", 1.0, 10.0, 7.0, 0.1)
st.caption("How likely they are to recommend the product (1 = very unhappy, 10 = strong promoter).")

new_score = round((usage * 0.5) + ((10 - tickets) * 0.3) + (nps * 0.2), 1)

st.write(f"Proposed new Health Score: **{new_score:.1f} / 10**")

save_clicked = st.button("💾 Save updated health score")

if save_clicked:
    st.session_state.df.loc[
        st.session_state.df["Customer"] == selected_customer,
        "Health Score"
    ] = new_score
    st.success(f"Saved new health score of {new_score:.1f} for {selected_customer}")

# -------------------------
# 📌 Customer Summary (reflects saved score)
# -------------------------
st.subheader("📌 Customer Summary")

updated_data = st.session_state.df[
    st.session_state.df["Customer"] == selected_customer
].iloc[0]

st.metric(
    "Latest Health Score",
    f"{updated_data['Health Score']:.1f} / 10"
)

# -------------------------
# 📝 Client Notes (saved per customer)
# -------------------------
st.subheader("📝 Client Notes")

existing_note = st.session_state.notes.get(selected_customer, "")

note_input = st.text_area(
    f"Notes for {selected_customer}",
    value=existing_note,
    height=150
)

notes_saved = st.button("💾 Save notes")

if notes_saved:
    st.session_state.notes[selected_customer] = note_input
    st.success(f"Notes saved for {selected_customer}")



