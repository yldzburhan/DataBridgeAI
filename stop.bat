@echo off
REM Stop DataBridge AI containers

echo Stopping DataBridge AI containers...
docker-compose down

echo.
echo To remove all data (including database):
echo   docker-compose down -v
echo.
pause
