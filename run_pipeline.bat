@echo off
echo ======================================================================
echo SAYLANI MEDICAL HELP DESK - REFACTORED PIPELINE
echo JSON-Based Knowledge Base System
echo ======================================================================

echo.
echo [1/5] Cleaning Data...
python src/data_cleaning.py

echo.
echo [2/5] Generating JSON Knowledge Base...
python src/json_kb_generator.py

echo.
echo [3/5] Running Enhanced EDA...
python src/eda_enhanced.py

echo.
echo [4/5] Starting Backend API (Refactored)...
start "Saylani API" python -m src.app

timeout /t 3 /nobreak > nul

echo.
echo [5/5] Starting Dashboard...
start "Saylani Dashboard" streamlit run src/dashboard.py

echo.
echo ======================================================================
echo  SYSTEM READY!
echo ======================================================================
echo API: http://localhost:8000
echo Dashboard: http://localhost:8501
echo ======================================================================
echo.
echo Press any key to stop all services.....
pause > nul
