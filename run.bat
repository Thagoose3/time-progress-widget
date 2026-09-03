@echo off
cd /d "%~dp0"
if exist "C:\Users\pooth\AppData\Local\Programs\Python\Python312\pythonw.exe" (
    start "" "C:\Users\pooth\AppData\Local\Programs\Python\Python312\pythonw.exe" "C:\Users\pooth\.gemini\antigravity\scratch\time-progress-widget\widget.py"
) else (
    start pythonw widget.py
)
exit
