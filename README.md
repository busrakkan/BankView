# BankView
Comprehensive customer and product analytics for business decision support. BankView extracts, cleans, and models banking data to calculate KPIs, visualize trends, and provide actionable insights for retail and SME banking.

## 📊 Dataset

### Source
The dataset used in this project is the **Bank Marketing Dataset**, publicly available on Kaggle.  
It contains data related to direct marketing campaigns (phone calls) of a retail banking institution, aimed at predicting whether a client subscribes to a term deposit.

The dataset was downloaded as a ZIP file and extracted into the `data/raw/` directory, following data engineering best practices.

---

### Dataset Structure
Each row represents a **customer interaction during a marketing campaign**, including customer demographics, financial information, and campaign-related attributes.

- **Number of records:** 11,162  
- **Number of features:** 17  

---

### Schema Overview

| Column | Description |
|------|------------|
| `age` | Age of the customer |
| `job` | Type of job |
| `marital` | Marital status |
| `education` | Education level |
| `default` | Has credit in default |
| `balance` | Average yearly account balance |
| `housing` | Has housing loan |
| `loan` | Has personal loan |
| `contact` | Contact communication type |
| `day` | Day of last contact |
| `month` | Month of last contact |
| `duration` | Duration of last contact (seconds) |
| `campaign` | Number of contacts during the campaign |
| `pdays` | Days since last contact |
| `previous` | Number of previous contacts |
| `poutcome` | Outcome of the previous marketing campaign |
| `deposit` | Target variable indicating subscription to a term deposit |

---

### Notes on Data Modeling
- The dataset does not include a unique customer identifier.
- For the purposes of this project, **each row is treated as a unique customer record**.
- Date information (`day`, `month`) will be combined into a derived date field during data transformation.
- The dataset is well-suited for customer segmentation, KPI calculation, and business decision support analytics.

---

### Data Organization
- `data/raw/`: Original dataset as downloaded from Kaggle (unchanged)
- `data/processed/`: Cleaned and transformed datasets used for analysis and modeling
