import psycopg2
import pandas as pd

# ------------------ DB CONNECTION ------------------
def get_connection():
    return psycopg2.connect(
        host="localhost",
        dbname="FinTrack",
        user="postgres",
        password="root",
        port="5432"
    )

# ------------------ CLIENTS CRUD ------------------
def add_client(name, email, phone, company):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO clients (name, email, phone, company) VALUES (%s, %s, %s, %s)",
                (name, email, phone, company))
    conn.commit()
    cur.close()
    conn.close()

def view_clients():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM clients ORDER BY client_id", conn)
    conn.close()
    return df

# ------------------ TRANSACTIONS CRUD ------------------
def add_transaction(client_id, txn_date, txn_type, amount, category, notes):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transactions (client_id, txn_date, txn_type, amount, category, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (client_id, txn_date, txn_type, amount, category, notes))
    conn.commit()
    cur.close()
    conn.close()

def view_transactions():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT t.txn_id, c.name AS client, t.txn_date, t.txn_type, t.amount, t.category, t.notes
        FROM transactions t
        JOIN clients c ON t.client_id = c.client_id
        ORDER BY t.txn_date DESC
    """, conn)
    conn.close()
    return df

# ------------------ INVESTMENTS CRUD ------------------
def add_investment(client_id, asset_type, invested_amount, current_value, start_date, maturity_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO investments (client_id, asset_type, invested_amount, current_value, start_date, maturity_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (client_id, asset_type, invested_amount, current_value, start_date, maturity_date))
    conn.commit()
    cur.close()
    conn.close()

def view_investments():
    conn = get_connection()
    df = pd.read_sql("""
        SELECT i.inv_id, c.name AS client, i.asset_type, i.invested_amount, i.current_value, 
               i.start_date, i.maturity_date
        FROM investments i
        JOIN clients c ON i.client_id = c.client_id
        ORDER BY i.start_date DESC
    """, conn)
    conn.close()
    return df
