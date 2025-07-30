# InsightPilot – AI-Powered Signal Intelligence for Slack

**InsightPilot** is a fully automated system that delivers **daily AI insights** from project data directly into your Slack workspace. It's built specifically for:

- ✅ Account Managers
- ✅ Business Developers
- ✅ Project Managers

---

## 🔍 What It Does

Every day at **9:00 AM (France time)**, InsightPilot:
- Loads your project tasks enriched by LLMs
- Filters key signals (e.g. delays, blockers, risks)
- Sends a structured Slack message with insights & actions

---

## 🧠 Example Alert
📢 InsightPilot Daily Sprint Update

• Task T017 is 9 days late
• Status: Blocked | Impact: High
• 🧠 LLM Insight: Escalate to tech team and notify client success manager.

---
---

## 🛠️ How It Works (Architecture)

| Component           | Purpose                             |
|--------------------|-------------------------------------|
| `project_tasks_with_insights.csv` | Input data from your system or LLM analysis |
| `main.py`           | Flask app + alert logic            |
| `schedule`          | Runs alert at 9AM daily             |
| `Slack Webhook`     | Delivers insights to a channel      |
| `Render.com`        | Keeps the bot live 24/7             |
| `.env`              | Stores secret Slack webhook securely|

---

## 🧰 Tech Stack

- Python
- Flask
- Pandas
- python-dotenv
- schedule
- Slack Webhook
- Render (Free Tier)

---

## 📦 Installation (Dev Setup)

1. Clone this repo  
2. Create a `.env` file:
    ```
    SLACK_WEBHOOK_URL=your_webhook_url_here
    ```
3. Add your task file: `project_tasks_with_insights.csv`  
4. Run locally:
    ```bash
    pip install -r requirements.txt
    python main.py
    ```

---

## ☁️ Deploy to Render

1. Connect repo to Render
2. Add `SLACK_WEBHOOK_URL` under **Environment Variables**
3. Set **Start Command**: `python main.py`
4. Done – Render keeps it running & alerts fire daily at 09:00 France time

---

## 💼 Why This Matters (For You)

| Role              | Value Gained                          |
|-------------------|---------------------------------------|
| Account Managers  | No need to manually track or report status updates  
| Business Developers | Spot risks early without digging into CRMs  
| Project Managers  | Escalate blockers and act fast using AI-generated actions  

---

## 👀 Want to See a Live Test?

Visit your Render app endpoint:

- `/test-slack` → Send a test alert now  
- `/force-alert` → Force a full alert manually  

---

## 🚀 Status

InsightPilot is now fully deployed, secured, and runs **automated daily Slack alerts at 9AM France time**.  
Stay informed, act faster, and never miss a signal.

---
Made with ☕ + 🤖 by Reem BOUQUEAU 
