import threading
import time
import datetime
import requests
import schedule  # Move this to the top
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

def run_scheduler():
    print("🚀 Scheduler thread starting...")
    
    # Schedule the job
    schedule.every().hour.do(send_insightpilot_alert)
    
    # Also schedule a test message in 30 seconds for immediate testing
    schedule.every(30).seconds.do(send_insightpilot_alert).tag('test')
    
    print("📅 Jobs scheduled:")
    print("   - Every hour: send_insightpilot_alert")
    print("   - Test in 30 seconds: send_insightpilot_alert")
    
    while True:
        try:
            pending_jobs = schedule.get_jobs()
            if pending_jobs:
                next_run = min(job.next_run for job in pending_jobs)
                print(f"⏰ Next scheduled job at: {next_run}")
            
            schedule.run_pending()
            
            # Cancel the test job after it runs once
            if schedule.get_jobs('test'):
                test_jobs = schedule.get_jobs('test')
                for job in test_jobs:
                    if job.next_run <= datetime.datetime.now():
                        schedule.cancel_job(job)
                        print("🧪 Test job completed and removed")
            
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"❌ Scheduler error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    print("🎯 Starting InsightPilot...")
    
    # Start scheduler in background
    print("🔧 Starting scheduler thread...")
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Give the scheduler a moment to start
    time.sleep(2)
    
    print("🌐 Starting Flask app...")
    # Run Flask app
    app.run(host="0.0.0.0", port=8080, debug=False)