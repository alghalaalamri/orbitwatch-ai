# 🛰️ OrbitWatch AI

Real-time orbital wildfire detection using onboard satellite AI.

OrbitWatch AI simulates how next-generation Earth observation satellites can analyze imagery directly in orbit instead of transmitting every raw frame back to Earth.

The system performs onboard wildfire and smoke analysis, identifies high-risk imagery, and prioritizes only critical frames for downlink. This reduces bandwidth usage while enabling faster emergency response.

---

# Problem

Modern satellites continuously capture enormous amounts of Earth imagery.

However:

- Downlink bandwidth is limited
- Transmitting every frame is expensive
- Critical wildfire events may be delayed inside massive datasets

Traditional workflows rely heavily on ground-based analysis after transmission.

OrbitWatch AI moves inference directly onboard the satellite.

---

# Solution

OrbitWatch AI performs onboard image analysis using computer vision techniques to detect:

- wildfire-like regions
- smoke anomalies
- high-risk imagery

The satellite then decides whether the frame should:

- be immediately transmitted to Earth
- stored for review
- ignored to save bandwidth

---

# Why Onboard AI Matters

Earth observation satellites generate continuous streams of imagery.

Instead of transmitting all raw imagery:

OrbitWatch AI filters low-risk frames directly in orbit and prioritizes only important wildfire events.

This enables:

- faster emergency response
- reduced bandwidth usage
- scalable orbital monitoring
- more efficient Earth observation systems

---

# Features

- 🛰️ Satellite telemetry dashboard
- 🔥 Wildfire/smoke anomaly detection
- 📡 Simulated onboard inference
- 🚨 Priority downlink decision engine
- 📊 Risk scoring system
- 🖼️ Demo satellite imagery mode
- 🌍 Earth observation workflow simulation

---

# System Architecture

```text
Satellite Imagery
        ↓
Onboard AI Inference
        ↓
Wildfire / Smoke Analysis
        ↓
Risk Scoring Engine
        ↓
Priority Downlink Decision
        ↓
Emergency Alert to Earth
```

---

# Tech Stack

- Python
- Streamlit
- OpenCV
- NumPy
- Pillow

---

# Demo

1. Load a demo satellite frame or upload imagery
2. OrbitWatch AI analyzes wildfire/smoke risk
3. The system generates:
   - risk score
   - bandwidth optimization estimate
   - onboard transmission decision

---

# Built For

AI in Space Hackathon  
DPhi Space × Liquid AI