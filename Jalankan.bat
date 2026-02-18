@echo off
chcp 65001 >nul
title 🌿 GitHub Greener - Auto Contribute
color 0A
cd /d "%~dp0"
python auto_contribute.py
