import mysql.connector
import joblib
import pandas as pd # Needed to fix the warning

# CONFIG
db_config = { 'host': 'localhost', 'user': 'root', 'passwd': '1234', 'database': 'bank_kaggle_db' }

# LOAD BRAIN
try:
    model = joblib.load('kaggle_brain.pkl')
    print(">> Balanced AI Brain Loaded.")
except:
    print("Error: Run 'train_kaggle_model.py' first!")
    exit()

print("\n--- UNIVERSAL BANK LOAN SYSTEM ---")
c_id = int(input("Enter New Customer ID: "))
zip_c = int(input("Enter Zip Code: "))
income = float(input("Enter Annual Income (in $000s): ")) 
cc_avg = float(input("Enter Avg Credit Card Spending (in $000s): ")) 
mortgage = float(input("Enter Mortgage Value (in $000s): "))

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

try:
    # 1. Insert Region/Customer/Loan logic...
    cursor.execute(f"INSERT IGNORE INTO Regions (ZipCode, City_Name) VALUES ({zip_c}, 'New City')")
    cursor.execute("INSERT INTO Customers (Customer_ID, ZipCode, Age, Experience, Family_Size, Education_Level) VALUES (%s, %s, 30, 5, 2, 1)", (c_id, zip_c))
    cursor.execute("INSERT INTO Loan_History (Customer_ID, Income_Annual, CC_Avg, Mortgage_Value, Personal_Loan_Status) VALUES (%s, %s, %s, %s, NULL)", (c_id, income, cc_avg, mortgage))
    loan_id = cursor.lastrowid 
    conn.commit()

    # 2. PREDICT (The Fixed Way)
    # We create a tiny DataFrame so the model sees the column names it expects
    input_data = pd.DataFrame([[income, cc_avg, mortgage]], columns=['Income_Annual', 'CC_Avg', 'Mortgage_Value'])
    
    prediction = model.predict(input_data)[0]
    
    result = "APPROVED (Safe)" if prediction == 1 else "REJECTED (Risky)"
    print(f"\n>> AI DECISION: {result}")

    # 3. UPDATE
    cursor.execute("UPDATE Loan_History SET AI_Prediction = %s WHERE Loan_ID = %s", (int(prediction), loan_id))
    conn.commit()
    print(">> Database Updated.")

except Exception as e:
    print(f"Error: {e}")

conn.close()