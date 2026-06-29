#!/bin/bash
python drift_service.py
evidently ui --host 0.0.0.0 --port 7888 --workspace /app/evidently_workspace