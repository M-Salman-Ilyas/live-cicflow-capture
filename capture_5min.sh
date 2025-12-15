#!/bin/bash

# ----------------------------------
# Configuration
# ----------------------------------
VENV_PYTHON="/home/tayyab/cic_env/bin/python3"
INTERFACE="ens33"
OUT_DIR="/home/tayyab/ddos_ids/capture/live_csv"
DURATION=300   # 5 minutes = 300 seconds

# ----------------------------------
# Ensure output directory exists
# ----------------------------------
mkdir -p "$OUT_DIR"

echo "🚀 Starting CICFlowMeter live capture (5-minute rotation)"
echo "📁 Output directory: $OUT_DIR"
echo "🛑 Press Ctrl+C to stop"

# ----------------------------------
# Infinite loop
# ----------------------------------
while true
do
    TIMESTAMP=$(date +%Y%m%d_%H%M)
    OUT_FILE="$OUT_DIR/flows_$TIMESTAMP.csv"

    echo "🕒 Capturing traffic to $OUT_FILE"

    sudo $VENV_PYTHON -m cicflowmeter.sniffer \
        -i $INTERFACE \
        -c "$OUT_FILE" &
    
    PID=$!

    # Let it run for 5 minutes
    sleep $DURATION

    # Stop cicflowmeter gracefully
    sudo kill $PID

    echo "✅ Finished capture: $OUT_FILE"
    echo "--------------------------------------"
done
