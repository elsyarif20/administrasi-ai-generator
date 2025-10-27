Write-Host "🚀 BUILDING AHIM STUDIO..." -ForegroundColor Green
cd $PSScriptRoot

# CREATE VENV
if (-not (Test-Path "venv")) { python -m venv venv }
.\venv\Scripts\Activate.ps1

# INSTALL
pip install --upgrade pip
pip install -r requirements.txt

# BUILD
pyinstaller --onefile --windowed --icon=icon.ico --noconsole --clean --name=AhimStudio super_editor.py

Write-Host "✅ EXE: dist\AhimStudio.exe" -ForegroundColor Green
explorer dist
pause