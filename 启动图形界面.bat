@echo off
chcp 65001 >nul
echo ========================================
echo  🧬 LingNexus 单模型生成
 echo ========================================
echo.
echo 支持模型：
echo  🇨🇳 Qwen-Max
echo  🧠 DeepSeek 3.2
echo  🔥 Gemini 3 Pro
echo.
echo 正在启动 Web 界面...
echo 启动后请访问: http://127.0.0.1:7860
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python app.py

pause
