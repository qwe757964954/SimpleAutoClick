@echo off
setlocal

rem Set Python executable path
set "PYTHON_PATH=C:\Python38\python.exe"

rem Set script path
set "SCRIPT_PATH=D:\Projects\MyScript\lian.py"

rem Change to script directory
cd /d %~dp0

rem Execute the Python script
"%PYTHON_PATH%" "%SCRIPT_PATH%"

endlocal
pause
