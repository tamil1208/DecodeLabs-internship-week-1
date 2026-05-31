# 🧹 Data Cleaning & Preparation Dashboard

<div align="center">

A professional, production-ready Streamlit dashboard for end-to-end data cleaning and preparation workflows.

**DecodeLabs Industrial Training Kit — Batch 2026 | Project 1**

🚀 Live Demo: https://decodelabs-internship-xiqu.onrender.com/

</div>

---

# 📌 Project Overview

This dashboard transforms raw, messy datasets into reliable, analysis-ready data.

Built as **Project 1 of the DecodeLabs Data Analytics Industrial Training Kit**, this project focuses on the foundational part of data analytics:

* Missing Value Handling
* Duplicate Detection
* Data Standardization
* Validation
* Exporting Clean Data

> "Your analysis is only as good as your data. Make it count."

---

# ✨ Features

## 📊 Dataset Overview

* Total rows and columns
* Missing values summary
* Duplicate count
* Dataset preview
* Data type distribution

## ❓ Missing Value Analysis

* Missing value counts
* Missing value percentages
* Null distribution visualization

## 🔁 Duplicate Detection

* Duplicate row identification
* Duplicate percentage calculation
* Before vs After comparison

## ✏️ Data Cleaning Operations

### Missing Values

* Mean Imputation
* Median Imputation
* Mode Imputation
* Forward Fill
* Backward Fill

### Text Cleaning

* Remove spaces
* Convert case formatting
* Remove unwanted characters

### Date Standardization

* Convert to ISO format (YYYY-MM-DD)

### Type Conversion

* Convert datatypes dynamically

---

# ✅ Validation & Quality Report

The dashboard validates:

✔ Duplicate IDs = 0

✔ Invalid Date Formats = 0

✔ Quality Score Calculation

---

# 📋 Audit Change Log

Tracks:

* Change ID
* Description
* Impact
* Status

Downloadable as CSV.

---

# 🛠 Tech Stack

| Technology | Purpose              |
| ---------- | -------------------- |
| Python     | Core Language        |
| Streamlit  | Dashboard            |
| Pandas     | Data Manipulation    |
| Plotly     | Visualization        |
| NumPy      | Numerical Operations |
| OpenPyXL   | Excel Handling       |

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
streamlit run data_cleaning_dashboard.py
```

---

# 📁 Project Structure

```text
data-cleaning-dashboard/
│
├── data_cleaning_dashboard.py
├── requirements.txt
├── README.md
└── sample_data/
```

---

# 🚀 Deployment

## Streamlit Community Cloud

1. Push code to GitHub
2. Open Streamlit Cloud
3. Select repository
4. Deploy

## Render

Start command:

```bash
streamlit run data_cleaning_dashboard.py --server.port $PORT --server.address 0.0.0.0
```

---

# 🎯 Workflow

```text
Raw Dataset
    ↓
Missing Value Analysis
    ↓
Duplicate Removal
    ↓
Data Cleaning
    ↓
Validation
    ↓
Download Clean Dataset
```

---

# 📋 Project Validation Gate

Before moving to Project 2:

| Check        | Requirement      |
| ------------ | ---------------- |
| Unique IDs   | 0% duplicates    |
| Date Formats | 0% invalid dates |

---

# 👨‍💻 Author

**Tamilarasan**

GitHub:

https://github.com/tamil1208

LinkedIn:

https://www.linkedin.com/in/tamil-arasan-a2466b274

---

Built with ❤️ as part of DecodeLabs Industrial Training Program.
