"""
Basic unit tests for Healthcare Data Pipeline.
Project 08 — Prajwal Kondala | IIT KGP
April 2026
"""
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_df():
    """Create sample DataFrame for testing."""
    return pd.DataFrame({
        "age"     : [45, 55, 62, 38, 70],
        "sex"     : [1, 0, 1, 1, 0],
        "cp"      : [0, 2, 1, 3, 0],
        "trestbps": [120, 130, 145, 110, 150],
        "chol"    : [180, 250, 300, 220, 190],
        "fbs"     : [0, 1, 0, 0, 1],
        "restecg" : [0, 1, 0, 0, 2],
        "thalach" : [160, 140, 120, 175, 130],
        "exang"   : [0, 1, 0, 0, 1],
        "oldpeak" : [0.0, 1.5, 2.3, 0.0, 3.1],
        "slope"   : [0, 1, 2, 0, 1],
        "ca"      : [0, 1, 2, 0, 3],
        "thal"    : [1, 2, 0, 1, 2],
        "target"  : [1, 0, 1, 1, 0],
    })


def test_no_missing_values(sample_df):
    """Test dataset has no missing values."""
    assert sample_df.isnull().sum().sum() == 0


def test_target_is_binary(sample_df):
    """Test target column contains only 0 and 1."""
    assert set(sample_df["target"].unique()).issubset({0, 1})


def test_age_range_valid(sample_df):
    """Test age values are in valid medical range."""
    assert sample_df["age"].min() >= 0
    assert sample_df["age"].max() <= 120


def test_cholesterol_positive(sample_df):
    """Test no zero or negative cholesterol values."""
    assert (sample_df["chol"] > 0).all()


def test_log_transform(sample_df):
    """Test log1p transform reduces skewness."""
    original_skew = abs(sample_df["oldpeak"].skew())
    transformed_skew = abs(np.log1p(sample_df["oldpeak"]).skew())
    assert transformed_skew <= original_skew


def test_age_groups_created(sample_df):
    """Test age group feature creation works correctly."""
    sample_df["age_group"] = pd.cut(
        sample_df["age"],
        bins=[0, 40, 50, 60, 100],
        labels=["Young (<40)", "Middle (40-50)",
                "Senior (50-60)", "Elderly (60+)"]
    )
    assert "age_group" in sample_df.columns
    assert sample_df["age_group"].isnull().sum() == 0


def test_high_hr_flag(sample_df):
    """Test high heart rate flag is binary 0 or 1."""
    sample_df["high_hr"] = np.where(
        sample_df["thalach"] > 150, 1, 0)
    assert set(sample_df["high_hr"].unique()).issubset({0, 1})


def test_no_duplicates_after_cleaning(sample_df):
    """Test duplicate removal works correctly."""
    # Add a duplicate row
    df_with_dup = pd.concat(
        [sample_df, sample_df.iloc[[0]]], ignore_index=True)
    assert len(df_with_dup) == 6  # 5 + 1 duplicate

    # Remove duplicates
    df_clean = df_with_dup.drop_duplicates().reset_index(drop=True)
    assert len(df_clean) == 5  # Back to original!
