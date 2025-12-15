# watcher.py
import os
import time
import shutil
from predictor import predict  # import the predictor module
from datetime import datetime

# -------------------------------
# Configuration
# -------------------------------
WATCH_DIR = "capture/live_csv"        # Folder where CICFlowMeter writes CSVs
PROCESSED_DIR = "processed/predicted" # Folder to move processed files
LOG_FILE = "alerts.log"               # Log file for attacks
SLEEP_INTERVAL = 1                     # Check folder every 1 second

# Create directories if they don't exist
os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# -------------------------------
# Logging function
# -------------------------------
def log_alert(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {message}\n")
    print(f"{timestamp} - {message}")

# -------------------------------
# Main watcher loop
# -------------------------------
def main():
    print("🟢 Starting live CSV watcher...")
    processed_files = set()  # keep track of already processed files

    while True:
        try:
            files = [f for f in os.listdir(WATCH_DIR) if f.endswith(".csv")]

            for file in files:
                if file in processed_files:
                    continue  # skip already processed files

                file_path = os.path.join(WATCH_DIR, file)

                try:
                    preds, probs, df_pred = predict(file_path)

                    # Check if any Attack detected
                    if "Attack" in df_pred['Prediction'].values:
                        attack_count = (df_pred['Prediction'] == "Attack").sum()
                        log_alert(f"⚠️ ATTACK detected in {file} | Count: {attack_count}")
                    else:
                        log_alert(f"✅ Normal traffic in {file}")

                    # Move file to processed folder
                    shutil.move(file_path, os.path.join(PROCESSED_DIR, file))
                    processed_files.add(file)

                except Exception as e:
                    log_alert(f"❌ Error processing {file}: {e}")

            time.sleep(SLEEP_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Watcher stopped by user.")
            break

        except Exception as e:
            log_alert(f"❌ Watcher encountered an error: {e}")
            time.sleep(SLEEP_INTERVAL)

# -------------------------------
# Entry point
# -------------------------------
if __name__ == "__main__":
    main()
