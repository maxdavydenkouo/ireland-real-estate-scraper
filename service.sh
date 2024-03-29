#!/bin/bash

# Check if no arguments are provided
if [[ $# -eq 0 ]]; then
  echo "No arguments provided. Usage: $0 [arg1] [arg2] ..."
  return
fi

# Handle different input arguments
case $1 in
  "start")
    echo "start service..."
    nohup venv/bin/python3 src/app.py &
    return
    ;;
  "stop")
    echo "shutdown service..."
    curl -X POST localhost:8080/shutdown
    ;;
  "restart")
    echo "shutdown service..."
    curl -X POST localhost:8080/shutdown
    sleep 5
    echo "start service..."
    nohup venv/bin/python3 src/app.py &
    ;;
  *)
    echo "Invalid argument '$1'. Please provide a valid argument."
    return
    ;;
esac
