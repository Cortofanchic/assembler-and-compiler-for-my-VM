@echo off
setlocal
cd /d "%~dp0"

set "PY_CMD="
if exist ".venv\Scripts\python.exe" set "PY_CMD=.venv\Scripts\python.exe"
if not defined PY_CMD if exist "..\.venv\Scripts\python.exe" set "PY_CMD=..\.venv\Scripts\python.exe"
if not defined PY_CMD if exist "C:\Users\maria\AppData\Local\Programs\Python\Python314\python.exe" set "PY_CMD=C:\Users\maria\AppData\Local\Programs\Python\Python314\python.exe"
if not defined PY_CMD (
    where py > nul 2 > nul && set "PY_CMD=py"
)

if not defined PY_CMD (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo Using Python: %PY_CMD%
echo.

if not "%~1"=="" (
    if not exist damp mkdir damp
    echo ^<%~n1^>
    "%PY_CMD%" src/intepr.py "%~1" "damp\%~n1.xml" --test
    if errorlevel 1 (
        echo FAIL on %~1
        pause
        exit /b 1
    )
    echo.
    echo Done
    pause
    exit /b 0
)

for %%f in (*.bin tests\tests_results\*.bin) do (
    if exist "%%f" (
        echo ^<%%~nf^>
        "%PY_CMD%" src/intepr.py "%%f" "tests\tests_of_intepr\%%~nf.xml" 1:1000
        if errorlevel 1 (
            echo FAIL on %%f
            pause
            exit /b 1
        )
        echo.
    )
)

echo Done
pause