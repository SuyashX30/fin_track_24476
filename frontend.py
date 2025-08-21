import streamlit as st
import pandas as pd
import backend as db
import plotly.express as px

st.set_page_config(page_title="FinTrack", layout="wide")
st.title("📊 FinTrack - Finance Management App")

menu = ["Dashboard", "Clients", "Transactions", "Investments"]
choice = st.sidebar.radio("Navigate", menu)

# ------------------ DASHBOARD ------------------
if choice == "Dashboard":
    st.subheader("📈 Finance Dashboard")

    clients = db.view_clients()
    txns = db.view_transactions()
    invs = db.view_investments()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients", len(clients))
    col2.metric("Total Transactions", len(txns))
    col3.metric("Total Investments", len(invs))

    if not txns.empty:
        st.write("### Transaction Trends")
        fig = px.histogram(txns, x="txn_date", y="amount", color="txn_type",
                           title="Cash Inflows & Outflows Over Time")
        st.plotly_chart(fig, use_container_width=True)

    if not invs.empty:
        st.write("### Investment Distribution")
        fig2 = px.pie(invs, names="asset_type", values="current_value", title="Portfolio Allocation")
        st.plotly_chart(fig2, use_container_width=True)

# ------------------ CLIENTS ------------------
elif choice == "Clients":
    st.subheader("👥 Manage Clients")
    with st.form("client_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        company = st.text_input("Company")
        submitted = st.form_submit_button("Add Client")
        if submitted:
            db.add_client(name, email, phone, company)
            st.success(f"Client {name} added!")

    st.write("### All Clients")
    st.dataframe(db.view_clients())

# ------------------ TRANSACTIONS ------------------
elif choice == "Transactions":
    st.subheader("💰 Manage Transactions")
    clients = db.view_clients()

    with st.form("txn_form"):
        client_id = st.selectbox("Select Client", clients["client_id"].tolist(), 
                                 format_func=lambda x: clients.loc[clients["client_id"]==x,"name"].values[0])
        txn_date = st.date_input("Date")
        txn_type = st.radio("Type", ["Credit", "Debit"])
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        category = st.text_input("Category")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Transaction")
        if submitted:
            db.add_transaction(client_id, txn_date, txn_type, amount, category, notes)
            st.success("Transaction added!")

    st.write("### All Transactions")
    st.dataframe(db.view_transactions())

# ------------------ INVESTMENTS ------------------
elif choice == "Investments":
    st.subheader("📈 Manage Investments")
    clients = db.view_clients()

    with st.form("inv_form"):
        client_id = st.selectbox("Select Client", clients["client_id"].tolist(),
                                 format_func=lambda x: clients.loc[clients["client_id"]==x,"name"].values[0])
        asset_type = st.selectbox("Asset Type", ["Equity", "Bond", "Mutual Fund", "FD", "Other"])
        invested_amount = st.number_input("Invested Amount", min_value=0.0, step=100.0)
        current_value = st.number_input("Current Value", min_value=0.0, step=100.0)
        start_date = st.date_input("Start Date")
        maturity_date = st.date_input("Maturity Date")
        submitted = st.form_submit_button("Add Investment")
        if submitted:
            db.add_investment(client_id, asset_type, invested_amount, current_value, start_date, maturity_date)
            st.success("Investment added!")

    st.write("### All Investments")
    st.dataframe(db.view_investments())
