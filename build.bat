@echo off
cd %~dp0
copy "dist\games.json"
pyinstaller -F --noconfirm -i app.ico -n "Games SysTray" app.pyw
copy games.json dist
