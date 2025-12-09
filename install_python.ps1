# Script para instalar Python 3.12 em Windows
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Instalador de Python 3.12 para Windows         ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# URL do instalador Python
$PythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$InstallerPath = "$env:TEMP\python-3.12.0-amd64.exe"

Write-Host "[1/3] Baixando Python 3.12..." -ForegroundColor Yellow
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $PythonUrl -OutFile $InstallerPath -ErrorAction Stop
    Write-Host "[✓] Download concluído!" -ForegroundColor Green
} catch {
    Write-Host "[✗] Erro ao baixar Python: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/3] Instalando Python (isso pode levar alguns minutos)..." -ForegroundColor Yellow
try {
    & $InstallerPath /quiet InstallAllUsers=1 PrependPath=1 /norestart | Out-Null
    Write-Host "[✓] Instalação concluída!" -ForegroundColor Green
} catch {
    Write-Host "[✗] Erro durante instalação: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/3] Verificando instalação..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Tentar encontrar Python
$PythonPaths = @(
    "C:\Python312\python.exe",
    "$env:ProgramFiles\Python312\python.exe",
    "$env:ProgramFiles(x86)\Python312\python.exe",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe"
)

$PythonFound = $false
foreach ($path in $PythonPaths) {
    if (Test-Path $path) {
        $PythonFound = $true
        $PythonVersion = & $path --version 2>&1
        Write-Host "[✓] Python encontrado: $PythonVersion" -ForegroundColor Green
        Write-Host "    Caminho: $path" -ForegroundColor Gray
        break
    }
}

if (-not $PythonFound) {
    Write-Host "[!] Python não encontrado nos caminhos esperados" -ForegroundColor Yellow
    Write-Host "    Atualize seu PATH ou reinicie o terminal" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    Tente também:" -ForegroundColor Yellow
    Write-Host "    1. Fechar e reabrir PowerShell" -ForegroundColor Gray
    Write-Host "    2. Executar: python --version" -ForegroundColor Gray
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Instalação finalizada! Execute 'python --version' para confirmar." -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
