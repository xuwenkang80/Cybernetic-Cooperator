@echo off
SET RECEIVER_PATH=.\remoteReceiverPlayer

:: 启动 simpleServer.py 在一个新的窗口
start "" python simpleServer.py

:: 等待 simpleServer.py 启动 
timeout /t 2 /nobreak

:: 启动 remoteReceiverPlayer 在另一个新的窗口
start "" cmd /k "cd /d %RECEIVER_PATH% && npm run dev"