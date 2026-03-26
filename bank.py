import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="NeoBank", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Title */
.title {
    font-size: 3rem;
    font-weight: 800;
    text-align:center;
    background: linear-gradient(90deg,#6366f1,#ec4899);
    -webkit-background-clip:text;
    color:transparent;
    margin-bottom: 20px;
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:15px;
    border:1px solid rgba(255,255,255,0.1);
    text-align:center;
}

/* Balance */
.balance {
    font-size:2.2rem;
    font-weight:bold;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg,#6366f1,#ec4899);
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 20px;
    font-weight:bold;
}

/* Inputs */
.stTextInput input, .stNumberInput input {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------- BACKEND ----------
class Bank:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.transactions = []
        self.card = " ".join([str(random.randint(1000,9999)) for _ in range(4)])

    def transact(self, t, amt, cat):
        if t == "Withdraw" and amt > self.balance:
            return False

        if t == "Deposit":
            self.balance += amt
        else:
            self.balance -= amt

        self.transactions.append({
            "Type": t,
            "Amount": amt,
            "Category": cat,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Balance": self.balance
        })
        return True

    def get_df(self):
        return pd.DataFrame(self.transactions)

# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------- TITLE ----------
st.markdown('<div class="title">🚀 NeoBank</div>', unsafe_allow_html=True)

# ---------- LOGIN PAGE ----------
if not st.session_state.user:

    st.subheader("Create Your Account")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Enter Name")

    with col2:
        balance = st.number_input("Initial Balance", min_value=0)

    if st.button("Create Account"):
        if name.strip():
            st.session_state.user = Bank(name, balance)
            st.success("✅ Account Created Successfully!")
            st.rerun()
        else:
            st.error("⚠️ Please enter your name")

# ---------- DASHBOARD ----------
else:
    user = st.session_state.user

    st.subheader(f"Welcome, {user.name} 👋")

    # ---------- TOP CARDS ----------
    c1, c2, c3 = st.columns(3)

    c1.markdown(f"""
    <div class='card'>
        💰 Balance
        <div class='balance'>₹{user.balance}</div>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class='card'>
        📊 Transactions
        <div class='balance'>{len(user.transactions)}</div>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class='card'>
        💳 Card Number
        <div class='balance'>{user.card}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ---------- TRANSACTION ----------
    st.subheader("💸 Make a Transaction")

    col1, col2, col3 = st.columns(3)

    t = col1.selectbox("Transaction Type", ["Deposit", "Withdraw"])
    amt = col2.number_input("Amount", min_value=1)
    cat = col3.selectbox("Category", ["Food", "Shopping", "Bills", "Travel", "Other"])

    if st.button("Proceed Transaction"):
        success = user.transact(t, amt, cat)

        if success:
            st.success("✅ Transaction Successful")
        else:
            st.error("❌ Insufficient Balance")

    st.divider()

    # ---------- DATA ----------
    df = user.get_df()

    if not df.empty:

        # ---------- BALANCE TREND ----------
        st.subheader("📈 Balance Trend")
        df_chart = df.copy()
        df_chart["Time"] = pd.to_datetime(df_chart["Time"])
        df_chart = df_chart.set_index("Time")
        st.line_chart(df_chart["Balance"])

        # ---------- CATEGORY SUMMARY ----------
        st.subheader("📊 Spending Summary")
        spend = df[df["Type"] == "Withdraw"].groupby("Category")["Amount"].sum()
        st.bar_chart(spend)

        # ---------- TABLE ----------
        st.subheader("📋 Transaction History")
        st.dataframe(df, use_container_width=True)

    else:
        st.info("No transactions yet...")

    # ---------- LOGOUT ----------
    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()