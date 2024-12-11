import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid


# Database setup
def setup_database():
    conn = sqlite3.connect('financial_ecosystem.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS clients
                 (id TEXT PRIMARY KEY,
                  name TEXT,
                  address TEXT,
                  phone_number TEXT,
                  income INTEGER,
                  credit_score INTEGER,
                  created_at TIMESTAMP,
                  updated_at TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS companies
                 (id TEXT PRIMARY KEY,
                  name TEXT,
                  type INTEGER,
                  created_at TIMESTAMP,
                  updated_at TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS financial_products
                 (id TEXT PRIMARY KEY,
                  company_id TEXT,
                  type TEXT,
                  interest_rate REAL,
                  loan_term INTEGER,
                  created_at TIMESTAMP,
                  updated_at TIMESTAMP,
                  FOREIGN KEY (company_id) REFERENCES companies(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id TEXT PRIMARY KEY,
                  client_id TEXT,
                  amount INTEGER,
                  category TEXT,
                  created_at TIMESTAMP,
                  FOREIGN KEY (client_id) REFERENCES clients(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS financial_transactions_attributes
                 (transaction_id TEXT PRIMARY KEY,
                  financial_product_id TEXT,
                  type TEXT,
                  FOREIGN KEY (transaction_id) REFERENCES transactions(id),
                  FOREIGN KEY (financial_product_id) REFERENCES financial_products(id))''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS account_transactions_attributes
                 (transaction_id TEXT PRIMARY KEY,
                  company_id TEXT,
                  type TEXT,
                  FOREIGN KEY (transaction_id) REFERENCES transactions(id),
                  FOREIGN KEY (company_id) REFERENCES companies(id))''')
    
    conn.commit()
    return conn


def generate_dummy_data():
    conn = setup_database()
    c = conn.cursor()
    
    # Clear existing data
    tables = ['account_transactions_attributes', 'financial_transactions_attributes', 
              'transactions', 'financial_products', 'companies', 'clients']
    for table in tables:
        c.execute(f'DELETE FROM {table}')
    
    current_time = datetime.now()
    
    # Generate companies
    company_types = {
        'Bank': 1,
        'Digital Payment': 2,
        'Fintech': 3,
        'Insurance': 4
    }
    
    companies = [
        ('BCA', 'Bank'), ('Mandiri', 'Bank'),
        ('GoPay', 'Digital Payment'), ('OVO', 'Digital Payment'),
        ('Akulaku', 'Fintech'), ('Kredivo', 'Fintech'),
        ('AIA', 'Insurance'), ('Astra Life', 'Insurance')
    ]
    
    company_ids = {}
    for name, type_ in companies:
        company_id = str(uuid.uuid4())
        company_ids[name] = company_id
        c.execute('''INSERT INTO companies 
                     (id, name, type, created_at, updated_at) 
                     VALUES (?, ?, ?, ?, ?)''',
                 (company_id, name, company_types[type_], 
                  current_time, current_time))
    
    # Generate financial products
    products = [
        ('Personal Loan', 'BCA', 12.5, 12),
        ('Business Loan', 'Mandiri', 10.0, 24),
        ('Quick Loan', 'Akulaku', 15.0, 6),
        ('Credit Line', 'Kredivo', 18.0, 12)
    ]
    
    product_ids = {}
    for name, company, rate, term in products:
        product_id = str(uuid.uuid4())
        product_ids[name] = product_id
        c.execute('''INSERT INTO financial_products 
                     (id, company_id, type, interest_rate, loan_term, 
                      created_at, updated_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (product_id, company_ids[company], name, rate, term,
                  current_time, current_time))
    
    # Generate clients
    addresses = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang']
    client_ids = []
    for i in range(1, 21):
        client_id = str(uuid.uuid4())
        client_ids.append(client_id)
        
        c.execute('''INSERT INTO clients 
                     (id, name, address, phone_number, income, 
                      credit_score, created_at, updated_at) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (client_id, f"Client {i}", 
                  random.choice(addresses),
                  f"+62812{random.randint(10000000, 99999999)}",
                  random.randint(5000000, 50000000),
                  random.randint(0, 1000),
                  current_time, current_time))
    
    # Generate transactions and their attributes
    transaction_categories = ['Payment', 'Transfer', 'Loan', 'Investment']
    account_transaction_types = ['Purchase', 'Bill Payment', 'Transfer']
    financial_transaction_types = ['Loan Disbursement', 'Loan Payment', 'Investment']
    
    start_date = current_time - timedelta(days=365)
    
    for client_id in client_ids:
        # Generate account transactions
        num_account_transactions = random.randint(50, 200)
        for _ in range(num_account_transactions):
            transaction_id = str(uuid.uuid4())
            transaction_date = start_date + timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            
            # Create base transaction
            c.execute('''INSERT INTO transactions 
                         (id, client_id, amount, category, created_at) 
                         VALUES (?, ?, ?, ?, ?)''',
                     (transaction_id, client_id,
                      random.randint(50000, 5000000),
                      'Account',
                      transaction_date))
            
            # Create account transaction attributes
            company = random.choice(list(company_ids.keys()))
            c.execute('''INSERT INTO account_transactions_attributes 
                         (transaction_id, company_id, type) 
                         VALUES (?, ?, ?)''',
                     (transaction_id, company_ids[company],
                      random.choice(account_transaction_types)))
        
        # Generate financial transactions
        num_financial_transactions = random.randint(1, 5)
        for _ in range(num_financial_transactions):
            transaction_id = str(uuid.uuid4())
            transaction_date = start_date + timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )
            
            # Create base transaction
            c.execute('''INSERT INTO transactions 
                         (id, client_id, amount, category, created_at) 
                         VALUES (?, ?, ?, ?, ?)''',
                     (transaction_id, client_id,
                      random.randint(5000000, 50000000),
                      'Financial',
                      transaction_date))
            
            # Create financial transaction attributes
            product = random.choice(list(product_ids.keys()))
            c.execute('''INSERT INTO financial_transactions_attributes 
                         (transaction_id, financial_product_id, type) 
                         VALUES (?, ?, ?)''',
                     (transaction_id, product_ids[product],
                      random.choice(financial_transaction_types)))
    
    conn.commit()
    conn.close()


def add_random_transaction(client_id):
    conn = sqlite3.connect('financial_ecosystem.db')
    c = conn.cursor()
    
    current_time = datetime.now()
    transaction_id = str(uuid.uuid4())
    
    # Random transaction type (Account or Financial)
    transaction_type = random.choice(['Account', 'Financial'])
    
    if transaction_type == 'Account':
        amount = random.randint(50000, 5000000)
        c.execute('''INSERT INTO transactions 
                     (id, client_id, amount, category, created_at) 
                     VALUES (?, ?, ?, ?, ?)''',
                 (transaction_id, client_id, amount, 'Account', current_time))
        
        # Get random company
        c.execute('SELECT id FROM companies WHERE type IN (1, 2)')  # Banks and Digital Payment
        companies = c.fetchall()
        company_id = random.choice(companies)[0]
        
        # Create account transaction attributes
        transaction_types = ['Purchase', 'Bill Payment', 'Transfer']
        c.execute('''INSERT INTO account_transactions_attributes 
                     (transaction_id, company_id, type) 
                     VALUES (?, ?, ?)''',
                 (transaction_id, company_id, random.choice(transaction_types)))
    
    else:  # Financial transaction
        amount = random.randint(5000000, 50000000)
        c.execute('''INSERT INTO transactions 
                     (id, client_id, amount, category, created_at) 
                     VALUES (?, ?, ?, ?, ?)''',
                 (transaction_id, client_id, amount, 'Financial', current_time))
        
        # Get random financial product
        c.execute('SELECT id FROM financial_products')
        products = c.fetchall()
        product_id = random.choice(products)[0]
        
        # Create financial transaction attributes
        transaction_types = ['Loan Disbursement', 'Loan Payment', 'Investment']
        c.execute('''INSERT INTO financial_transactions_attributes 
                     (transaction_id, financial_product_id, type) 
                     VALUES (?, ?, ?)''',
                 (transaction_id, product_id, random.choice(transaction_types)))
    
    conn.commit()
    conn.close()


def update_credit_score(client_id, new_score):
    """Update client's credit score in the database"""
    conn = sqlite3.connect('financial_ecosystem.db')
    c = conn.cursor()
    
    current_time = datetime.now()
    
    c.execute('''UPDATE clients 
                 SET credit_score = ?, 
                     updated_at = ?
                 WHERE id = ?''',
             (int(new_score), current_time, client_id))
    
    conn.commit()
    conn.close()


def calculate_transaction_score(transactions_df):
    if len(transactions_df) == 0:
        return 0
    
    # Calculate frequency score (0-40 points)
    max_freq = 200  # Maximum expected transactions
    freq_score = min(400, (len(transactions_df) / max_freq) * 400)
    
    # Calculate value score (0-40 points)
    avg_value = transactions_df['amount'].mean()
    max_value = 5000000  # Expected maximum average transaction
    value_score = min(400, (avg_value / max_value) * 400)
    
    # Calculate consistency score (0-20 points)
    dates = pd.to_datetime(transactions_df['created_at'])
    date_diffs = dates.diff().dt.days.dropna()
    consistency_score = 200 if len(date_diffs) > 0 else 0
    if len(date_diffs) > 0:
        avg_gap = date_diffs.mean() * -1
        consistency_score = min(200, (30 / avg_gap) * 200)
    
    # print(consistency_score)

    return freq_score + value_score + consistency_score


def calculate_income_score(income):
    # Base score on income brackets (0-100 points)
    if income >= 40000000:  # Above 40M
        return 1000
    elif income >= 30000000:  # 30M-40M
        return 800
    elif income >= 20000000:  # 20M-30M
        return 600
    elif income >= 10000000:  # 10M-20M
        return 400
    else:  # Below 10M
        return 200


def get_credit_score(client_id):
    conn = sqlite3.connect('financial_ecosystem.db')
    
    # Get transactions
    transactions_df = pd.read_sql_query('''
        SELECT t.*, ata.type as account_type, fta.type as financial_type
        FROM transactions t
        LEFT JOIN account_transactions_attributes ata ON t.id = ata.transaction_id
        LEFT JOIN financial_transactions_attributes fta ON t.id = fta.transaction_id
        WHERE t.client_id = ?
        ORDER BY created_at DESC
    ''', conn, params=(client_id,))
    
    # Get client info
    client_df = pd.read_sql_query(
        'SELECT * FROM clients WHERE id = ?', 
        conn, params=(client_id,)
    )
    
    conn.close()
    
    # Calculate scores
    transaction_score = calculate_transaction_score(transactions_df)
    income_score = calculate_income_score(client_df['income'].iloc[0])
    
    # Weighted combination (60% transactions, 40% income)
    final_score = (0.6 * transaction_score) + (0.4 * income_score)
    
    return final_score, transactions_df, client_df


def get_risk_category(score):
    if 750 <= score <= 1000:
        risk = 'Kolektibilitas 1 - Lancar (Resiko Rendah)'
    elif 650 <= score <= 749:
        risk = 'Kolektibilitas 2 - Dalam Perhatian Khusus'
    elif 550 <= score <= 649:
        risk = 'Kolektibilitas 3 - Kurang Lancar'
    elif 450 <= score <= 549:
        risk = 'Kolektibilitas 4 - Diragukan'
    else:
        risk = 'Kolektibilitas 5 - Macet (Resiko Tinggi)'
    
    return risk


def main():
    st.title('Credit Scoring Simulation')
    
    # Initialize database and generate data if needed
    if st.button('Generate New Dummy Data'):
        generate_dummy_data()
        st.success('New dummy data generated successfully!')
    
    # Get client list
    conn = sqlite3.connect('financial_ecosystem.db')
    clients_df = pd.read_sql_query('SELECT * FROM clients', conn)
    conn.close()
    
    # Display client list with credit scores
    st.header('Client List')
    
    # Create a DataFrame with client info and credit scores
    client_scores = []
    for _, client in clients_df.iterrows():
        client_scores.append({
            'Name': client['name'],
            'Address': client['address'],
            'Income': f"Rp {client['income']:,.2f}",
            'Credit Score': client['credit_score'],
            'Risk Category': get_risk_category(client['credit_score'])
        })
    
    clients_summary_df = pd.DataFrame(client_scores)
    st.dataframe(clients_summary_df)

    # Client selection for detailed view
    st.header('Detailed Client Analysis')
    selected_client = st.selectbox(
        'Select Client:',
        clients_df['name'].tolist()
    )
    
    client_id = clients_df[clients_df['name'] == selected_client]['id'].iloc[0]
    
    # Add button to generate random transaction
    if st.button('Add Random Transaction'):
        add_random_transaction(client_id)
        st.success('New transaction added successfully!')

    if st.button('Check Credit Score'):
        score, transactions_df, client_df = get_credit_score(client_id)
        update_credit_score(client_id, score)
        
        # Display results
        st.header('Credit Score Analysis')
        
        # Score display with color coding
        if 750 <= score <= 1000:
            score_color = '#4CAF50'
        elif 650 <= score <= 749:
            score_color = '#FFC107'
        elif 550 <= score <= 649:
            score_color = '#FF9800'
        elif 450 <= score <= 549:
            score_color = '#FF5722'
        else:
            score_color = '#F44336'

        st.markdown(
            f'<h1 style="color: {score_color};">{int(score)}</h1>', 
            unsafe_allow_html=True
        )
        
        # Risk
        st.subheader('Risk')
        st.markdown(
            f'<h5 style="color: {score_color};">{get_risk_category(score)}</h5>', 
            unsafe_allow_html=True
        )

        # Client summary
        st.subheader('Client Summary')
        st.write(f"Name: {client_df['name'].iloc[0]}")
        st.write(f"Address: {client_df['address'].iloc[0]}")
        st.write(f"Phone: {client_df['phone_number'].iloc[0]}")
        st.write(f"Monthly Income: Rp {client_df['income'].iloc[0]:,.2f}")
        st.write(f"Current Credit Score: {client_df['credit_score'].iloc[0]}")
        
        # Transaction summary
        st.subheader('Transaction Summary')
        st.write(f"Total Transactions: {len(transactions_df)}")
        if len(transactions_df) > 0:
            st.write(
                f"Average Transaction Value: Rp "
                f"{transactions_df['amount'].mean():,.2f}"
            )
            st.write(
                f"Total Transaction Value: Rp "
                f"{transactions_df['amount'].sum():,.2f}"
            )
            
            # Transaction history chart
            st.subheader('Transaction History')
            transactions_df['created_at'] = pd.to_datetime(
                transactions_df['created_at']
            )
            transactions_df = transactions_df.sort_values('created_at')
            
            # Line chart of transaction amounts over time
            st.line_chart(
                transactions_df.set_index('created_at')['amount']
            )
            
            # Transaction type distribution
            st.subheader('Transaction Type Distribution')
            # Combine account and financial types
            transactions_df['type'] = transactions_df['account_type'].fillna(
                transactions_df['financial_type']
            )
            type_counts = transactions_df['type'].value_counts()
            st.bar_chart(type_counts)

if __name__ == '__main__':
    main()
    