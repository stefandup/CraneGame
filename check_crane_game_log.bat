@echo off
REM Wrapper script for check_crane_game_log.py
REM Usage: check_crane_game_log.bat [file_path]

set PYTHON_EXE=C:\Users\stefan\Documents\Unreal Projects\UnrealPythonTools\CraneGame\crane\Scripts\python.exe
set PYTHON_SCRIPT=C:\Users\stefan\Documents\Unreal Projects\UnrealPythonTools\CraneGame\check_crane_game_log.py

REM If a file path argument is provided, pass it to Python
if "%~1"=="" (
    "%PYTHON_EXE%" "%PYTHON_SCRIPT%"
) else (
    "%PYTHON_EXE%" "%PYTHON_SCRIPT%" "%~1"
)

pause

