# VIT Interview UI

A PyQt6 desktop UI prototype for managing VIT course candidate interviews.

## Run on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

This is a front-end prototype. Candidate and interview entries exist only while
the application is open; there is no backend or persistent storage yet.
