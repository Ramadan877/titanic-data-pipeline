"""Titanic passenger data: cleaning, SQLite persistence, and SQL analytics."""

from __future__ import annotations

import sqlite3
import sys
from typing import Optional

import pandas as pd

DEFAULT_DATASET_URL = (
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)


def _extract_title(name: str) -> str:
    """Parse title from name (e.g. 'Braund, Mr. Owen Harris' -> 'Mr')."""
    return name.split(",", 1)[1].split(".", 1)[0].strip()


class TitanicAnalyzer:
    """Load, clean, persist, and analyze Titanic passenger data."""

    def __init__(self, db_name: str = "titanic_project.db") -> None:
        self.conn = sqlite3.connect(db_name)
        self.df: Optional[pd.DataFrame] = None

    def clean_data(self, source: str) -> None:
        """Load CSV from a URL or local path, then clean and engineer features."""
        print(f"--- Loading data from: {source} ---")
        self.df = pd.read_csv(source)

        print(f"\nDataset loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        print("\nMissing values before cleaning:")
        print(self.df.isnull().sum())

        self.df["Age"] = self.df["Age"].fillna(self.df["Age"].median())
        self.df = self.df.dropna(subset=["Embarked"])
        self.df = self.df.drop(columns=["Cabin"])

        print("\nMissing values after cleaning:")
        print(self.df.isnull().sum())
        print(f"\nDimensions after cleaning: {self.df.shape}")
        print("-" * 30)

        self.df["Title"] = self.df["Name"].map(_extract_title)
        self.df["FamilySize"] = self.df["SibSp"] + self.df["Parch"] + 1

        print("\nFeature engineering complete.")
        print(f"Final dimensions: {self.df.shape}")
        print(self.df.head())
        print("-" * 30)

    def save_to_db(self) -> None:
        """Persist the cleaned dataframe to the passengers table."""
        if self.df is None:
            raise RuntimeError("No data to save. Run clean_data() first.")
        self.df.to_sql("passengers", self.conn, if_exists="replace", index=False)

    def run_analytics(self) -> None:
        """Execute SQL analytics and print the summary report."""
        print("\n" + "=" * 40)
        print(" Titanic Analytics Report")
        print("=" * 40)

        queries = {
            "Survival rate by title (count > 5)": """
                SELECT Title,
                       COUNT(*) AS Count,
                       ROUND(AVG(Survived), 4) AS Survival_Rate
                FROM passengers
                GROUP BY Title
                HAVING Count > 5
                ORDER BY Survival_Rate DESC
            """,
            "Top 10 fares by class (window rank)": """
                SELECT Name, Pclass, Fare,
                       RANK() OVER (PARTITION BY Pclass ORDER BY Fare DESC) AS Fare_Rank
                FROM passengers
                LIMIT 10
            """,
            "Survival probability by family size": """
                SELECT FamilySize,
                       ROUND(AVG(Survived), 4) AS Survival_Probability
                FROM passengers
                GROUP BY FamilySize
                ORDER BY FamilySize
            """,
            "Survival rate by age group (%)": """
                SELECT
                    CASE
                        WHEN Age < 18 THEN 'Child'
                        WHEN Age < 65 THEN 'Adult'
                        ELSE 'Senior'
                    END AS Age_Group,
                    COUNT(*) AS Passenger_Count,
                    ROUND(AVG(Survived) * 100, 2) AS Survival_Rate_Pct
                FROM passengers
                GROUP BY Age_Group
                ORDER BY Survival_Rate_Pct DESC
            """,
        }

        for title, sql in queries.items():
            print(f"\n--- {title} ---")
            print(pd.read_sql_query(sql, self.conn).to_string(index=False))

    def close_conn(self) -> None:
        """Close the SQLite connection."""
        self.conn.close()
        print("\nDatabase connection closed.")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <csv_url_or_path>")
        print(f"\nExample:\n  python analyzer.py {DEFAULT_DATASET_URL}")
        sys.exit(1)

    analyzer = TitanicAnalyzer()
    try:
        source = sys.argv[1]
        analyzer.clean_data(source)
        analyzer.save_to_db()
        analyzer.run_analytics()
    except Exception as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        analyzer.close_conn()


if __name__ == "__main__":
    main()
