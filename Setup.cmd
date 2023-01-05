@ECHO OFF

SETLOCAL EnableDelayedExpansion

SET VU_NAME=PyVutils

ECHO *** %VU_NAME% Setup ***
ECHO.

IF EXIST "%PyVutils%" (
	ECHO %VU_NAME% already installed
	GOTO L_EXIT
)

ECHO ---
ECHO.
FOR %%I IN ("%~dp0.") DO FOR %%J IN ("%%~dpI.") DO SET VU_DIR=%%~dpnxJ\
ECHO Add/Update Enviroment `PyVutils` -^> `%VU_DIR%`
rem SETX PyVutils %VU_DIR%
ECHO.

ECHO ---
ECHO.
ECHO Add/Update Enviroment `PYTHONPATH` -^> `%VU_DIR%`
SETX PYTHONPATH %VU_DIR%;%PYTHONPATH%
ECHO.

ECHO ---
ECHO.
pip3 install -r requirements.txt
ECHO.

ECHO ---
ECHO.
ECHO Completed

:L_EXIT

ECHO.
PAUSE