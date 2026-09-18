# ML MODEL REPORT — HUMAN FIREWALL NLP CLASSIFICATION PIPELINE

## 1. Dataset Overview

- **Total Rows:** `8,241`
- **Data Splits:**
  - **Train Set (70.0%):** `5,770` rows
  - **Validation Set (15.0%):** `1,234` rows
  - **Test Set (15.0% - Untouched Held-Out):** `1,237` rows
- **Binary Target (`manipulation_detected`):**
  - **Negative (`0`):** `5,403` (65.6%)
  - **Positive (`1`):** `2,838` (34.4%)
- **Source Breakdown:** Integrated from 5 open sources (`Mathur et al. 2019`, `ec-darkpattern yamanalab`, `Logical Fallacy Dataset`, `Clickbait Dataset`, `DarkPatternGuiltyFeeds`).

---

## 2. Data Quality & Leakage Audit

- **Exact & Near-Duplicate Removal:** Removed 378 exact duplicates and 322 near-duplicates during dataset preparation.
- **Leakage Prevention Invariant:**
  - `0` text clusters or normalized sentences cross boundaries between Train, Validation, or Test sets.
  - All metadata columns (`source_dataset`, `source_url`, `source_sample_id`, `content_type`, `sample_id`) are **100% excluded** from feature input. The model takes **ONLY raw text**.

---

## 3. Model Development & Iterative Experiments

| Iteration | Model Architecture | Feature Representation | Hyperparameters | Val Acc | Val Prec | Val Rec | Val F1 | ROC-AUC | PR-AUC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Iter 1 (Baseline)** | Logistic Regression | Word TF-IDF (1-2 n-grams) | `C=1.0`, thresh=`0.50` | 83.39% | 91.95% | 56.60% | 70.07% | 0.9028 | 0.8650 |
| **Iter 2** | Logistic Regression | Word + Char TF-IDF (Word 1-3 + Char 2-5) | `C=2.0`, `class_weight='balanced'`, thresh=`0.50` | 87.20% | 83.93% | 77.59% | 80.64% | 0.9322 | 0.9053 |
| **Iter 3 (Optimal)** | Logistic Regression | Word + Char TF-IDF (Word 1-3 + Char 2-5) | `C=2.0`, `class_weight='balanced'`, **thresh=`0.62`** | **87.44%** | **91.90%** | **69.58%** | **79.19%** | **0.9322** | **0.9053** |

---

## 4. Final Binary Classifier Performance (Test Set Evaluation)

The binary detector was evaluated on the **untouched held-out test set (1,237 rows)** at the optimal operating threshold of `0.62`:

- **Accuracy:** `86.66%`
- **Precision:** `90.65%` *(Extremely low false-positive rate: only 30 false alarms out of 811 benign test samples)*
- **Recall:** `68.31%`
- **F1-Score:** `77.91%`
- **ROC-AUC:** `0.9297`
- **PR-AUC:** `0.9060`

### Confusion Matrix (Test Set)
| Actual \ Predicted | Predicted Negative (0) | Predicted Positive (1) |
| :--- | :--- | :--- |
| **Actual Negative (0)** | **TN = 781** | **FP = 30** |
| **Actual Positive (1)** | **FN = 135** | **TP = 291** |

---

## 5. Secondary Manipulation Type Classifier Performance

Evaluated on positive manipulative test samples across 8 manipulation categories:

- **Accuracy:** `91.31%`
- **Macro F1-Score:** `89.71%`
- **Weighted F1-Score:** `91.27%`

### Per-Class Test Performance
| Manipulation Category | Test Samples | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- | :--- |
| `clickbait` | 180 | 0.98 | 0.98 | **0.98** |
| `social_pressure` | 50 | 0.94 | 0.92 | **0.93** |
| `general_persuasion` | 51 | 0.88 | 0.86 | **0.87** |
| `deceptive_choice` | 47 | 0.91 | 0.91 | **0.91** |
| `artificial_scarcity` | 41 | 0.93 | 0.93 | **0.93** |
| `urgency` | 32 | 0.85 | 0.88 | **0.86** |
| `emotional_manipulation` | 17 | 0.76 | 0.76 | **0.76** |
| `dark_pattern` | 8 | 0.75 | 0.75 | **0.75** |

---

## 6. Error Analysis & Key Improvements

1. **High Precision Target:** Tuned binary operating threshold from `0.50` to `0.62` to prevent annoying false-positive warnings on standard website copy, raising test precision to `90.65%`.
2. **Character N-Gram Support:** Sublinear TF-IDF character n-grams (2-5) enabled the model to catch subtle confirmshaming typography ("No thanks, I hate saving money") and short CTA countdown strings.

---

## 7. Production Inference & Artifacts

- **Model Artifacts Saved In:** `ml/models/`
  - [`binary_classifier.pkl`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/ml/models/binary_classifier.pkl)
  - [`binary_vectorizer.pkl`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/ml/models/binary_vectorizer.pkl)
  - [`secondary_classifier.pkl`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/ml/models/secondary_classifier.pkl)
  - [`secondary_vectorizer.pkl`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/ml/models/secondary_vectorizer.pkl)
  - [`config.json`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/ml/models/config.json)
- **Inference Entrypoint:** [`ml/src/predict.py`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/ml/src/predict.py)
- **FastAPI Integration:** Formatted to return `{ "manipulation_detected": bool, "confidence": float, "manipulation_type": str }`.

---

## 8. Final Recommendation
Use the trained **Word+Char TF-IDF + Logistic Regression pipeline** (`ml/models/`) in the FastAPI backend service (`backend/app/services/ml_service.py`) for low-latency, high-precision real-time detection in the Human Firewall browser extension.
