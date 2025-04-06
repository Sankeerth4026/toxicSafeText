@echo off
echo [✓] Starting WebSocket server...
start cmd /k python ws_sever.py

timeout /t 2 > nul

echo [✓] Starting Backend AI classifier...
start cmd /k python backend.py

timeout /t 2 > nul

echo [✓] Starting React + Electron app...
start cmd /k npm run start

timeout /t 3 > nul

echo [✓] Starting OCR sender (main.py)...
start cmd /k python main.py
