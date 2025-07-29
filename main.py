import threading
import time
import datetime
import requests
from flask import Flask

app = Flask(__name__)

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

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
            print(f"[{now}] ❌ Slack POST failed: {response.status_code}")
    except Exception as e:
        print(f"[{now}] ❌ Slack exception: {e}")

@app.route("/")
def home():
    return "InsightPilot is running!"

def run_scheduler():
    import schedule
    schedule.every().hour.do(send_insightpilot_alert)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Start scheduler in background
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # Run Flask app
    app.run(host="0.0.0.0", port=8080)
