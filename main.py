import os
import time
import datetime
import requests
import pandas as pd
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

# Global variables for scheduling
last_alert_time = None
ALERT_INTERVAL = 3600  # 1 hour in seconds

def should_send_alert():
    """Check if it's time to send an alert"""
    global last_alert_time
    now = time.time()
    if last_alert_time is None:
        return True
    return (now - last_alert_time) >= ALERT_INTERVAL

def check_and_send_alert():
    """Check if we should send an alert and send it if needed"""
    global last_alert_time
    if should_send_alert():
        send_insightpilot_alert()
        last_alert_time = time.time()
        return True
    return False

@app.before_request
def before_request():
    """Check for scheduled alerts before each request"""
    check_and_send_alert()

@app.route("/force-alert")
def force_alert():
    """Force send an alert immediately"""
    global last_alert_time
    send_insightpilot_alert()
    last_alert_time = time.time()
    return "Alert sent!"

if __name__ == "__main__":
    print("🎯 Starting InsightPilot...")
    print("📅 Alert system will check every request and send hourly alerts")
    print("🧪 Visit /force-alert to test Slack integration immediately")
    print("🧪 Visit /test-slack for another test endpoint")
    
    # Send initial alert
    print("📡 Sending initial alert...")
    send_insightpilot_alert()
    last_alert_time = time.time()
    
    print("🌐 Starting Flask app...")
    app.run(host="0.0.0.0", port=8080, debug=False)
