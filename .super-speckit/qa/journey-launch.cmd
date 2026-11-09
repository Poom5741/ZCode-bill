@echo off
rem RDUX15 journey launcher v3: env mirrors wdio.conf.ts E2E launch exactly
rem (HOME/USERPROFILE/ZCODE_* isolation, default-user-data mode, fixed 9229
rem disabled so the argv debug port survives), bound to the running vite dev
rem server. Isolated home = never touches the user's real app data.
set "JHOME=%~dp0journey-home"
set "HOME=%JHOME%"
set "USERPROFILE=%JHOME%"
set "ZCODE_E2E_HOME_DIR=%JHOME%"
set "ZCODE_DATA_BASE_DIR=%JHOME%"
set "ZCODE_DESKTOP_APPLICATION_NAME=ZCode E2E"
set "ZCODE_DESKTOP_HOME_DIR=%JHOME%"
set "ZCODE_DESKTOP_USE_ELECTRON_DEFAULT_USER_DATA=1"
set "ZCODE_DISABLE_FIXED_REMOTE_DEBUGGING_PORT=1"
set "ZCODE_ENV=test"
cd /d "%~dp0..\..\packages\desktop"
start "journey-vite" /min cmd /c "pnpm exec vite dev --port 5174 --strictPort"
:waitvite
timeout /t 2 /nobreak >nul
node -e "fetch('http://localhost:5174/').then(()=>process.exit(0)).catch(()=>process.exit(1))" && goto viteup
goto waitvite
:viteup
set "ELECTRON_RENDERER_URL=http://localhost:5174"
"..\..\node_modules\electron\dist\electron.exe" . --remote-debugging-port=9223
