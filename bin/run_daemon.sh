#!/bin/bash

mkdir -p logs
# Kill the previously running process if any
kill -9 `cat logs/save_pid.txt`
# Cleanup the old files
rm nohup.out, logs/outputfile.log
# Start daemon script
nohup python3 service/service-daemon.py 2>&1 > logs/outputfile.log &
# Save PID
echo $! > logs/save_pid.txt
# Display immediate output
echo
echo "Waiting for daemon to start..."
echo
sleep 2 && tail logs/outputfile.log
