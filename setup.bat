@echo off
cls
echo Downloading Python...

winget install Python

cls
echo Downloading libaries

pip3 install tk
pip3 install customtkinter
cls
color 3

echo Everything should be ready!

pause