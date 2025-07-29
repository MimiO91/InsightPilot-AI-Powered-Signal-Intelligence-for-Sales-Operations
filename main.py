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
        print(f"[{now}] 🔄 Sending Slack digest...")
        response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=10)
        if response.status_code == 200:
            print(f"[{now}] ✅ Slack digest sent successfully!")
        else:
            print(f"[{now}] ❌ Slack POST failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[{now}] ❌ Slack exception: {e}")

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
        # First run - send immediately
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
    # Run Flask app
    app.run(host="0.0.0.0", port=8080, debug=False)