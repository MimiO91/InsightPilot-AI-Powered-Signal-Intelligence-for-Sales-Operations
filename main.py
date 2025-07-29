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
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"✅ Ping received from UptimeRobot at {now}")
    try:
        with open("uptime_log.txt", "a") as f:
            f.write(f"Ping received at {now}\n")
    except Exception as e:
        print("❌ Failed to log ping:", e)
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
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = {
        "text": f"📡 InsightPilot Digest – {now}\n• Status: ✅ Online\n• Ping received."
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print(f"[{now}] ✅ Slack digest sent.")
        else:
            print(f"[{now}] ❌ Slack POST failed. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[{now}] ❌ Exception occurred while sending Slack message: {e}")

# Schedule alerts
schedule.every().hour.do(send_insightpilot_alert)

# Keep the schedule running
while True:
    try:
        schedule.run_pending()
    except Exception as e:
        print("❌ Scheduler error:", e)
    time.sleep(60)
