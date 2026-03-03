#!/bin/bash
# Linux/macOS 启动脚本

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查并安装依赖
echo "检查依赖..."
pip3 install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt 2>/dev/null

# 启动程序
python3 rest_timer.py &
