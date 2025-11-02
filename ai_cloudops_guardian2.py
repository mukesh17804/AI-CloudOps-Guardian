import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pyttsx3
import random
import time
from datetime import datetime

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 165)  # slower, clear voice
engine.setProperty('volume', 1.0)

# Simulated AWS resource data (demo mode)
def generate_demo_data():
    services = ['EC2 Instances', 'S3 Storage', 'Lambda Functions', 'RDS Databases', 'IAM Users']
    cpu_usage = [random.randint(20, 95) for _ in services]
    cost = [random.uniform(100, 700) for _ in services]
    risk_level = []
    for c in cpu_usage:
        if c > 85:
            risk_level.append('High')
        elif c > 60:
            risk_level.append('Medium')
        else:
            risk_level.append('Low')
    data = pd.DataFrame({
        'Service': services,
        'CPU Usage (%)': cpu_usage,
        'Cost (USD)': [round(c, 2) for c in cost],
        'Risk Level': risk_level
    })
    return data

# Speak alert
def speak_alert(message):
    engine.say(message)
    engine.runAndWait()

# Dashboard UI
st.set_page_config(page_title="AI CloudOps Guardian", layout="wide")
st.title("🌩️ AI CloudOps Guardian")
st.subheader("AI-powered Cloud Risk Analyzer & Voice Alert Dashboard")

st.info("🔐 Running in Demo Mode (no real AWS credentials needed)")

# Sidebar controls
st.sidebar.header("⚙️ Control Panel")
refresh_rate = st.sidebar.slider("Auto-refresh every (seconds):", 5, 60, 15)
voice_alerts = st.sidebar.checkbox("Enable Voice Alerts", True)
st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 Created by Mukesh Kanna — Innovative AI Project")

# Generate data
data = generate_demo_data()

# Risk summary
high_risk_count = (data['Risk Level'] == 'High').sum()
medium_risk_count = (data['Risk Level'] == 'Medium').sum()
low_risk_count = (data['Risk Level'] == 'Low').sum()

# Display data
st.subheader("📊 Cloud Resource Metrics")
st.dataframe(data, use_container_width=True)

# Visualization
st.subheader("📈 Resource Utilization Overview")
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(data['Service'], data['CPU Usage (%)'], color=['red' if r == 'High' else 'orange' if r == 'Medium' else 'green' for r in data['Risk Level']])
ax.set_ylabel("CPU Usage (%)")
ax.set_xlabel("AWS Service")
ax.set_title("AI CloudOps Guardian: Risk Visualization")
st.pyplot(fig)

# Logs dashboard
st.subheader("🧾 Real-time Log Dashboard")
log_area = st.empty()

# Generate fake logs
log_messages = []
for i in range(5):
    ts = datetime.now().strftime("%H:%M:%S")
    service = random.choice(data['Service'])
    level = random.choice(["INFO", "WARNING", "ALERT"])
    msg = f"[{ts}] [{level}] {service} check completed."
    log_messages.append(msg)
log_df = pd.DataFrame(log_messages, columns=["Logs"])
log_area.table(log_df)

# Voice alerts
if voice_alerts:
    if high_risk_count > 0:
        speak_alert(f"Alert! {high_risk_count} high risk services detected.")
    elif medium_risk_count > 0:
        speak_alert(f"Attention! {medium_risk_count} services need optimization.")
    else:
        speak_alert("All systems stable. No risks found.")
        speak_alert("Good job, Mukesh. Cloud is healthy now.")

# Summary metrics
st.subheader("📉 AI Risk Summary")
col1, col2, col3 = st.columns(3)
col1.metric("High Risk", high_risk_count)
col2.metric("Medium Risk", medium_risk_count)
col3.metric("Low Risk", low_risk_count)

# Refresh simulation
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh Now"):
    st.experimental_rerun()

# Footer
st.markdown("---")
st.caption("🧠 Powered by Streamlit • AI CloudOps Guardian • Voice Integrated Cloud Risk Monitor (Demo Mode)")
