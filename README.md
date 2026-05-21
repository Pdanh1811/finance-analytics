# 🏦 Credit Card Fraud Analytics Pipeline

> End-to-end analytics project phân tích gian lận thẻ tín dụng  
> với Python, SQL, Power BI và AI Agent tự động hóa

---

## 📌 Tổng quan

Project mô phỏng quy trình làm việc thực tế của một **Data Analyst** tại công ty Fintech/Ngân hàng — từ khám phá dữ liệu, phân tích SQL, xây dựng dashboard đến tự động hóa báo cáo bằng AI.

**Dataset:** [Credit Card Fraud Detection — Kaggle](https://www.kaggle.com/datasets/kartik2112/fraud-detection)  
**Quy mô:** 1,296,675 giao dịch · 23 cột · 2 năm dữ liệu

---

## 🎯 Key Insights

| #   | Insight                      | Chi tiết                               |
| --- | ---------------------------- | -------------------------------------- |
| 1   | **Fraud rate tổng thể**      | 0.58% — 7,506 vụ / 1.2M giao dịch      |
| 2   | **Khung giờ nguy hiểm nhất** | 22h-23h chiếm ~50% tổng fraud          |
| 3   | **Category rủi ro cao nhất** | shopping_net (1.76%), misc_net (1.45%) |
| 4   | **Thiệt hại trung bình/vụ**  | $531 — gấp 8x giao dịch bình thường    |
| 5   | **Khu vực rủi ro nhất**      | NY (555 vụ), TX (479 vụ), PA (458 vụ)  |

---

## 🏗️ Kiến trúc Pipeline

```
Raw Data (CSV)
      ↓
Ingestion & Cleaning (pandas)
      ↓
SQL Analysis (DuckDB)
      ↓
  ┌───────────────────┐
  │   AI Agent Layer  │
  │ • Insight Agent   │ → LLM báo cáo tiếng Việt
  │ • Alert Agent     │ → Z-score anomaly detection
  │ • Telegram Bot    │ → Alert tự động
  └───────────────────┘
      ↓
Power BI Dashboard (3 trang)
```

---

## 📁 Cấu trúc thư mục

```
finance-analytics/
├── agents/
│   ├── insight_agent.py    # LLM tự động viết báo cáo
│   ├── alert_agent.py      # Phát hiện anomaly bằng Z-score
│   ├── telegram_agent.py   # Gửi alert qua Telegram
│   └── main_agent.py       # Chạy toàn bộ pipeline
├── data/                   # Dataset (không push lên GitHub)
├── dashboard/
│   └── fraud_analytics_report.pbix  # Power BI report
├── notebooks/
│   ├── 01_EDA.ipynb         # Exploratory Data Analysis
│   └── 02_SQL_Analysis.ipynb # SQL với DuckDB
├── reports/
│   ├── EDA_Report.html      # Báo cáo EDA dạng HTML
│   ├── fraud_by_category.csv
│   ├── fraud_by_hour.csv
│   ├── fraud_by_state.csv
│   ├── fraud_kpi.csv
│   └── ai_insight.txt       # AI-generated report
├── .env.example             # Template biến môi trường
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer             | Công cụ                 | Mục đích                        |
| ----------------- | ----------------------- | ------------------------------- |
| Data Processing   | `pandas`, `numpy`       | Clean & transform data          |
| SQL Analytics     | `DuckDB`                | Window functions, aggregation   |
| Visualization     | `matplotlib`, `seaborn` | EDA charts                      |
| BI Dashboard      | `Power BI`              | Interactive business report     |
| AI/LLM            | `Groq API` (Llama 3.3)  | Auto-generate insights          |
| Anomaly Detection | `scipy` Z-score         | Alert khi fraud rate bất thường |
| Notification      | `python-telegram-bot`   | Gửi alert tự động               |
| Version Control   | `Git`, `GitHub`         | Source control                  |

---

## 🚀 Hướng dẫn chạy

### 1. Clone repo

```bash
git clone https://github.com/Pdanh1811/finance-analytics.git
cd finance-analytics
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv
venv\Scripts\activate.bat  # Windows
```

### 3. Cài thư viện

```bash
pip install -r requirements.txt
```

### 4. Cấu hình biến môi trường

```bash
cp .env.example .env
# Điền API key vào file .env
```

### 5. Tải dataset

Tải từ [Kaggle](https://www.kaggle.com/datasets/kartik2112/fraud-detection) → đặt vào thư mục `data/`

### 6. Chạy pipeline

```bash
# Chạy toàn bộ pipeline
python agents/main_agent.py

# Hoặc chạy từng phần
python agents/insight_agent.py   # AI insight
python agents/alert_agent.py     # Anomaly detection
```

---

## 📊 Dashboard Preview

**Trang 1 — Overview:** KPI cards + Fraud rate theo category & giờ  
**Trang 2 — Fraud Analysis:** Top states + Detail table  
**Trang 3 — Geography:** Map visualization theo bang

---

## 📈 Kết quả phân tích

- Phát hiện **2 anomaly** tại 22h (Z-score: 2.65) và 23h (Z-score: 2.60)
- AI tự động sinh báo cáo tiếng Việt gửi qua Telegram mỗi khi chạy pipeline
- Export 4 file CSV sạch sẵn sàng kết nối Power BI

---

## 👤 Author

**Duc Anh** — Data Analyst  
📧 ducanhphan1909@gmail.com

---

_Project này được xây dựng với mục đích học tập và thể hiện kỹ năng DA thực tế._
