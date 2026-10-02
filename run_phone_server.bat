@echo off
chcp 65001 > nul
echo ====================================================
echo   Daily English 99 - スマホ復習サーバー起動
echo ====================================================
echo.
echo スマホと同じWi-Fiに接続されていることを確認してください。
echo.
echo スマホのブラウザ（Safari または Chrome）のアドレスバーに
echo 以下のURLを入力して開いてください:
echo.
echo   👉 http://192.168.100.161:8000
echo.
echo ====================================================
echo 終了するときは、このウィンドウを閉じるか Ctrl+C を押してください。
echo.
python -m http.server 8000
pause
