import mysql.connector
import random
import time

# --- CONFIGURATION ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '1234', # <--- PUT YOUR PASSWORD HERE
    'database': 'bank_project_db'
}

print("--- STARTING PROFESSIONAL DATA GENERATION ---")

# 1. Connect
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print(">> Connected to MySQL.")
except Exception as e:
    print(f"Error: {e}")
    exit()

# 2. CLEAR OLD DATA (Clean Slate)
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("TRUNCATE TABLE Loans")
cursor.execute("TRUNCATE TABLE Customers")
cursor.execute("TRUNCATE TABLE Branches")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
print(">> Old data wiped.")

# 3. GENERATE REALISTIC BRANCHES
branches = [
    (1, 'New York - Main St', 'Michael Scott'),
    (2, 'San Francisco - Tech Park', 'Sheryl Sandberg'),
    (3, 'Chicago - Loop', 'Oprah Winfrey'),
    (4, 'Austin - Downtown', 'Elon Musk'),
    (5, 'Miami - Beach', 'Pitbull')
]
sql_branch = "INSERT INTO Branches (Branch_ID, Location, Manager_Name) VALUES (%s, %s, %s)"
cursor.executemany(sql_branch, branches)
print(f">> Created {len(branches)} Branches.")

# 4. GENERATE 500 REALISTIC CUSTOMERS & LOANS
first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]

customers = []
loans = []

print(">> Generating 500 applicants (using Normal Distribution)...")

for i in range(1, 501):
    c_id = 1000 + i
    
    # 1. Realistic Name
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # 2. Realistic Age (Bell curve around 35 years old)
    age = int(random.gauss(35, 10))
    age = max(18, min(70, age)) # Keep between 18 and 70
    
    # 3. Realistic Income (Log-Normal distribution - most people earn 40k-80k, few earn huge amounts)
    # Mean 60k, Std Dev 20k
    income = int(random.gauss(60000, 20000))
    income = max(20000, min(250000, income)) # Cap between 20k and 250k
    
    # 4. Realistic Credit Score (Correlated to Income + Randomness)
    # Base score 600 + (Income factor) + (Age factor) + Noise
    base_score = 600
    income_bonus = (income - 50000) / 1000  # +1 point for every $1k over 50k
    age_bonus = (age - 25) * 2              # +2 points for every year over 25
    noise = random.randint(-50, 50)         # Random luck factor
    
    credit_score = int(base_score + income_bonus + age_bonus + noise)
    credit_score = max(300, min(850, credit_score)) # Strict limits
    
    customers.append((c_id, name, age, income, credit_score))
    
    # 5. Loan Details
    l_id = 5000 + i
    branch_id = random.randint(1, 5)
    
    # Loan Amount (People usually borrow 10% to 50% of their income)
    loan_ratio = random.uniform(0.1, 0.5)
    loan_amount = int(income * loan_ratio)
    
    term = random.choice([12, 24, 36, 48, 60])
    
    # 6. BANKER DECISION LOGIC (The "Truth")
    # Rule: Approved if (Income > 40k AND Score > 600) OR (Income > 100k)
    if (income > 40000 and credit_score > 600) or (income > 100000):
        decision = 1 # Approved
        # Add 5% human error (Banker made a mistake)
        if random.random() < 0.05: decision = 0 
    else:
        decision = 0 # Rejected
        # Add 5% human error (Banker was generous)
        if random.random() < 0.05: decision = 1

    loans.append((l_id, c_id, branch_id, loan_amount, term, decision, None))

# 5. INSERT DATA
print(">> Inserting data into MySQL...")
sql_cust = "INSERT INTO Customers (Customer_ID, Name, Age, Income, Credit_Score) VALUES (%s, %s, %s, %s, %s)"
cursor.executemany(sql_cust, customers)

sql_loan = "INSERT INTO Loans (Loan_ID, Customer_ID, Branch_ID, Loan_Amount, Term_Months, Banker_Decision, AI_Risk_Prediction) VALUES (%s, %s, %s, %s, %s, %s, %s)"
cursor.executemany(sql_loan, loans)

conn.commit()
conn.close()
print(f"\nSUCCESS! Your database now has {len(customers)} real-looking customers.")
print("Run 'train_model.py' next to train your AI on this huge dataset!")