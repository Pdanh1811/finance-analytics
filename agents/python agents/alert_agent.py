import duckdb
import numpy as np
from datetime import datetime

DATA_PATH = r"C:\Users\Admin\finance-analytics\data\fraudTrain.csv"

def detect_anomalies() -> list:
    con = duckdb.connect()
    con.execute(f"CREATE VIEW transactions AS SELECT * FROM read_csv_auto('{DATA_PATH}')")
    
    # Lấy fraud rate theo từng giờ
    df = con.execute("""
        SELECT 
            EXTRACT(hour FROM CAST(trans_date_trans_time AS TIMESTAMP)) AS hour,
            COUNT(*)                        AS total,
            SUM(is_fraud)                   AS fraud_count,
            ROUND(AVG(is_fraud)*100, 2)     AS fraud_rate
        FROM transactions
        GROUP BY hour
        ORDER BY hour
    """).df()
    
    # Tính Z-score để phát hiện anomaly
    mean = df['fraud_rate'].mean()
    std  = df['fraud_rate'].std()
    df['z_score'] = (df['fraud_rate'] - mean) / std
    
    # Flag những giờ có Z-score > 2 (bất thường)
    anomalies = df[df['z_score'] > 2].to_dict(orient='records')
    
    return anomalies, mean, std, df

def generate_alert(anomalies, mean, std):
    alerts = []
    
    for a in anomalies:
        severity = "🔴 CRITICAL" if a['z_score'] > 3 else "🟡 WARNING"
        alert = {
            "severity"   : severity,
            "hour"       : int(a['hour']),
            "fraud_rate" : a['fraud_rate'],
            "z_score"    : round(a['z_score'], 2),
            "fraud_count": int(a['fraud_count']),
            "message"    : f"{severity} | Giờ {int(a['hour']):02d}:00 — Fraud rate {a['fraud_rate']}% (Z-score: {round(a['z_score'],2)}) — Cao hơn trung bình {round(a['fraud_rate']/mean, 1)}x"
        }
        alerts.append(alert)
    
    return alerts

if __name__ == "__main__":
    print("🔍 Đang phân tích anomaly...")
    anomalies, mean, std, df = detect_anomalies()
    
    print(f"\n📊 Fraud rate trung bình: {mean:.2f}%")
    print(f"📊 Độ lệch chuẩn (std):  {std:.2f}%")
    print(f"📊 Ngưỡng alert (mean + 2*std): {mean + 2*std:.2f}%")
    
    if anomalies:
        alerts = generate_alert(anomalies, mean, std)
        print(f"\n⚠️  Phát hiện {len(alerts)} anomaly:\n")
        for a in alerts:
            print(a['message'])
    else:
        print("\n✅ Không phát hiện anomaly nào!")
    
    # Lưu report
    with open(r"C:\Users\Admin\finance-analytics\reports\anomaly_report.txt", "w", encoding="utf-8") as f:
        f.write(f"ANOMALY REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Mean fraud rate: {mean:.2f}%\n")
        f.write(f"Std: {std:.2f}%\n\n")
        if anomalies:
            for a in generate_alert(anomalies, mean, std):
                f.write(a['message'] + "\n")
    
    print("\n✅ Đã lưu vào reports/anomaly_report.txt")