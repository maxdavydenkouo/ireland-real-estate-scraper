#!/bin/bash

# Check if no arguments are provided
if [[ $# -eq 0 ]]; then
  echo "No arguments provided. Usage: $0 [arg1] [arg2] ..."
  return
fi

# Handle different input arguments
case $1 in
  "start")
    echo "starting service..."
    nohup venv/bin/python src/app.py >> app.log &
    return
    ;;
  "stop")
    echo "shutdown service..."
    curl -X POST localhost:8080/shutdown
    ;;
  *)
    echo "Invalid argument '$1'. Please provide a valid argument."
    return
    ;;
esac
