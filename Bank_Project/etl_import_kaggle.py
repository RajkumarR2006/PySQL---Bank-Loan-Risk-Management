import mysql.connector
import pandas as pd
import random

# --- CONFIGURATION ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '1234',  # <--- PUT YOUR MYSQL PASSWORD HERE
    'database': 'bank_kaggle_db' # New database name
}

csv_filename = 'UniversalBank.csv'

# 1. READ KAGGLE DATA
print(">> Reading CSV file...")
try:
    # We drop ID column from CSV because we will make our own
    df = pd.read_csv(csv_filename)
    print(f">> CSV Loaded. Found {len(df)} rows.")
except FileNotFoundError:
    print(f"Error: Could not find '{csv_filename}'. Did you download it?")
    exit()

# 2. CONNECT TO MYSQL
conn = mysql.connector.connect(host=db_config['host'], user=db_config['user'], passwd=db_config['passwd'])
cursor = conn.cursor()

# 3. CREATE DATABASE & TABLES
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
cursor.execute(f"USE {db_config['database']}")

# Clean start
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("DROP TABLE IF EXISTS Loan_History")
cursor.execute("DROP TABLE IF EXISTS Customers")
cursor.execute("DROP TABLE IF EXISTS Regions")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

# Table 1: Regions (Derived from ZIP Code)
cursor.execute("""
CREATE TABLE Regions (
    ZipCode INT PRIMARY KEY,
    City_Name VARCHAR(50),
    Region_Code VARCHAR(10)
)
""")

# Table 2: Customers (Linked to Region)
cursor.execute("""
CREATE TABLE Customers (
    Customer_ID INT PRIMARY KEY,
    Age INT,
    Experience INT,
    Family_Size INT,
    Education_Level INT,
    ZipCode INT,
    FOREIGN KEY (ZipCode) REFERENCES Regions(ZipCode)
)
""")

# Table 3: Loan_History (Financials + The Decision)
cursor.execute("""
CREATE TABLE Loan_History (
    Loan_ID INT AUTO_INCREMENT PRIMARY KEY,
    Customer_ID INT,
    Income_Annual FLOAT,
    CC_Avg FLOAT,
    Mortgage_Value FLOAT,
    Personal_Loan_Status INT, -- 0 = Reject, 1 = Accept
    AI_Prediction INT,        -- NULL initially
    FOREIGN KEY (Customer_ID) REFERENCES Customers(Customer_ID)
)
""")

print(">> Database Schema Created.")

# 4. PROCESS & INSERT DATA
# This loop simulates a real ETL process
print(">> Importing data (This might take 10-20 seconds)...")

# Sets to track duplicates
unique_zips = set()
region_data = []
customer_data = []
loan_data = []

for index, row in df.iterrows():
    # KAGGLE COLUMN MAPPING (Adjust these names if your CSV is slightly different)
    # Usually: ID, Age, Experience, Income, ZIP Code, Family, CCAvg, Education, Mortgage, Personal Loan
    
    c_id = int(row['ID'])
    zip_code = int(row['ZIP Code'])
    
    # Handle Regions (Only insert unique Zips)
    if zip_code not in unique_zips:
        unique_zips.add(zip_code)
        # We fake the city name because the CSV doesn't have it
        region_data.append((zip_code, f"City_{zip_code}", "USA"))

    # Handle Customer
    customer_data.append((
        c_id, 
        int(row['Age']), 
        int(row['Experience']), 
        int(row['Family']), 
        int(row['Education']), 
        zip_code
    ))

    # Handle Loan History
    loan_data.append((
        c_id, 
        float(row['Income']), # Usually in thousands
        float(row['CCAvg']), 
        float(row['Mortgage']), 
        int(row['Personal Loan']) # The Target
    ))

# BULK INSERT (Much faster than row-by-row)
print(">> Writing to MySQL...")

cursor.executemany("INSERT INTO Regions (ZipCode, City_Name, Region_Code) VALUES (%s, %s, %s)", region_data)
cursor.executemany("INSERT INTO Customers (Customer_ID, Age, Experience, Family_Size, Education_Level, ZipCode) VALUES (%s, %s, %s, %s, %s, %s)", customer_data)

# Note: We let Loan_ID auto-increment, AI_Prediction is NULL
cursor.executemany("INSERT INTO Loan_History (Customer_ID, Income_Annual, CC_Avg, Mortgage_Value, Personal_Loan_Status) VALUES (%s, %s, %s, %s, %s)", loan_data)

conn.commit()
conn.close()

print(f"SUCCESS! Imported {len(customer_data)} customers into database '{db_config['database']}'.")