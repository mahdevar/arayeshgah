@echo off
SET PYTHONDONTWRITEBYTECODE=1
set FLASK_APP=app.py
set FLASK_DEBUG=1
set FLASK_RUN_HOST=0.0.0.0
SET FLASK_RUN_PORT=80

D:\Software\flask\Scripts\flask.exe run