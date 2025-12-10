@echo off
chcp 65001 >nul
echo ========================================
echo  🔬 LingNexus 三模型对比工具
echo ========================================
echo.
echo 🇨🇳 Qwen-Max vs 🧠 DeepSeek 3.2 vs 🔥 Gemini 3 Pro
echo.
echo 功能：同时测试三大模型的分子生成能力
echo 启动后请访问: http://127.0.0.1:7861
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python app_compare.py

pause
