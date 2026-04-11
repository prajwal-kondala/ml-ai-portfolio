# Dataset Documentation
## Project 08 — Healthcare Data Analytics Pipeline
**Prajwal Kondala | IIT KGP → AI/ML Engineer**

---

## Dataset Overview

| Property | Value |
|----------|-------|
| Name | Heart Disease Dataset |
| Source | [Kaggle — johnsmith88](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset) |
| Origin | Cleveland Clinic Foundation, USA (1988) |
| Usability Score | 8.82 / 10 on Kaggle |
| License | Unknown |
| Raw Rows | 1,025 |
| Clean Rows | **302 unique patients** |
| Duplicates Removed | 723 rows (70.5%!) |
| Columns | 14 (13 features + 1 target) |
| Missing Values | **Zero** |

---

## About This Dataset

This dataset originates from the famous 1988 UCI Machine Learning Repository study on heart disease. It combines data from four hospitals:
- Cleveland Clinic Foundation
- Hungarian Institute of Cardiology, Budapest
- VA Medical Center, Long Beach, California
- University Hospital, Zurich, Switzerland

Although the original dataset contains 76 attributes, all published experiments and analyses use this subset of 14 features — the exact columns in this dataset!

---

## Column Reference

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| age | Numeric | 29-77 years | Patient age in years |
| sex | Categorical | 0, 1 | 1=Male, 0=Female |
| cp | Categorical | 0, 1, 2, 3 | Chest pain type (see below) |
| trestbps | Numeric | 94-200 mm Hg | Resting blood pressure |
| chol | Numeric | 126-564 mg/dl | Serum cholesterol |
| fbs | Categorical | 0, 1 | Fasting blood sugar > 120: 1=Yes, 0=No |
| restecg | Categorical | 0, 1, 2 | Resting ECG results (see below) |
| thalach | Numeric | 71-202 bpm | Maximum heart rate achieved |
| exang | Categorical | 0, 1 | Exercise induced angina: 1=Yes, 0=No |
| oldpeak | Numeric | 0.0-6.2 | ST depression induced by exercise |
| slope | Categorical | 0, 1, 2 | Slope of peak exercise ST segment |
| ca | Categorical | 0, 1, 2, 3 | Major vessels colored by fluoroscopy |
| thal | Categorical | 0, 1, 2 | Thalassemia type (see below) |
| target | Categorical | 0, 1 | **0=No Disease, 1=Disease Present** |

---

## Categorical Column Value Meanings

### cp — Chest Pain Type
```
0 → Typical Angina (classic heart-related chest pain)
1 → Atypical Angina (heart-related but unusual presentation)
2 → Non-Anginal Pain (not heart-related chest pain)
3 → Asymptomatic (no chest pain!)
```

### restecg — Resting ECG Results
```
0 → Normal
1 → ST-T wave abnormality (possible heart stress)
2 → Left ventricular hypertrophy (enlarged heart!)
```

### slope — ST Segment Slope
```
0 → Upsloping (generally healthy!)
1 → Flat (borderline concerning)
2 → Downsloping (most concerning!)
```

### thal — Thalassemia Type
```
0 → Normal
1 → Fixed Defect (permanent blood flow issue)
2 → Reversible Defect (blood flow issue during stress)
```

---

## What is ST Depression (oldpeak)?

The heart's electrical activity creates waves measured by ECG.
The ST segment appears between the S and T waves.

During exercise, a healthy heart maintains a flat ST segment.
A diseased heart shows ST depression — the segment drops below baseline.

```
oldpeak = 0.0 → No depression → Healthy response! ✅
oldpeak = 2.5 → Significant drop → Concerning! ⚠️
oldpeak = 5.0+ → Large drop → Serious risk! 🚨

32.5% of patients show oldpeak = 0 → completely valid!
These are healthy responders — no ST depression during exercise.
```

---

## Folder Structure

```
data/
├── raw/
│   └── heart.csv              ← NEVER MODIFY! Original preserved!
├── processed/
│   └── heart_disease_cleaned.csv  ← After cleaning pipeline
└── README.md                  ← This file!
```

### raw/heart.csv
- Original download from Kaggle
- Contains 1,025 rows (including 723 duplicates!)
- NEVER modify this file — source of truth!

### processed/heart_disease_cleaned.csv
- Output of cleaning pipeline
- 302 unique patient records
- Category dtypes applied
- Ready for analysis and modeling

---

## Key Statistics

```
Target Distribution:
→ Disease Present (1): 164 patients (54.3%)
→ No Disease (0):      138 patients (45.7%)
→ Near-perfect balance! No class imbalance handling needed!

Age:
→ Min: 29 years, Max: 77 years
→ Average: 54.4 years
→ Disease group average: 52.59 years
→ No disease group average: 56.60 years

Cholesterol:
→ Min: 126 mg/dl, Max: 564 mg/dl (extreme outlier!)
→ Average: 246.50 mg/dl (High Risk territory!)

Max Heart Rate:
→ Disease group average: 158.38 bpm
→ No disease group average: 139.10 bpm
→ 19.28 bpm difference — strongest predictor!
```

---

## Data Cleaning Steps Applied

```
1. Removed 723 duplicate rows (70.5% of raw data!)
2. Confirmed zero missing values in all 14 columns
3. Converted 9 columns from int to category dtype:
   sex, cp, fbs, restecg, exang, slope, ca, thal, target
4. Validated no impossible values:
   → No zero cholesterol ✅
   → No zero blood pressure ✅
   → oldpeak zeros are medically valid ✅
5. Saved clean data to processed/ folder
```

---

## Citation

If you use this dataset, please cite:

```
Detrano, R., Janosi, A., Steinbrunn, W., Pfisterer, M., 
Schmid, J., Sandhu, S., Guppy, K., Lee, S., & Froelicher, V. 
(1989). International application of a new probability algorithm 
for the diagnosis of coronary artery disease. 
American Journal of Cardiology, 64, 304-310.
```

---

*Data README — Project 08 Healthcare Capstone*
*Prajwal Kondala | IIT KGP → AI/ML Engineer | April 2026*
