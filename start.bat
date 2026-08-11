@echo off
chcp 65001 >nul
title 可予礼品竞品监控平台

echo ============================================
echo   可予礼品有限公司 · 竞品监控平台
echo   正在启动...
echo ============================================

set PYTHON=C:\Users\51752\.workbuddy\binaries\python\envs\candy_monitor\Scripts\python.exe
set NODE=C:\Users\51752\.workbuddy\binaries\node\versions\22.22.2\node.exe
set APP_DIR=C:\Users\51752\WorkBuddy\Claw\candy_monitor
set LT_DIR=C:\Users\51752\.workbuddy\binaries\node\workspace

echo.
echo [1/2] 启动 Python 服务器...
start "CandyMonitor-Server" /MIN cmd /c "cd /d %APP_DIR% && %PYTHON% run.py"

echo [2/2] 启动公网隧道...
timeout /t 3 /nobreak >nul

start "CandyMonitor-Tunnel" /MIN cmd /c "cd /d %LT_DIR% && %NODE% -e \"const lt=require('localtunnel');lt(5000,{subdomain:'candy-monitor'},function(e,t){if(e){console.log('Fallback tunnel...');lt(5000,function(e2,t2){if(e2){console.error(e2);process.exit(1)}console.log('URL: '+t2.url);setInterval(function(){},99999)})}else{console.log('URL: '+t.url);setInterval(function(){},99999)}});\""

timeout /t 5 /nobreak >nul
echo.
echo ============================================
echo   ✅ 启动完成！
echo   公网地址: https://candy-monitor.loca.lt
echo   本地地址: http://127.0.0.1:5000
echo   新手引导: https://candy-monitor.loca.lt/guide
echo ============================================
echo.
echo   按任意键关闭此窗口（服务继续在后台运行）
pause >nul
