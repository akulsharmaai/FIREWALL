# DATA QUALITY & LEAKAGE PREVENTION REPORT

## 1. Final Dataset & Split Summary Statistics

- **Total Dataset Size:** `8,241` rows
- **Number of Source Datasets:** `5` open datasets.
- **Split Distribution:**
  - **Train Set (70.0%):** 5,770 rows
  - **Validation Set (15.0%):** 1,234 rows
  - **Test Set (15.0% - HELD OUT UNTOUCHED):** 1,237 rows

---

## 2. Zero-Leakage Verification Report

> [!IMPORTANT]
> **Zero-Leakage Invariant:**
> Text clusters and near-duplicate normalized groups were grouped prior to splitting. **Zero (0) text clusters or normalized text strings cross boundaries between Train, Validation, or Test sets.**

| Cross-Split Boundary Check | Crossing Groups Count | Leakage Status |
| :--- | :--- | :--- |
| **Train ↔ Validation** | `0` | ✅ PASSED |
| **Train ↔ Test** | `0` | ✅ PASSED |
| **Validation ↔ Test** | `0` | ✅ PASSED |
| **Total Crossing Groups** | `0` | ✅ PASSED |

---

## 3. Split Distributions

### A. Binary Class Distribution (`manipulation_detected`)

| Split Name | Total Rows | Positive (1) | Negative (0) | Positive % | Negative % |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | 5,770 | 1,988 | 3,782 | 34.45% | 65.55% |
| **Validation** | 1,234 | 424 | 810 | 34.36% | 65.64% |
| **Test** | 1,237 | 426 | 811 | 34.44% | 65.56% |

### B. Secondary Category Distribution (`manipulation_type`)

| Category (`manipulation_type`) | Train Count | Validation Count | Test Count | Total Count |
| :--- | :--- | :--- | :--- | :--- |
| `none` | 3,782 | 810 | 811 | **5,403** |
| `clickbait` | 840 | 180 | 180 | **1,200** |
| `social_pressure` | 246 | 56 | 50 | **352** |
| `general_persuasion` | 232 | 48 | 51 | **331** |
| `deceptive_choice` | 218 | 47 | 47 | **312** |
| `artificial_scarcity` | 212 | 47 | 41 | **300** |
| `urgency` | 142 | 26 | 32 | **200** |
| `emotional_manipulation` | 71 | 16 | 17 | **104** |
| `dark_pattern` | 27 | 4 | 8 | **39** |

---

## 4. Reproducibility & Saved Split Artifacts

To guarantee 100% exact reproducibility during ML model training:
1. [`data/FINAL_MASTER_DATASET_SPLIT.csv`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/data/FINAL_MASTER_DATASET_SPLIT.csv) — Contains the dataset with the `split` column (`train`, `val`, `test`).
2. [`data/dataset_splits.csv`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/data/dataset_splits.csv) — Mapping file storing `sample_id` -> `split`.
