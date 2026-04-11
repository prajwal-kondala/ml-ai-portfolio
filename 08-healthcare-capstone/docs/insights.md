# Healthcare Data Analysis — Key Insights
## Project 08 — Prajwal Kondala | IIT KGP
## April 2026

---

## Dataset Overview

| Property | Value |
|----------|-------|
| Source | Cleveland Heart Disease Dataset (UCI, 1988) |
| Raw rows | 1,025 |
| Clean rows | 302 (after removing 723 duplicates!) |
| Features | 14 (13 clinical + 1 target) |
| Target balance | 54.3% disease vs 45.7% no disease |
| Missing values | Zero |

---

## Day 1 Insights — Data Understanding

### Finding 1: Massive Duplicate Issue
- Raw dataset: 1,025 rows
- Duplicates found: **723 (70.5%!)**
- Clean dataset: 302 unique patients
- **Lesson:** Always check duplicates FIRST before any analysis!

### Finding 2: Zero Missing Values
- All 14 columns have zero missing values
- Dataset usability score 8.82 on Kaggle — fully justified!
- No imputation strategy needed

### Finding 3: 9 Categorical Columns Disguised as Integers
- Columns like sex, cp, thal stored as int dtype in CSV
- Must convert to category for correct analysis
- **Lesson:** Always check domain knowledge — not just dtypes!

### Finding 4: Balanced Target Variable
- Disease (1): 164 patients → 54.3%
- No Disease (0): 138 patients → 45.7%
- Near-perfect balance → No class imbalance handling needed!

### Finding 5: Oldpeak Zeros Are Medically Valid
- 98 patients (32.5%) have oldpeak = 0
- NOT missing values — means no ST depression during exercise
- These are patients with healthy cardiac response!

---

## Day 2 Insights — Feature Engineering

### Feature 1: Age Groups (pd.cut)

| Age Group | Patients | Disease Rate |
|-----------|---------|-------------|
| Young (<40) | 18 | 66.7% |
| Middle (40-50) | 76 | **69.7%** ← Highest! |
| Senior (50-60) | 129 | 49.6% |
| Elderly (60+) | 79 | 44.3% ← Lowest! |

**Counterintuitive:** Younger patients have MORE disease!
**Explanation:** Selection bias — younger patients referred due to serious symptoms!

### Feature 2: Cholesterol Risk (np.select)

| Risk Category | Patients | Disease Rate |
|--------------|---------|-------------|
| Normal (<200) | 49 | 59.2% |
| Borderline (200-240) | 98 | 60.2% |
| High Risk (>240) | 155 | **49.0%** ← Lowest! |

**Counterintuitive:** High cholesterol patients have LESS disease!
**Explanation:** Routine cholesterol monitoring vs symptomatic referrals!

### Feature 3: Heart Rate Flag (np.where)

| HR Category | Patients | Disease Rate |
|------------|---------|-------------|
| Low HR (≤150) | 139 | 32.4% |
| High HR (>150) | 163 | **73.0%** ← Highest! |

**Finding:** High heart rate patients have MORE disease!
**Medical explanation:** Diseased hearts race harder under exercise stress!

### Feature 4: Blood Pressure Categories (pd.qcut)

| BP Category | Disease Rate |
|------------|-------------|
| Low | 61.9% ← Highest! |
| Normal | 54.1% |
| Elevated | 56.1% |
| High | 41.5% ← Lowest! |

**Counterintuitive:** Low BP patients have MORE disease!
**Explanation:** Same selection bias pattern throughout!

### Feature 5: Oldpeak Log Transform (np.log1p)
- Skewness BEFORE: 1.266 (heavily right skewed!)
- Skewness AFTER: 0.392 (much improved!)
- log1p used instead of log because 32.5% zeros!
- **Lesson:** log(0) = undefined, log1p(0) = 0 ✅

---

## Day 2 Insights — EDA Analysis

### Correlation with Target (Numeric Features)

| Feature | Correlation |
|---------|------------|
| thalach (Max Heart Rate) | **+0.42** ← Strongest! |
| oldpeak (ST Depression) | -0.43 |
| oldpeak_log | -0.43 |
| age | -0.22 |
| trestbps (Blood Pressure) | -0.15 |
| chol (Cholesterol) | **-0.08** ← Weakest! |

**Key finding:** Cholesterol correlation = -0.08 (near zero!)
Confirms cholesterol is a poor predictor in this dataset!

### Chest Pain Analysis

| CP Type | Description | Disease Pattern |
|---------|-------------|----------------|
| 0 | Typical Angina | Blue dominant (more no-disease!) |
| 1 | Atypical Angina | Roughly equal |
| 2 | Non-Anginal | **Red dominant (most disease!)** |
| 3 | Asymptomatic | More disease than expected |

**Insight:** Non-anginal pain patients delay seeking help → later diagnosis → more disease!

### Gender Analysis

| Gender | Disease Rate |
|--------|------------|
| Female | **75.0%** |
| Male | 44.7% |

**Counterintuitive:** Females have HIGHER disease rate!
**Explanation:** Clinical selection bias in 1988 referral patterns!

### NamedAgg Age Group Complete Picture

| Age Group | Count | Avg Chol | Avg HR | Avg BP | Disease % |
|-----------|-------|----------|--------|--------|-----------|
| Young (<40) | 18 | 215.0 | 169.3 | 126.2 | 66.7% |
| Middle (40-50) | 76 | 236.6 | 158.6 | 124.1 | 69.7% |
| Senior (50-60) | 129 | 248.4 | 147.8 | 133.5 | 49.6% |
| Elderly (60+) | 79 | 260.2 | 139.2 | 137.0 | 44.3% |

**Triple pattern revealed:**
- Cholesterol INCREASES with age ↑
- Heart rate DECREASES with age ↓
- Disease rate DECREASES with age ↓ (counterintuitive!)

---

## Day 2 Insights — Hypothesis Testing

### Test 1: Age vs Heart Disease (t-test)

```
H0: Mean age same for both groups
H1: Mean age differs between groups

Disease group    → 52.59 years
No Disease group → 56.60 years
Difference       → 4.01 years

t-statistic : -3.9338
p-value     : 0.0001

Result: REJECT H0 ✅
Age IS significantly different — not random chance!
```

### Test 2: Gender vs Heart Disease (Chi-square)

```
H0: Disease rate same for males and females
H1: Disease rate differs by gender

Contingency Table:
         No Disease  Disease
Female       24         72
Male        114         92

Chi-square : 23.0839
p-value    : 0.0000
dof        : 1

Result: REJECT H0 ✅
Gender IS significantly associated with disease!
```

### Test 3: Max Heart Rate vs Heart Disease (t-test)

```
H0: Max heart rate same for both groups
H1: Max heart rate differs between groups

Disease group    → 158.38 bpm
No Disease group → 139.10 bpm
Difference       → 19.28 bpm!

t-statistic : 8.0148
p-value     : 0.0000

Result: REJECT H0 ✅ MOST SIGNIFICANT!
Heart rate is the strongest statistical predictor!
```

### Hypothesis Test Summary

| Test | p-value | t/χ² statistic | Significant? |
|------|---------|----------------|-------------|
| Age vs Disease | 0.0001 | t = -3.93 | ✅ YES |
| Gender vs Disease | 0.0000 | χ² = 23.08 | ✅ YES |
| Heart Rate vs Disease | 0.0000 | t = 8.01 | ✅ STRONGEST |

**All 3 tests → All 3 REJECT H0!**

---

## The Big Picture — Key Lessons

### Lesson 1: Selection Bias Explains Everything
```
Traditional assumption → Older = More disease
Data shows            → Younger = More disease

Why? Patients in this 1988 Cleveland study were NOT
a random sample. They were REFERRED based on symptoms.

Young patients → serious symptoms → referred → found disease!
Old patients → routine checkups → many healthy → lower rate!
```

### Lesson 2: Traditional Risk Factors Are Insufficient
```
Every "classic" risk factor showed counterintuitive pattern:
→ Age: younger = more disease ❌
→ Cholesterol: higher = LESS disease ❌
→ Blood pressure: lower = MORE disease ❌
→ Gender: females = MORE disease ❌

The REAL predictors:
→ Chest pain type (cp) — strongest categorical!
→ Thalassemia (thal) — blood disorder type!
→ Max heart rate (thalach) — exercise stress response!
→ ST depression (oldpeak) — electrical heart signal!
```

### Lesson 3: Correlation ≠ Causation
```
High heart rate → more disease

Does high HR CAUSE disease? NO!
Disease CAUSES high HR during exercise stress!

Diseased hearts work harder → race faster under stress!
This is a classic correlation ≠ causation scenario!
```

### Lesson 4: Data Cleaning Is Everything
```
Raw: 1025 rows
After cleaning: 302 rows

70.5% of raw data were duplicates!
Without cleaning → every analysis would be wrong!
This is why cleaning comes BEFORE everything else!
```

---

## Profiling Alerts Reference

ydata profiling flagged 4 alerts on this dataset:

```
1. cp highly correlated with target → ✅ Confirmed!
2. thal highly correlated with target → ✅ Confirmed!
3. oldpeak has 32.5% zeros → ✅ Medically valid!
4. 9 categorical, 5 numeric columns → ✅ Fixed with astype!
```

---

## Final Insight — Why ML Is Needed

```
Visual inspection showed overlapping distributions.
Statistical tests showed significant differences.
But no single feature perfectly separates disease groups.

This is exactly why Machine Learning models exist:
→ Logistic Regression, Random Forest, XGBoost
→ Find patterns across ALL features simultaneously
→ What humans can't see, models can learn!

Phase 2 (ML) begins next week — bringing these insights
into predictive models! 🤖
```

---

*insights.md — Project 08 Healthcare Data Analytics Pipeline*
*Prajwal Kondala | IIT Kharagpur | B.Tech*
*DS/AI Journey — Feb 2026 → Mastery*

