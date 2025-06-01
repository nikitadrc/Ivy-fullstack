@echo off
echo Starting build process...

echo Cleaning up...
rmdir /s /q node_modules 2>nul
del /f /q package-lock.json 2>nul
del /f /q build 2>nul

echo Installing dependencies...
call npm install --legacy-peer-deps --no-audit

if %errorlevel% neq 0 (
    echo Error installing dependencies
    pause
    exit /b %errorlevel%
)

echo Running type check...
call npm run type-check

if %errorlevel% neq 0 (
    echo Type check failed
    pause
    exit /b %errorlevel%
)

echo Building project...
call npm run build

if %errorlevel% neq 0 (
    echo Build failed
    pause
    exit /b %errorlevel%
)

echo Build completed successfully!
echo The build output is in the 'build' directory
pause 