import streamlit as st
import pandas as pd
from datetime import datetime
import random
import plotly.express as px

# ---------- CONFIG ----------
st.set_page_config(page_title="NeoBank", layout="wide")

# ---------- CSS ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
}

/* Title */
.title {
    font-size: 3rem;
    font-weight: 800;
    text-align:center;
    background: linear-gradient(90deg,#6366f1,#ec4899);
    -webkit-background-clip:text;
    color:transparent;
}

/* Card */
.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:15px;
    border:1px solid rgba(255,255,255,0.1);
    margin-bottom:10px;
}

/* Balance */
.balance {
    font-size:2.5rem;
    font-weight:bold;
}

/* Button */
.stButton button {
    background: linear-gradient(135deg,#6366f1,#ec4899);
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 20px;
    font-weight:bold;
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
        if t=="Withdraw" and amt>self.balance:
            return False

        self.balance += amt if t=="Deposit" else -amt

        self.transactions.append({
            "type":t,
            "amount":amt,
            "category":cat,
            "time":datetime.now(),
            "balance":self.balance
        })
        return True

    def df(self):
        return pd.DataFrame(self.transactions)

# ---------- SESSION ----------
if "user" not in st.session_state:
    st.session_state.user=None

# ---------- TITLE ----------
st.markdown('<div class="title">🚀 NeoBank</div>', unsafe_allow_html=True)

# ---------- LOGIN ----------
if not st.session_state.user:
    st.subheader("Create Account")

    name = st.text_input("Name")
    bal = st.number_input("Initial Balance",0)

    if st.button("Create Account"):
        if name:
            st.session_state.user = Bank(name, bal)
            st.success("Account Created")
            st.rerun()
        else:
            st.error("Enter name")

# ---------- DASHBOARD ----------
else:
    user = st.session_state.user

    st.subheader(f"Welcome {user.name}")

    # Top Cards
    c1,c2,c3 = st.columns(3)

    c1.markdown(f"<div class='card'>💰 Balance<br><div class='balance'>₹{user.balance}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'>📊 Transactions<br>{len(user.transactions)}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'>💳 Card<br>{user.card}</div>", unsafe_allow_html=True)

    st.divider()

    # Transaction
    st.subheader("Make Transaction")

    col1,col2,col3 = st.columns(3)

    t = col1.selectbox("Type",["Deposit","Withdraw"])
    amt = col2.number_input("Amount",1)
    cat = col3.selectbox("Category",["Food","Shopping","Bills","Travel","Other"])

    if st.button("Proceed"):
        if user.transact(t,amt,cat):
            st.success("Transaction Successful")
        else:
            st.error("Insufficient Balance")

    st.divider()

    # Data
    df = user.df()

    if not df.empty:

        # Chart
        st.subheader("Analytics")

        spend = df[df["type"]=="Withdraw"].groupby("category")["amount"].sum()

        if not spend.empty:
            fig = px.bar(
                x=spend.index,
                y=spend.values,
                labels={'x':'Category','y':'Amount'}
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig,use_container_width=True)

        # Line Chart
        st.subheader("Balance Trend")
        st.line_chart(df.set_index("time")["balance"])

        # Table
        st.subheader("Transactions")
        st.dataframe(df,use_container_width=True)

    else:
        st.info("No transactions yet")

    # Logout
    if st.button("Logout"):
        st.session_state.user=None
        st.rerun()