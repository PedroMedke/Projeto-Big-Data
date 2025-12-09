Write-Host "=== Instalando Python 3.12 ===" -ForegroundColor Cyan
$PythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$InstallerPath = "$env:TEMP\python-installer.exe"

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -Uri $PythonUrl -OutFile $InstallerPath
& $InstallerPath /quiet InstallAllUsers=1 PrependPath=1 /norestart

Write-Host "Instalação iniciada! Aguarde..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

python --version
