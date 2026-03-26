import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="NeoBank 🏦", layout="wide")

# ---------- TARGETED COLOR CSS ----------
st.markdown("""
<style>
/* Base Theme */
.stApp {
    background-color: #0d1117;
    color: #ffffff;
}

/* Force visibility on Selectbox (Action & Category) */
div[data-baseweb="select"] > div {
    background-color: #1f2937 !important; /* Dark grey-blue background */
    border: 2px solid #3b82f6 !important; /* Bright blue border */
    border-radius: 10px !important;
}

/* Text inside the dropdowns */
div[data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Label colors for Action and Category */
label[data-testid="stWidgetLabel"] {
    color: #00d4ff !important; /* Neon blue labels */
    font-size: 1.1rem !important;
    font-weight: 700 !important;
}

/* Card Styling */
.card {
    background-color: #161b22;
    padding: 1.5rem;
    border-radius: 15px;
    border: 1px solid #30363d;
    margin-bottom: 1rem;
}

/* Highlight specific values */
.balance { color: #22c55e !important; font-size: 2rem; font-weight: 800; }
.card-number { color: #eab308 !important; letter-spacing: 2px; font-weight: 700; }

/* Button Visibility */
.stButton>button {
    background-image: linear-gradient(to right, #2563eb, #7c3aed) !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- BACKEND ----------
if "user" not in st.session_state:
    st.session_state.user = None

class Bank:
    def __init__(self, name, balance):
        self.name, self.balance = name, float(balance)
        self.transactions = []
        self.card = " ".join([f"{random.randint(1000, 9999):04}" for _ in range(4)])

    def transact(self, t, amt, cat):
        amt = float(amt)
        if t == "Withdraw" and amt > self.balance: return False
        self.balance += amt if t == "Deposit" else -amt
        self.transactions.append({"Type": t, "Amount": amt, "Category": cat, "Balance": self.balance})
        return True

# ---------- UI ----------
st.title("🏦 NeoBank")

if not st.session_state.user:
    st.subheader("Create Your Account")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        name = st.text_input("Full Name")
        bal = st.number_input("Initial Deposit", min_value=0.0, value=1000.0)
        if st.button("Get Started"):
            if name: 
                st.session_state.user = Bank(name, bal)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
else:
    u = st.session_state.user
    
    # Top Metrics
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="card">Wallet Balance<br><span class="balance">₹{u.balance:,.2f}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card">Card Number<br><span class="card-number">{u.card}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card">Transactions<br><span style="font-size:2rem; color:#3b82f6;">{len(u.transactions)}</span></div>', unsafe_allow_html=True)

    # Transaction Form (The section you wanted changed)
    st.markdown("### 💸 Move Money")
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col_action, col_amt, col_cat = st.columns(3)
        
        # Action Dropdown
        t_type = col_action.selectbox("Choose Action", ["Deposit", "Withdraw"], help="Select the type of movement")
        
        # Amount Input
        t_amt = col_amt.number_input("Enter Amount (₹)", min_value=1.0)
        
        # Category Dropdown
        t_cat = col_cat.selectbox("Select Category", ["Food & Dining", "Shopping", "Utility Bills", "Travel", "Personal Care", "Investment"])
        
        if st.button("Confirm Transfer", use_container_width=True):
            if u.transact(t_type, t_amt, t_cat):
                st.toast(f"{t_type} successful!", icon="✅")
                st.rerun()
            else:
                st.error("Insufficient Funds!")
        st.markdown('</div>', unsafe_allow_html=True)

    # History Table
    if u.transactions:
        st.markdown("### 📋 History")
        st.dataframe(pd.DataFrame(u.transactions), use_container_width=True)

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()