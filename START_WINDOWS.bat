@echo off
chcp 65001 >nul
cd /d "%~dp0"
title KOTA BERSIH 3D - Local Game
where powershell.exe >nul 2>nul
if errorlevel 1 (
  echo PowerShell tidak ditemukan pada Windows ini.
  echo Coba buka index.html dengan Chrome sebagai alternatif.
  pause
  exit /b 1
)
echo Menjalankan KOTA BERSIH 3D di browser lokal...
echo Biarkan jendela ini tetap terbuka selama bermain.
echo Tekan Ctrl+C di jendela ini untuk menghentikan server.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-local.ps1"
pause
