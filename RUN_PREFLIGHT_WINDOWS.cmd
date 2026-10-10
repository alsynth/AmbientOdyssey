@echo off
setlocal
cd /d "%~dp0"
echo Ambient Odyssey v0.4h -- READ-ONLY diagnostics
echo Enter the path of a separate, imported CurseForge instance.
echo No game files will be edited.
set /p "AO_INSTANCE=Installed profile folder: "
if "%AO_INSTANCE%"=="" (
  echo No folder entered.
  exit /b 2
)
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set "AO_PY=py -3"
) else (
  set "AO_PY=python"
)
%AO_PY% "tools\diagnose_v04_instance.py" --profile "%AO_INSTANCE%"
%AO_PY% "tools\audit_installed_jars_v04.py" --profile "%AO_INSTANCE%"
echo.
echo PRE-FLIGHT ONLY. Review any issues or warnings before testing Minecraft.
pause
endlocal
