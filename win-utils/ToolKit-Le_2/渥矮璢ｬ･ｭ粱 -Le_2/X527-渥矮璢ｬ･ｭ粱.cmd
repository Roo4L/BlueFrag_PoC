@echo off
TITLE LeEco Le 2 x520, x526, x527 - Utility
color 17
mode con cols=90 lines=30
:STARTS
CLS
ECHO.
ECHO. ======================================================================================
ECHO. 
ECHO.

ECHO. ======================================================================================
ECHO.                    1.Reboot Bootloader
ECHO.
ECHO.                    2.FastBoot - Unlock Bootloader
ECHO.
ECHO.                    3.FastBoot - Install Splash
ECHO.                    
ECHO.                    4.FastBoot - Install TWRP Recovery
ECHO.                    
ECHO.                    5.FastBoot - Install Stock Recovery
ECHO.                    
ECHO.                    6.4PDA
ECHO.
ECHO.                    0.Exit
ECHO. ======================================================================================
:CHO
set choice=
set /p choice= Select the action and then press Enter:
if /i "%choice%"=="1" goto Reboot
if /i "%choice%"=="2" goto Unlock
if /i "%choice%"=="3" goto InstallSplash
if /i "%choice%"=="4" goto InstallTWRP
if /i "%choice%"=="5" goto InstallStock
if /i "%choice%"=="6" goto Blog
if /i "%choice%"=="0" goto SECEDE
echo Error!
echo.
GOTO STARTS

:Reboot
CLS
ECHO ***************************************************************************************
ECHO *      ------------------------^< waiting for device ^>-------------------------      *
ECHO *                                                                                     *
ECHO *            If you get stuck at this point - the need to install drivers.            *
ECHO ***************************************************************************************
ECHO.
ECHO. ...
ECHO.
files\adb reboot bootloader

ECHO.
ECHO.
ECHO. Reboot Bootloader... Complete
ECHO.  
ECHO. 
ECHO.
pause
GOTO STARTS 

:Unlock
CLS
ECHO ***************************************************************************************
ECHO *      ------------------------^< waiting for device ^>-------------------------      *
ECHO *                                                                                     *
ECHO *            If you get stuck at this point - the need to install drivers.            *
ECHO ***************************************************************************************
ECHO.
ECHO. ...
ECHO.
files\fastboot oem unlock-go

ECHO.
ECHO.
ECHO. Smartphone successfully unlocked
ECHO.  
ECHO. 
ECHO.
pause
GOTO STARTS 

:InstallSplash 
CLS
ECHO ***************************************************************************
ECHO *------------------------^< waiting for device ^>-------------------------*
ECHO *                                                                         *
ECHO *      If you get stuck at this point - the need to install drivers.      *
ECHO ***************************************************************************
ECHO.
ECHO. Make sure that the bootloader is unlocked successfully!!!
ECHO.
files\fastboot flash splash files\splash.img
ECHO.
ECHO.
ECHO. Successfully installed Splash...
ECHO.
ECHO.
ECHO.
ECHO.
pause
GOTO STARTS

:InstallTWRP
CLS
ECHO ***************************************************************************
ECHO *------------------------^< waiting for device ^>-------------------------*
ECHO *                                                                         *
ECHO *      If you get stuck at this point - the need to install drivers.      *
ECHO ***************************************************************************
ECHO.
ECHO. Make sure that the bootloader is unlocked successfully!!!
ECHO.
files\fastboot flash recovery files\TWRP_Recovery.img
files\fastboot boot files\TWRP_Recovery.img >NUL 2>NUL
ECHO.
ECHO.
ECHO. Successfully installed TWRP Recovery...
ECHO.
ECHO.
ECHO.
ECHO.
pause
GOTO STARTS

:InstallStock
CLS
ECHO ***************************************************************************
ECHO *------------------------^< waiting for device ^>-------------------------*
ECHO *                                                                         *
ECHO *      If you get stuck at this point - the need to install drivers.      *
ECHO ***************************************************************************
ECHO.
ECHO. Make sure that the bootloader is unlocked successfully!!!
ECHO.
files\fastboot flash recovery files\STOCK_Recovery.img
files\fastboot boot files\STOCK_Recovery.img >NUL 2>NUL
ECHO.
ECHO.
ECHO. Successfully installed Stock Recovery...
ECHO.
ECHO.
ECHO.
ECHO.
ECHO.
pause
GOTO STARTS 

:Blog
START http://4pda.ru/forum/index.php?showtopic=773468

:SECEDE
exit