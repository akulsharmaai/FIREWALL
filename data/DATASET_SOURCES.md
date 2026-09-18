# DATASET SOURCES DOCUMENTATION

## 1. Overview
The `FINAL_MASTER_DATASET.csv` (located in `data/`) integrates 5 distinct real-world open-source datasets to train the **Human Firewall** machine learning models.

---

## 2. Source Breakdown & Licensing

| Source Dataset Name | Primary Domain / Context | Contributed Rows | License / Access Status | Mapped Categories |
| :--- | :--- | :--- | :--- | :--- |
| **Mathur et al. 2019 / yamanalab ec-darkpattern** | E-Commerce Web Pages | 1,008 | MIT / Open Academic | Artificial Scarcity, Urgency, Social Pressure, Deceptive Choice, Dark Patterns |
| **ec-darkpattern Negatives (yamanalab)** | E-Commerce & General Web | 1,167 | MIT / Open Academic | Non-manipulative UI elements, product descriptions, privacy notices |
| **Logical Fallacy Dataset (Jin et al. / tasksource)** | Articles, News, Rhetoric | 3,396 | CC-BY 4.0 / Open Access | Digital Persuasion, Emotional Manipulation, Negative Controls |
| **Clickbait Dataset (christinacdl / HuggingFace)** | News & Social Headlines | 2,400 | Open / Public | Clickbait attention traps, Curiosity Gap (Balanced 1:1 manipulative vs non-clickbait news) |
| **DarkPatternGuiltyFeeds (HuggingFace)** | Web Pop-ups & Banners | 270 | Open Access | Confirmshaming, Guilt/Shame-based deceptive choice UI options |

---

## 3. Storage Location
All dataset files and supporting metadata are located in the `data/` directory:
- [`data/FINAL_MASTER_DATASET.csv`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/data/FINAL_MASTER_DATASET.csv)
- [`data/DATASET_SOURCES.md`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/data/DATASET_SOURCES.md)
- [`data/LABEL_MAPPING.md`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/data/LABEL_MAPPING.md)
- [`data/DATA_QUALITY_REPORT.md`](file:///c:/Users/acous/Desktop/projects/FIREWALL_ML/data/DATA_QUALITY_REPORT.md)
