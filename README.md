🧹 Data Cleaning & Preparation Dashboard
<div align="center">
Show Image
Show Image
Show Image
Show Image
Show Image
A professional, production-ready Streamlit dashboard for end-to-end data cleaning and preparation workflows.
DecodeLabs Industrial Training Kit — Batch 2026 | Project 1
🚀 Live Demo • 📦 Installation • ✨ Features • 📸 Screenshots
</div>

📌 Project Overview
This dashboard transforms raw, messy datasets into reliable, analysis-ready data. Built as Project 1 of the DecodeLabs Data Analytics Industrial Training Kit, it covers the foundational 80% of every real-world data science workflow — cleaning and wrangling.

"Your analysis is only as good as your data. Make it count." — DecodeLabs


✨ Features
📊 Dataset Overview

Total rows, columns, missing values, and duplicate counts at a glance
Column summary table with dtype, null count, and unique values
Data type distribution pie chart
Interactive data preview (first 50 rows)

❓ Missing Value Analysis

Per-column missing value count and percentage
Completeness rate bar chart (color-coded: red → green)
Visual heatmap of null distribution across rows

🔁 Duplicate Detection & Removal

Duplicate row count with percentage
Before/after composition donut chart
Preview of duplicate rows
One-click duplicate removal (keeps first occurrence)

✏️ Data Cleaning Operations
OperationDescriptionFill Missing ValuesMean, Median, Mode, Forward Fill, Backward Fill, Custom ValueText StandardisationStrip whitespace, Title/Upper/Lower case, Remove special charactersDate FormattingAuto-detect & convert all date columns to ISO 8601 (YYYY-MM-DD)Type ConversionConvert columns to int64, float64, str, datetime64, boolDrop Null RowsRemove rows where a selected column is null
✅ Validation & Quality Report

Verification Gate — 0% duplicate IDs + 0% bad date formats (Project 2 threshold)
Before vs After comparison bar chart
Data Quality Score gauge (0–100%)

📋 Audit Change Log

Every operation is automatically logged (Change ID, Description, Impact, Status)
Download change log as CSV
Full dataset reset to original


🛠️ Tech Stack
TechnologyPurposePython 3.10+Core languageStreamlitWeb app frameworkPandasData manipulationPlotlyInteractive chartsNumPyNumerical operationsOpenPyXLExcel file handling

📦 Installation
1. Clone the repository
bashgit clone https://github.com/your-username/data-cleaning-dashboard.git
cd data-cleaning-dashboard
2. Create a virtual environment (recommended)
bashpython -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
3. Install dependencies
bashpip install -r requirements.txt
4. Run the app
bashstreamlit run data_cleaning_dashboard.py
The app will open at http://localhost:8501

📁 Project Structure
data-cleaning-dashboard/
│
├── data_cleaning_dashboard.py   # Main Streamlit application
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── sample_data/                 # (Optional) Sample datasets
    └── Dataset_for_Analytics.xlsx

🚀 Deployment
Option 1: Streamlit Community Cloud (Free — Recommended)

Push this repo to GitHub
Visit share.streamlit.io
Sign in with GitHub → New App
Select repo → set main file to data_cleaning_dashboard.py
Click Deploy → Get a public .streamlit.app URL

Option 2: Render (Free tier)

Connect your GitHub repo at render.com
Set Start Command:

bashstreamlit run data_cleaning_dashboard.py --server.port $PORT --server.address 0.0.0.0
Option 3: Railway (Free tier)

Connect repo at railway.app
Set the same start command as above


🎯 How to Use

Upload your .xlsx, .xls, or .csv dataset via the sidebar
Explore the Overview page to understand your data
Analyse missing values and duplicates
Clean your data using the available operations
Validate — confirm 0 duplicate IDs and 0 bad date formats
Download the cleaned dataset and the audit change log


📊 Data Quality Workflow
Raw Dataset  →  Missing Value Analysis  →  Duplicate Removal
     ↓
Text Standardisation  →  Date Formatting  →  Type Conversion
     ↓
Validation Gate  →  Quality Score  →  Download Cleaned Data

📋 Validation Gate (Project 2 Threshold)
Before progressing to Project 2, the dataset must pass:
CheckRequirement✅ Unique Identifiers0% duplicate IDs✅ Date Format Compliance0% non-ISO 8601 dates

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request


📄 License
This project is licensed under the MIT License — see the LICENSE file for details.

👨‍💻 Author
Built with ❤️ as part of the DecodeLabs Industrial Training Program
Show Image
📧 decodelabs.tech@gmail.com
🌐 www.decodelabs.tech
📍 Greater Lucknow, India
