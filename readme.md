Project Structure & File Descriptions

This repository contains scripts for live network flow capture, CSV monitoring, and ML-based traffic analysis using CICFlowMeter.

Directory Structure
.
├── capture_5min.sh
├── watcher.py
├── predictor.py
├── requirements.txt
├── capture/
│   └── live_csv/
│       ├── flows_20251214_0745.csv
│       ├── flows_20251214_0750.csv
│       └── ...
└── README.md

File-by-File Explanation
capture_5min.sh
Purpose

Captures live network traffic using CICFlowMeter and automatically generates a new CSV file every 5 minutes.

 What it does

Listens on a specified network interface

Stops capture every 5 minutes

Saves output as timestamped CSV

Restarts capture automatically

▶️ How to run
sudo ./capture_5min.sh

Output

CSV files are stored in:

capture/live_csv/

2️capture/ (Directory)
 Purpose

Stores all captured flow CSV files.

 capture/live_csv/
 Purpose

Holds time-segmented flow data generated every 5 minutes.

📄 File naming format
flows_YYYYMMDD_HHMM.csv

📄 Example
flows_20251214_0745.csv
flows_20251214_0750.csv
flows_20251214_0755.csv



Machine learning pipelines

DDoS detection

Time-based traffic analysis

3️watcher.py
 Purpose

Continuously monitors the capture directory and automatically processes new CSV files as they are created.

What it does

Watches capture/live_csv/

Detects new CSV files

Sends new files to predictor.py

Prevents duplicate processing

How to run
python3 watcher.py


Run this in a separate terminal while capture is running.

Typical Logic (Conceptual)
Loop forever
 └── Check capture folder
     └── If new CSV found
         └── Call predictor.py

4️predictor.py
 Purpose

Loads a trained machine learning model and performs traffic classification / prediction on captured flow data.

 What it does

Reads CSV file passed by watcher.py

Preprocesses features

Loads ML model (e.g., .pkl)

Outputs predictions (benign / attack)

▶️ How it is used

predictor.py is not run directly by users.

It is called automatically by:

watcher.py → predictor.py

 Typical Logic (Conceptual)
load_model()
read_csv()
extract_features()
predict()
print_or_store_results()

5️requirements.txt
 Purpose

Lists all Python dependencies required to run watcher and predictor scripts.

 Example
pandas
numpy
scikit-learn
joblib

Install dependencies
pip3 install -r requirements.txt

Full Workflow (How Everything Works Together)
1. capture_5min.sh
   └── Captures live traffic
       └── Creates CSV every 5 minutes

2. watcher.py
   └── Detects new CSV file
       └── Sends file to predictor.py

3. predictor.py
   └── Classifies traffic
       └── Outputs detection result

Recommended Run Order
Terminal 1 – Start Capture
sudo ./capture_5min.sh

Terminal 2 – Start Watcher
python3 watcher.py

Important Notes

Ensure capture/live_csv exists before running

Run capture_5min.sh with sudo

Run Python scripts as normal user

Ensure sufficient disk space

Best Practices

Keep capture and prediction logs separate

Archive old CSV files daily

Monitor disk usage using:

df -h

📌 Intended Use

✔ Academic research
✔ DDoS detection experiments
✔ Network traffic analysis
✔ Dataset generation
