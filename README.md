# Crane Game Log Checker

A Python script to validate and check Crane Game log files (Excel or CSV format) for data consistency and correctness.

## Installation

### 1. Clone the Repository

**💡 Recommendation:** It's recommended to clone git repositories in a directory that is easy to find, such as your Windows home directory (`C:\Users\<yourusername>`) or a dedicated projects folder within it. This makes it easier to locate and manage your repositories.

Open **PowerShell** and navigate to your Windows home directory:

```powershell
cd C:\Users\<yourusername>
```

**⚠️ Important:** Replace `<yourusername>` with your actual Windows username! For example, if your username is `john`, use:
```powershell
cd C:\Users\john
```

Then clone the repository:
```powershell
git clone <repository-url> CraneGame
cd CraneGame
```

### 2. Set Up Python Environment

The project includes a virtual environment in the `crane` directory. Activate it:

```powershell
.\crane\Scripts\Activate.ps1
```

If you need to install dependencies manually:
```powershell
pip install pandas openpyxl colorama IPython
```

## Usage

### Option 1: Run with Python (One-time use)

Activate the virtual environment and run the script:

```powershell
.\crane\Scripts\Activate.ps1
python check_crane_game_log.py
```

To check a specific log file:
```powershell
python check_crane_game_log.py "path\to\your\logfile.xlsx"
python check_crane_game_log.py "path\to\your\logfile.csv"
```

### Option 2: Create a Batch File (Recommended for frequent use)

If you'll be using this script frequently, create a `.bat` file for quick access. Create a file named `check_crane_game_log.bat` in the project root with the following content:

```batch
@echo off
REM Wrapper script for check_crane_game_log.py
REM Usage: check_crane_game_log.bat [file_path]

set PYTHON_EXE=C:\Users\<yourusername>\CraneGame\crane\Scripts\python.exe
set PYTHON_SCRIPT=C:\Users\<yourusername>\CraneGame\check_crane_game_log.py

REM If a file path argument is provided, pass it to Python
if "%~1"=="" (
    "%PYTHON_EXE%" "%PYTHON_SCRIPT%"
) else (
    "%PYTHON_EXE%" "%PYTHON_SCRIPT%" "%~1"
)

pause
```

**⚠️ Important:** Replace `<yourusername>` in the batch file with your actual Windows username!

Then you can simply double-click the `.bat` file or run it from PowerShell:
```powershell
.\check_crane_game_log.bat
```

Or with a specific file:
```powershell
.\check_crane_game_log.bat "logs\your_logfile.xlsx"
.\check_crane_game_log.bat "logs\your_logfile.csv"
```

## What the Script Checks

The script performs several validation checks on your log file:

- **NrSlips Total**: Verifies that NrSlips equals the sum of other slip columns
- **TotalDropped Equals Slips**: Checks that TotalDropped equals the sum of all slip columns
- **Stress Dropped**: Compares items dropped during stress vs non-stress periods
- **Velocity Comparison**: Ensures non-slip trials have faster velocity than slip trials
- **Stress Block Velocity**: Compares velocity between StressBlock and NonStressBlock
- **Stress Block Balance**: Verifies equal counts of StressBlock and NonStressBlock when Training is FALSE
- **Slip Trial Slips**: Confirms Slip Trials have more total slips than non-slip trials
- **Trial Duration**: Calculates average trial duration and checks total duration

Results are displayed with color-coded output (green for OK, red for errors).

## Default Log File

By default, the script checks:
```
logs\20251181420_TEST_CraneOut.xlsx
```

You can override this by passing a file path as an argument. The script automatically detects and loads both Excel (`.xlsx`) and CSV (`.csv`) files.

