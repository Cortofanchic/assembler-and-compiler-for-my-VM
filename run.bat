@echo off
setlocal
cd /d "%~dp0"

set "PY_CMD="
if exist ".venv\Scripts\python.exe" set "PY_CMD=.venv\Scripts\python.exe"
if not defined PY_CMD if exist "..\.venv\Scripts\python.exe" set "PY_CMD=..\.venv\Scripts\python.exe"
if not defined PY_CMD if exist "C:\Users\maria\AppData\Local\Programs\Python\Python314\python.exe" set "PY_CMD=C:\Users\maria\AppData\Local\Programs\Python\Python314\python.exe"
if not defined PY_CMD (
    where py >nul 2>nul && set "PY_CMD=py"
)

if not defined PY_CMD (
    echo ERROR: Python not found!
    pause
    exit /b 1
)

echo Using Python: %PY_CMD%
echo.

if not "%~1"=="" (
    if not exist build mkdir build
    echo ^<%~n1^>
    "%PY_CMD%" src/asm.py "%~1" "build\%~n1.bin" --test
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

for %%f in (*.asm tests\*.asm) do (
    if exist "%%f" (
        echo ^<%%~nf^>
        "%PY_CMD%" src/asm.py "%%f" "build\%%~nf.bin" --test
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