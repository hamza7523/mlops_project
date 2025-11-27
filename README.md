# MLOPS_Project
Application to detect plant diseases
Setting Up a auto testing CI
# Plant Disease Dataset - Evidently AI Dashboard

This repository contains data quality and drift monitoring dashboards for the [New Plant Diseases Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset).

## 📊 Dashboard Overview

The Evidently AI dashboard provides comprehensive monitoring of:
- Data drift detection between training and validation sets
- Feature distribution analysis (color channels, brightness, contrast)
- Data quality metrics (missing values, duplicates)
- Statistical tests for dataset stability

## 🎯 Key Results

- ✅ **Dataset Drift:** NOT detected (0% drifted columns)
- ✅ **Data Quality:** No missing values
- ✅ **Feature Stability:** All 17 features stable (drift < 0.05)
- ✅ **Dataset Split:** 3,800 training / 1,900 validation samples

## 📂 Files

- `data_drift_report.html` - Main Evidently AI dashboard (click to view)

## 🔍 How to View

1. Download the HTML file
2. Open it in your web browser
3. Interact with the dashboard (expand sections, view detailed metrics)

## 📈 Features Monitored

### Image Features:
- Color channels: mean_red, mean_green, mean_blue
- Color variation: std_red, std_green, std_blue
- Color ratios: red_ratio, green_ratio, blue_ratio
- Image quality: brightness, contrast
- File metadata: file_size_kb

### Classification Labels:
- class_name (38 plant disease categories)
- plant_type (Apple, Tomato, Corn, etc.)
- disease_type (specific disease or healthy)

## 🌱 Dataset Information

- **Source:** Kaggle - New Plant Diseases Dataset
- **Total Images:** 87,900 images
- **Classes:** 38 plant disease categories
- **Image Size:** 256×256 pixels

## 🛠️ Generated With

- **Tool:** Evidently AI v0.4.25
- **Python:** 3.12
- **Notebook:** Google Colab

## 📝 License

Dataset: [Database: Open Database, Contents: © Original Authors]
