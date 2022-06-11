@echo off
cd %~dp0
copy "dist\Games SysTray\games.json"
pyinstaller --clean --noconfirm --uac-admin -i app.ico --add-data "style.qss;." -n "Games SysTray" app.pyw
del "dist\Games SysTray\opengl32sw.dll"