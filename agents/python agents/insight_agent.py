import os
from groq import Groq
from dotenv import load_dotenv
import duckdb
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DATA_PATH = r"C:\Users\Admin\finance-analytics\data\fraudTrain.csv"

def get_fraud_summary():
    con = duckdb.connect()
    con.execute(f"CREATE VIEW transactions AS SELECT * FROM read_csv_auto('{DATA_PATH}')")
    
    summary = con.execute("""
        SELECT 
            COUNT(*)                                    AS total_transactions,
            SUM(is_fraud)                               AS total_fraud,
            ROUND(AVG(is_fraud) * 100, 2)               AS fraud_rate_pct,
            ROUND(SUM(CASE WHEN is_fraud=1 THEN amt ELSE 0 END), 2) AS total_fraud_amount,
            ROUND(AVG(CASE WHEN is_fraud=1 THEN amt END), 2)        AS avg_fraud_amount
        FROM transactions
    """).df()
    
    top_category = con.execute("""
        SELECT category, ROUND(AVG(is_fraud)*100,2) AS fraud_rate
        FROM transactions GROUP BY category
        ORDER BY fraud_rate DESC LIMIT 3
    """).df()
    
    top_hour = con.execute("""
        SELECT EXTRACT(hour FROM CAST(trans_date_trans_time AS TIMESTAMP)) AS hour,
               ROUND(AVG(is_fraud)*100,2) AS fraud_rate
        FROM transactions GROUP BY hour
        ORDER BY fraud_rate DESC LIMIT 3
    """).df()
    
    return {
        "summary": summary.to_dict(orient="records")[0],
        "top_categories": top_category.to_dict(orient="records"),
        "top_hours": top_hour.to_dict(orient="records")
    }

def generate_insight(data: dict) -> str:
    prompt = f"""
Bạn là một chuyên gia phân tích rủi ro tài chính tại ngân hàng.
Dựa vào số liệu sau, hãy viết một đoạn báo cáo ngắn gọn bằng tiếng Việt 
(khoảng 150-200 từ) theo phong cách chuyên nghiệp cho ban lãnh đạo:

SỐ LIỆU:
- Tổng giao dịch: {data['summary']['total_transactions']:,}
- Tổng fraud: {data['summary']['total_fraud']:,}
- Fraud rate: {data['summary']['fraud_rate_pct']}%
- Tổng thiệt hại: ${data['summary']['total_fraud_amount']:,}
- Trung bình/vụ: ${data['summary']['avg_fraud_amount']:,}

TOP 3 CATEGORY RỦI RO NHẤT:
{json.dumps(data['top_categories'], ensure_ascii=False, indent=2)}

TOP 3 GIỜ NGUY HIỂM NHẤT:
{json.dumps(data['top_hours'], ensure_ascii=False, indent=2)}

Yêu cầu:
1. Bắt đầu bằng tóm tắt tổng quan
2. Nêu các điểm rủi ro chính
3. Kết thúc bằng 2-3 khuyến nghị cụ thể
"""
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("🔄 Đang lấy dữ liệu...")
    data = get_fraud_summary()
    
    print("🤖 Đang sinh insight từ AI...")
    insight = generate_insight(data)
    
    print("\n" + "="*60)
    print("BÁO CÁO PHÂN TÍCH GIAN LẬN — AI GENERATED")
    print("="*60)
    print(insight)
    print("="*60)
    
    # Lưu ra file
    with open(r"C:\Users\Admin\finance-analytics\reports\ai_insight.txt", "w", encoding="utf-8") as f:
        f.write(insight)
    print("\n✅ Đã lưu vào reports/ai_insight.txt")