@echo off

REM Проверка, существует ли папка venv
if not exist venv (
    echo Virutual environment not found. Creating venv...
    python3 -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check and install dependencies
echo Checking dependencies...
python -m pip freeze > tmp_requirements.txt
fc tmp_requirements.txt requirements.txt > nul
if errorlevel 1 (
    echo Install dependencies...
    python -m pip install -r requirements.txt
) else (
    echo All dependencies are already installed.
)
del tmp_requirements.txt

REM Запуск скрипта
echo Starting client.py...
python client.py

pause