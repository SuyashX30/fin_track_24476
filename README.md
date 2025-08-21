# fin_track_24476

📌 README – FinTrack (Finance Professional CRUD App)
📖 Overview

FinTrack is a CRUD (Create, Read, Update, Delete) application built for finance professionals to manage clients, financial transactions, and investment portfolios.

The application is built with:

Python (Streamlit) → User Interface

PostgreSQL → Database

psycopg2 → Database connection

It provides an easy-to-use UI for performing all CRUD operations, along with basic dashboard analytics such as client portfolio summaries and transaction history.

⚙️ Features

Client Management

Add, update, delete clients

View client details

Transactions Management

Record credits and debits

Filter by client, date, type, or category

Track income vs. expenses

Investments Management

Add different asset classes (Equity, Bonds, Mutual Funds, FD, etc.)

Track invested amount vs. current value

Visualize portfolio allocation

Dashboard

View total clients, total investments, and transaction summaries

Charts for cash flow and portfolio distribution

🗄 Database Schema

The application uses PostgreSQL.
Run the following SQL schema in pgAdmin or psql before starting the app:

CREATE DATABASE fintrack_db;

\c fintrack_db;

-- Clients
CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    company VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transactions
CREATE TABLE transactions (
    txn_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    txn_date DATE NOT NULL,
    txn_type VARCHAR(20) CHECK (txn_type IN ('Credit','Debit')) NOT NULL,
    amount NUMERIC(12,2) CHECK (amount >= 0) NOT NULL,
    category VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_txn_client FOREIGN KEY (client_id)
        REFERENCES clients(client_id) ON DELETE CASCADE
);

-- Investments
CREATE TABLE investments (
    inv_id SERIAL PRIMARY KEY,
    client_id INT NOT NULL,
    asset_type VARCHAR(50) NOT NULL,
    invested_amount NUMERIC(12,2) CHECK (invested_amount >= 0),
    current_value NUMERIC(12,2) CHECK (current_value >= 0),
    start_date DATE,
    maturity_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inv_client FOREIGN KEY (client_id)
        REFERENCES clients(client_id) ON DELETE CASCADE
);

📦 Installation & Setup
1. Clone the repository
git clone https://github.com/yourusername/fintrack.git
cd fintrack

2. Install dependencies

Make sure you have Python 3.9+ and PostgreSQL installed.
Then install the required Python libraries:

pip install streamlit psycopg2 pandas matplotlib

3. Configure database

Edit backend.py with your PostgreSQL connection details:

conn = psycopg2.connect(
    host="localhost",
    database="fintrack_db",
    user="your_username",
    password="your_password"
)

4. Run the app
streamlit run frontend.py

🚀 Usage

Launch the Streamlit app.

Navigate between Clients, Transactions, Investments, and Dashboard.

Perform CRUD operations directly from the UI.

Analyze transaction history and portfolio distribution.

📌 Future Enhancements

Authentication (multi-user support)

Export reports (CSV, Excel, PDF)

Expense categorization with AI suggestions

More advanced analytics (e.g., CAGR, IRR, Risk analysis)

📜 License

This project is licensed under the MIT License.

👉 Would you like me to also create sample dummy data (INSERT statements) for clients, transactions, and investments, so you can test the app right after running the schema?
