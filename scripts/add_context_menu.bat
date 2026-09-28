@echo off
cd /d "%~dp0"
echo Registering context menu...

set "TARGET_BAT=%~dp0run_context_menu.bat"

powershell -NoProfile -Command "$exts = @('.mp4','.avi','.mkv','.mov','.wmv'); $bat = $env:TARGET_BAT; foreach($e in $exts) { $path = \"HKCU:\Software\Classes\SystemFileAssociations\$e\shell\DiscordVideoCompress\"; New-Item -Path $path -Force | Out-Null; Set-ItemProperty -Path $path -Name '(default)' -Value 'Compress for Discord' -Force; New-Item -Path \"$path\command\" -Force | Out-Null; Set-ItemProperty -Path \"$path\command\" -Name '(default)' -Value \"`\"$bat`\" `\"%%1`\"\" -Force }"

echo.
echo Registration complete!
echo Right-click a video file to see the "Compress for Discord" option.
echo (On Windows 11, you may need to click "Show more options")
echo.
pause
