@echo off

if not exist output\ mkdir output

if exist output\*.pdf del /f /q output\*.pdf

python main.py "BAB 05,24.pdf"

if not errorlevel 0 echo Exit code: %errorlevel%

pause