@echo off
:: MAYA

:: --- PATH ---
set "PROJECT_ROOT=C:/Users/hsull/Documents/maya/projects/default"
set "PIPELINEPATH=%PROJECT_ROOT%/dev"

set "MAYA_VERSION=2020"

:: --- PYTHON ---
set "PYTHONPATH=%PROJECT_ROOT%/dev"

:: --- Arnold ---
set MAYA_MODULE_PATH=%MAYA_MODULE_PATH%
set MAYA_RENDER_DESC_PATH=%MAYA_RENDER_DESC_PATH%

:: --- CALL MAYA ---
set "MAYA_DIR=C:/Program Files/Autodesk/Maya%MAYA_VERSION%"
set "PATH=%MAYA_DIR%/bin;%PATH%"
start "" "%MAYA_DIR%/bin/maya.exe"