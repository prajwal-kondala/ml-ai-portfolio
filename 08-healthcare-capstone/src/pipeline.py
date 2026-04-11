"""
Healthcare Data Analysis Pipeline
Project 08 — Prajwal Kondala
IIT Kharagpur | DS/AI Journey
April 2026
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings("ignore")


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load and validate healthcare data.

    Args:
        filepath: Path to CSV file

    Returns:
        Validated DataFrame
    """
    df = pd.read_csv(filepath)
    print(f"Data loaded: {df.shape}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full data cleaning pipeline.

    Steps:
        1. Remove duplicate rows
        2. Fix categorical data types

    Args:
        df: Raw DataFrame

    Returns:
        Cleaned DataFrame
    """
    initial_rows = len(df)

    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Duplicates removed: {initial_rows - len(df)}")

    categorical_cols = ["sex", "cp", "fbs", "restecg",
                        "exang", "slope", "ca", "thal", "target"]
    for col in categorical_cols:
        df[col] = df[col].astype("category")

    print(f"Clean data shape: {df.shape}")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create new features from existing columns.

    Features created:
        - age_group: Age buckets using pd.cut
        - chol_risk: Cholesterol risk using np.select
        - high_hr: High heart rate flag using np.where
        - bp_category: BP categories using pd.qcut
        - oldpeak_log: Log transform using np.log1p

    Args:
        df: Cleaned DataFrame

    Returns:
        DataFrame with engineered features
    """
    # Age groups — pd.cut!
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 40, 50, 60, 100],
        labels=["Young (<40)", "Middle (40-50)",
                "Senior (50-60)", "Elderly (60+)"]
    )

    # Cholesterol risk — np.select!
    conditions = [
        df["chol"] < 200,
        (df["chol"] >= 200) & (df["chol"] < 240),
        df["chol"] >= 240
    ]
    choices = ["Normal", "Borderline High", "High Risk"]
    df["chol_risk"] = np.select(conditions, choices,
                                default="Unknown")

    # Heart rate flag — np.where!
    df["high_hr"] = np.where(df["thalach"] > 150, 1, 0)

    # Blood pressure — pd.qcut!
    df["bp_category"] = pd.qcut(
        df["trestbps"],
        q=4,
        labels=["Low", "Normal", "Elevated", "High"]
    )

    # Log transform — np.log1p!
    df["oldpeak_log"] = np.log1p(df["oldpeak"])

    print(f"Features engineered: {df.shape[1]} total columns")
    return df


def run_hypothesis_tests(df: pd.DataFrame) -> dict:
    """
    Run statistical hypothesis tests.

    Tests:
        1. T-test: Age vs Heart Disease
        2. Chi-square: Gender vs Heart Disease
        3. T-test: Max Heart Rate vs Heart Disease

    Args:
        df: Feature engineered DataFrame

    Returns:
        Dictionary of test results
    """
    results = {}

    # Test 1: Age
    disease = df[df["target"].astype(int) == 1]["age"]
    no_disease = df[df["target"].astype(int) == 0]["age"]
    t_stat, p_val = stats.ttest_ind(disease, no_disease)
    results["age_test"] = {
        "test"       : "Independent t-test",
        "t_stat"     : round(t_stat, 4),
        "p_value"    : round(p_val, 4),
        "significant": p_val < 0.05,
        "finding"    : f"Disease: {disease.mean():.2f} vs "
                       f"No Disease: {no_disease.mean():.2f} years"
    }

    # Test 2: Gender
    contingency = pd.crosstab(df["sex"], df["target"])
    chi2, p_val, dof, _ = stats.chi2_contingency(contingency)
    results["gender_test"] = {
        "test"       : "Chi-square test",
        "chi2"       : round(chi2, 4),
        "p_value"    : round(p_val, 4),
        "dof"        : dof,
        "significant": p_val < 0.05,
        "finding"    : "Females: 75% vs Males: 44.7% disease rate"
    }

    # Test 3: Heart Rate
    hr_disease = df[df["target"].astype(int) == 1]["thalach"]
    hr_no_disease = df[df["target"].astype(int) == 0]["thalach"]
    t_stat, p_val = stats.ttest_ind(hr_disease, hr_no_disease)
    results["heartrate_test"] = {
        "test"       : "Independent t-test",
        "t_stat"     : round(t_stat, 4),
        "p_value"    : round(p_val, 4),
        "significant": p_val < 0.05,
        "finding"    : f"Disease: {hr_disease.mean():.2f} vs "
                       f"No Disease: {hr_no_disease.mean():.2f} bpm"
    }

    return results


def run_pipeline(filepath: str) -> pd.DataFrame:
    """
    Run complete data pipeline end to end.

    Args:
        filepath: Path to raw CSV file

    Returns:
        Final processed DataFrame
    """
    print("=" * 55)
    print("HEALTHCARE DATA PIPELINE — STARTING")
    print("=" * 55)

    df = load_data(filepath)
    df = clean_data(df)
    df = engineer_features(df)
    results = run_hypothesis_tests(df)

    print("\nHypothesis Test Results:")
    print("-" * 55)
    for test, result in results.items():
        sig = "SIGNIFICANT ✅" if result["significant"] else "NOT SIGNIFICANT ❌"
        print(f"  {test}: p={result['p_value']:.4f} → {sig}")
        print(f"  Finding: {result['finding']}\n")

    print("=" * 55)
    print(f"✅ Pipeline complete! Final shape: {df.shape}")
    print("=" * 55)
    return df


if __name__ == "__main__":
    df = run_pipeline("data/raw/heart.csv")
    df.to_csv("data/processed/heart_disease_cleaned.csv",
              index=False)
    print("\nProcessed data saved!")
