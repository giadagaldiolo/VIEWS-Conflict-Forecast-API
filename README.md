# JunctionHack Project Overview

This repository contains three sample projects:

1. **Face Detection + Emotion Recognition Demo (using face-api.js)**  
   A simple browser demo that performs real-time face detection and emotion recognition.

2. **Simple Web API Server with FastAPI**  
   Provides a root endpoint and a dummy weather forecast API.

3. **Anomaly Detection Sample (using IsolationForest)**  
   A Python script to detect anomalies from CSV data.

---

# How to Use

## 1. Face Detection + Emotion Recognition Demo

- Place `index.html`, `style.css`, and `script.js` in the same folder.
- Open `index.html` in a browser to see real-time face detection and emotion recognition using your camera.
- Required libraries are loaded via CDN.

---

## 2. FastAPI Web API

### How to Run

```bash
uvicorn main:app --reload
```
FastAPI code is in main.py.

### Endpoints
- /
<br>Returns a "Hello World" message.

- /api/forecast/{grid_id}
<br>Returns a dummy weather forecast (e.g., "Sunny") for the specified grid_id.

## 3. Anomaly Detection Script
Prepare a CSV file named sample_data.csv containing numerical columns.

Save the Python script as anomaly_detection.py and run:
```bash
python data_quality.py
```
It checks for missing values and prints anomalies detected by IsolationForest.

### Requirements
Python 3.7 or higher
Libraries:
- fastapi
- uvicorn
- pandas
- scikit-learn
### License
MIT License

uvicorn app.main:app --reload
