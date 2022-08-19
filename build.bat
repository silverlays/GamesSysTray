@echo off
cd %~dp0
copy "dist\Games SysTray\games.json"
pyinstaller --clean --noconfirm --uac-admin -i app.ico --add-data "style.qss;." -n "Games SysTray" app.pyw
copy games.json "dist\Games SysTray"
del "dist\Games SysTray\opengl32sw.dll"