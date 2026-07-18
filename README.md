# PySQL: Bank Loan Risk Management System

## 📌 Project Overview
This repository contains an end-to-end data engineering and intelligent risk classification system that bridges relational database mechanics with machine learning. The project implements a complete **ETL (Extract, Transform, Load) pipeline** to clean, normalize, and load historical consumer banking datasets into a structured MySQL database schema.

Using the normalized historical records, the system builds a machine learning engine to predict personal loan application risks, exposing a command-line interface (CLI) for real-time customer onboarding, risk inference, and automated database ledger updates.

---

## 🏗️ System Architecture & Workflow

The platform operates across three independent, cascading modules:

### 1. The ETL Data Pipeline (`etl_import_kaggle.py`)
- Reads raw, flat financial data (`UniversalBank.csv`).
- Eliminates anomalies and drops redundant identifiers.
- Dynamically constructs a relational schema containing three normalized entities: `Regions`, `Customers`, and `Loan_History` to enforce data integrity and eliminate structural redundancy.
- Executes high-speed bulk inserts to populate the tables.

### 2. The Predictive Risk Engine (`train_kaggle_model.py`)
- Establishes an active database session to pull verified historical records.
- Implements strict logical grouping using `WHERE Personal_Loan_Status IS NOT NULL` to isolate historical decisions from active applicants awaiting a determination.
- Isolates key predictive feature vectors: annual income, average credit card spending, and outstanding mortgage values.
- Deploys a **Logistic Regression class-weighted classification model** configured with `class_weight='balanced'` to explicitly mitigate extreme class imbalance.
- Serializes the optimized model parameters into a production-ready file (`kaggle_brain.pkl`).

### 3. The Live Application Ledger Interface (`app_kaggle_interface.py`)
- Acts as the main operations portal.
- Loads the serialized classification parameters.
- Accepts live console inputs for new applicants (income, credit spending, mortgage).
- Generates a real-time risk decision: **APPROVED (Safe)** or **REJECTED (Risky)**.
- Dynamically formats structural inserts and writes the raw input, AI prediction status, and generated ledger keys back to MySQL.

---

## 📊 Relational Database Schema Design

The schema is built to model an enterprise banking ledger while enforcing relational integrity:

- **`Regions` Table:** Tracks unique geography points using the zip code as a primary key to map corresponding municipal attributes.
- **`Customers` Table:** Collects anonymous demographic metrics such as age, experience, family size, and education level, linked to the `Regions` table via foreign key constraints.
- **`Loan_History` Table:** Stores annual financials, credit spending trends, outstanding mortgage collateral, the historical ground-truth loan status, and the machine learning risk tag, linked back to customer profiles through relational keys.

---

## 📂 Repository Structure

- `etl_import_kaggle.py` - Automated MySQL database initialization, relational table creation, and data parsing script.
- `train_kaggle_model.py` - Historical data query script, feature extraction, balanced logistic classifier training, and model serialization engine.
- `app_kaggle_interface.py` - Interactive client onboarding application for live prediction and database ledger insertion.
- `generate_real_data.py` - Synthetic data generation script using Gaussian distributions to create balanced banking applicants for local prototyping.
- `requirements.txt` - Project dependency specification file.

---

## ⚙️ Local Deployment & Execution Order

Follow this sequence to set up the pipeline and run the application locally on Windows.

### 1. Install Dependencies
Install all required database connectors and data science dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Database Credentials
Open `etl_import_kaggle.py`, `train_kaggle_model.py`, and `app_kaggle_interface.py`, and make sure the `db_config` dictionary contains your MySQL credentials:

```python
db_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "YOUR_MYSQL_PASSWORD",
    "database": "bank_kaggle_db"
}
```

### 3. Initialize the ETL Pipeline
Parse, clean, normalize, and import the dataset into your MySQL database:

```bash
python etl_import_kaggle.py
```

### 4. Train the Risk Model
Pull the cleaned historical records, fit the classifier, and serialize the trained model:

```bash
python train_kaggle_model.py
```

### 5. Launch the Client Portal
Start the live CLI portal to onboard new applicants, run real-time predictions, and automatically store results in the database:

```bash
python app_kaggle_interface.py
```

---

## ✅ Key Features

- End-to-end ETL pipeline for structured banking data ingestion.
- Normalized MySQL relational database design.
- Machine learning-based personal loan risk prediction.
- Balanced logistic regression for imbalanced classification handling.
- CLI-driven real-time applicant onboarding and prediction.
- Automated ledger updates to MySQL after each inference.

---

## 🛠️ Tech Stack

- **Python**
- **MySQL**
- **Pandas**
- **Scikit-learn**
- **Pickle**
- **CLI-based workflow**

---

## 🚀 Use Case

This project is designed for learning and prototyping intelligent banking systems that combine:
- Data engineering
- Relational database design
- Machine learning classification
- Real-time application processing

It is especially useful for students and developers exploring how ETL pipelines and AI models can work together in financial risk systems.