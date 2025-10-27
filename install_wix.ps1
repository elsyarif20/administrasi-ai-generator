# install_wix.ps1
Write-Host "Menginstal WiX Toolset 3.11.2..."
Invoke-WebRequest -Uri "https://github.com/wixtoolset/wix3/releases/download/wix3112rtm/wix311.exe" -OutFile "wix311.exe"
Start-Process "wix311.exe" -ArgumentList "/install", "/quiet", "/norestart" -Wait
Write-Host "WiX Toolset selesai diinstal."
