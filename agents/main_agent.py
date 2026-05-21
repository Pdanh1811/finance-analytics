import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.alert_agent import detect_anomalies, generate_alert
from agents.insight_agent import get_fraud_summary, generate_insight
from agents.telegram_agent import send_fraud_alert, send_insight
from datetime import datetime

async def run_pipeline():
    print("="*50)
    print(f"🚀 PIPELINE BẮT ĐẦU — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("="*50)

    # BƯỚC 1: Phát hiện anomaly
    print("\n🔍 Bước 1: Phát hiện anomaly...")
    anomalies, mean, std, df = detect_anomalies()
    
    if anomalies:
        alerts = generate_alert(anomalies, mean, std)
        for a in alerts:
            print(a['message'])
        await send_fraud_alert(alerts, mean)
    else:
        print("✅ Không có anomaly!")

    # BƯỚC 2: Sinh AI insight
    print("\n🤖 Bước 2: Sinh AI insight...")
    data    = get_fraud_summary()
    insight = generate_insight(data)
    print(insight[:200] + "...")
    await send_insight(insight)

    print("\n✅ PIPELINE HOÀN THÀNH!")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
