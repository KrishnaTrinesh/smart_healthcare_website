@echo off
echo Starting MongoDB with local configuration...
cd /d "%~dp0"
echo Current directory: %CD%
echo Starting MongoDB on port 27017...
echo.
mongod --config db\mongod.conf
pause

