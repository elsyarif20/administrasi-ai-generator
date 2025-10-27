# build_all.ps1
Write-Host "=== Building AhimStudio ==="

# Aktifkan virtual environment
.\venv\Scripts\activate

# Install dependensi
pip install -r requirements.txt
pip install pyinstaller

# Build EXE
pyinstaller --noconsole --onefile --icon=icon.ico super_editor.py --name AhimStudio

Write-Host "=== Membuat Installer MSI ==="

# Pastikan WiX sudah diinstall
if (-Not (Get-Command candle.exe -ErrorAction SilentlyContinue)) {
    Write-Host "WiX belum terinstall, jalankan install_wix.ps1 dulu."
    exit
}

# Compile WXS
candle.exe AhimStudio.wxs

# Link ke MSI
light.exe AhimStudio.wixobj -ext WixUIExtension -o AhimStudio.msi

Write-Host "=== Selesai! File MSI ada di folder ini ==="
