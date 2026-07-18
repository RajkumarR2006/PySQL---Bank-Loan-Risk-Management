import mysql.connector
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# CONFIG
db_config = { 'host': 'localhost', 'user': 'root', 'passwd': '1234', 'database': 'bank_kaggle_db' }

conn = mysql.connector.connect(**db_config)

# --- THE FIX IS HERE ---
# We added "WHERE Personal_Loan_Status IS NOT NULL"
# This prevents the AI from trying to learn from the new applicants who have no decision yet.
query = """
    SELECT Income_Annual, CC_Avg, Mortgage_Value, Personal_Loan_Status 
    FROM Loan_History 
    WHERE Personal_Loan_Status IS NOT NULL
"""
df = pd.read_sql(query, conn)
conn.close()

print(f"Training on {len(df)} valid historical records...")

# 2. Prepare
X = df[['Income_Annual', 'CC_Avg', 'Mortgage_Value']]
y = df['Personal_Loan_Status']

# 3. Train with BALANCE (To handle rich people correctly)
model = LogisticRegression(class_weight='balanced', solver='liblinear')
model.fit(X, y)

# 4. Save
joblib.dump(model, 'kaggle_brain.pkl')
print("SUCCESS! Balanced Brain saved.")