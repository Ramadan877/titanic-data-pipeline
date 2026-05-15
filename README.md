# Titanic Survival Analysis

A compact end-to-end data science sample project that loads the classic **Titanic passenger dataset**, cleans and engineers features in **pandas**, persists the result to **SQLite**, and runs exploratory analytics with **SQL window functions** and aggregations.

Built as a portfolio-ready demonstration of reproducible ETL, feature engineering, and SQL-driven insights in Python.

---

## Overview

The RMS Titanic disaster is one of the most studied datasets in introductory data science. This project answers practical questions about survival patterns—by passenger title, ticket class, family size, and age group—using a small, object-oriented pipeline you can run from the command line.

| Stage | Tooling | What happens |
|-------|---------|--------------|
| Ingest & clean | pandas | Load CSV, handle missing values, drop sparse columns |
| Feature engineering | pandas | Extract `Title` from names; compute `FamilySize` |
| Persist | SQLite | Store cleaned table as `passengers` |
| Analyze | SQL | Grouped survival rates, window rankings, age cohorts |

---

## Features

- **Structured cleaning pipeline** — median imputation for `Age`, row drops for missing `Embarked`, removal of the high-null `Cabin` column
- **Feature engineering** — social title extraction (`Mr`, `Mrs`, `Miss`, …) and household size (`SibSp` + `Parch` + 1)
- **Local analytics database** — SQLite for portable, dependency-free storage
- **Four analytic SQL reports** — survival by title, fare rank within class, family-size survival, age-band survival
- **CLI entry point** — load data directly from a public CSV URL (no local download required)

---

## Project structure

```
Titanic_Data_Analysis/
├── analyzer.py        # Main pipeline: TitanicAnalyzer class + CLI
├── requirements.txt   # Python dependencies (pandas)
├── README.md
├── .gitignore
└── titanic_project.db # Created at runtime (gitignored)
```

---

## Tech stack

- **Python 3.10+** (recommended)
- **[pandas](https://pandas.pydata.org/)** — data loading, cleaning, feature engineering
- **[SQLite](https://www.sqlite.org/)** (stdlib `sqlite3`) — embedded analytics store

---

## Dataset

The pipeline loads the Titanic dataset from a public hosted CSV ([Data Science Dojo / datasets](https://github.com/datasciencedojo/datasets)):

`https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv`

Expected columns include: `PassengerId`, `Survived`, `Pclass`, `Name`, `Sex`, `Age`, `SibSp`, `Parch`, `Ticket`, `Fare`, `Cabin`, `Embarked`.

No manual download is required—pandas reads the URL at runtime. You can also pass a local file path with the same schema if you prefer.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Ramadan877/Titanic_Data_Analysis.git
   cd Titanic_Data_Analysis
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the full pipeline (clean → save → analyze) against the public dataset URL:

```bash
python analyzer.py https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
```

Example output sections:

1. Missing-value summary before and after cleaning  
2. Dataset shape and preview after feature engineering  
3. **Titanic Analytics Report** — four SQL result tables printed to the console  

The script creates **`titanic_project.db`** in the working directory and replaces the `passengers` table on each run.

---

## Pipeline details

### 1. Data cleaning (`clean_data`)

| Step | Rationale |
|------|-----------|
| Fill `Age` with median | Robust to skew vs. mean; preserves sample size |
| Drop rows with null `Embarked` | Only two rows affected; avoids arbitrary mode imputation |
| Drop `Cabin` | ~77% missing; low signal for this exploratory pass |

### 2. Feature engineering

- **`Title`** — parsed from `Name` (e.g. `Braund, Mr. Owen Harris` → `Mr`)
- **`FamilySize`** — `SibSp + Parch + 1` (passenger plus relatives aboard)

### 3. Persistence (`save_to_db`)

Cleaned data is written to SQLite table **`passengers`** via `DataFrame.to_sql(..., if_exists='replace')`.

### 4. Analytics (`run_analytics`)

| Query | Question answered |
|-------|-------------------|
| **Q1** | Which titles (with >5 passengers) had the highest survival rate? |
| **Q2** | Who paid the top fares within each ticket class?    |
| **Q3** | How does survival probability change with family size? |
| **Q4** | Child vs. adult vs. senior survival rates (age buckets) |

---

## Code architecture

The pipeline is encapsulated in a single class for clarity and reuse:

```python
from analyzer import TitanicAnalyzer

analyzer = TitanicAnalyzer(db_name="titanic_project.db")
analyzer.clean_data(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)
analyzer.save_to_db()
analyzer.run_analytics()
analyzer.close_conn()
```

**`TitanicAnalyzer` methods**

| Method | Description |
|--------|-------------|
| `__init__(db_name)` | Open SQLite connection |
| `clean_data(filepath)` | Load CSV from URL or local path, clean, engineer features |
| `save_to_db()` | Persist `self.df` to `passengers` |
| `run_analytics()` | Execute and print SQL reports |
| `close_conn()` | Close database connection |

---

## Possible extensions

- [ ] Add unit tests for cleaning and title extraction  
- [ ] Export reports to HTML or Markdown  
- [ ] Visualize survival rates with **matplotlib** / **seaborn**  
- [ ] Train a simple classifier (`Survived` ~ `Pclass`, `Sex`, `Age`, …)  
- [ ] Parameterize SQL queries via CLI flags  

---

## Author

**Abdelrahman Ramadan** — [GitHub @Ramadan877](https://github.com/Ramadan877)

---

