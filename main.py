import os
import time
import datetime
import requests
import pandas as pd
import schedule
import threading
from flask import Flask
from dotenv import load_dotenv

# 🔐 Load .env file for secure webhook storage
load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

app = Flask(__name__)

def send_insightpilot_alert():
    try:
        df_tasks = pd.read_csv("project_tasks_with_insights.csv")

        # Only select rows that contain an LLM Insight
        df_filtered = df_tasks[df_tasks['llm_insight'].notnull()]

        if df_filtered.empty:
            print("ℹ️ No insights to send today.")
            return

        message_text = "📢 *InsightPilot Daily Sprint Update*\n\n"

        for _, row in df_filtered.iterrows():
            message_text += (
                f"• Task `{row['task_id']}` is *{row['days_late']} days late*\n"
                f"  • Status: *{row['status']}* | Impact: *{row['client_impact']}*\n"
                f"  • 🧠 LLM Insight: {row['llm_insight']}\n\n"
            )

        response = requests.post(SLACK_WEBHOOK_URL, json={"text": message_text})
        if response.status_code == 200:
            print("✅ Slack digest sent with real insights.")
        else:
            print("❌ Failed to send Slack message:", response.text)

    except Exception as e:
        print("❌ Error while sending insights:", e)

@app.route("/")
def home():
    return "InsightPilot is running!"

@app.route("/test-slack")
def test_slack():
    """Manual endpoint to test Slack integration"""
    send_insightpilot_alert()
    return "Slack test sent! Check your logs."

@app.route("/force-alert")
def force_alert():
    """Force send an alert immediately"""
    send_insightpilot_alert()
    return "Alert sent!"

# 🔁 Daily Scheduler Thread for 9:00 AM France (07:00 UTC)
def schedule_daily_alert():
    schedule.every().day.at("07:00").do(send_insightpilot_alert)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    print("🎯 Starting InsightPilot...")
    print("📅 Daily alert will send at 9:00 AM France time (07:00 UTC)")
    print("🧪 Visit /force-alert or /test-slack to test manually")
    
    # Start background scheduler
    scheduler_thread = threading.Thread(target=schedule_daily_alert, daemon=True)
    scheduler_thread.start()

    # Initial run (optional)
    print("📡 Sending initial alert...")
    send_insightpilot_alert()

    print("🌐 Starting Flask app...")
    app.run(host="0.0.0.0", port=8080, debug=False)
