@echo off
cd /d "%~dp0"
echo Unregistering context menu...

powershell -NoProfile -Command "$exts = @('.mp4','.avi','.mkv','.mov','.wmv'); foreach($e in $exts) { $path = \"HKCU:\Software\Classes\SystemFileAssociations\$e\shell\DiscordVideoCompress\"; if (Test-Path $path) { Remove-Item -Path $path -Recurse -Force } }"

echo.
echo Unregistration complete!
echo Context menu option has been removed.
echo.
pause
