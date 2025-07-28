# main.py
import schedule
import time
import requests
import pandas as pd
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "InsightPilot Slack Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Start Flask in a separate thread
flask_thread = Thread(target=run_flask)
flask_thread.start()

# Example DataFrame — replace this with real data logic
example_df = pd.DataFrame({
    'Task ID': ['T001', 'T002'],
    'Status': ['In Progress', 'Blocked'],
    'Days Late': [3, 13],
    'Client Impact': ['High', 'Critical'],
    'LLM Insight': [
        'Contact assignee, escalate to client success.',
        'Escalate to tech team, update timeline.'
    ]
})

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Send Slack Message
def send_insightpilot_alert():
    df_filtered = example_df[example_df['LLM Insight'].notnull()]
    if df_filtered.empty:
        print("ℹ️ No insights to send today.")
        return

    message = "*🧠 InsightPilot Daily Sprint Update*\n\n"
    for _, row in df_filtered.iterrows():
        message += (
            f"• Task `{row['Task ID']}` – *{row['Days Late']} days late* – "
            f"Status: `{row['Status']}` – Impact: *{row['Client Impact']}*\n"
            f"  🔹 LLM Insight: {row['LLM Insight']}\n\n")

    response = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
    if response.status_code == 200:
        print("✅ Slack digest sent.")
    else:
        print("❌ Slack error:", response.text)

# Schedule alerts
schedule.every().day.at("08:00").do(send_insightpilot_alert)
schedule.every().day.at("16:00").do(send_insightpilot_alert)

# Keep the schedule running
while True:
    schedule.run_pending()
    time.sleep(60)
