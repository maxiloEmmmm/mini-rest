@echo off
chcp 65001 >nul
REM Windows 启动脚本

REM 切换到脚本所在目录
cd /d "%~dp0"

echo 检查依赖...
pip install -q -r requirements.txt 2>nul

echo 启动休息提醒器...
pythonw rest_timer.py
