@echo off
echo "0: Get data as CSV"
echo "1: Get data as Excel"
echo "2: Get data as both"
set /p userInput="Enter number: "
python "%cd%\src\main.py" %userInput%
pause