# OpenClaw + Ollama 自动启动方案

## 方案概览

1. **方案 A（推荐）**: 使用系统服务/启动项自动启动 Ollama
2. **方案 B**: 修改 memory-lancedb-pro 插件，在初始化时启动 Ollama
3. **方案 C**: 使用包装脚本同时启动两者

---

## 方案 A: 系统服务自动启动（推荐）

### Windows - 使用任务计划程序

创建启动任务，在登录时自动启动 Ollama：

```powershell
# 创建 Ollama 启动任务（用户登录时）
$action = New-ScheduledTaskAction -Execute "ollama" -Argument "serve"
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
Register-ScheduledTask -TaskName "Ollama-AutoStart" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

# 立即运行
Start-ScheduledTask -TaskName "Ollama-AutoStart"
```

查看任务：
```powershell
Get-ScheduledTask -TaskName "Ollama-AutoStart"
```

删除任务：
```powershell
Unregister-ScheduledTask -TaskName "Ollama-AutoStart" -Confirm:$false
```

### Windows - 使用启动文件夹

创建快捷方式到启动文件夹：

```powershell
# 创建启动脚本
$startupScript = @'
@echo off
echo Starting Ollama...
start /min "" ollama serve
timeout /t 3 /nobreak >nul
'@

$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\start-ollama.bat"
$startupScript | Out-File -FilePath $startupPath -Encoding ASCII

Write-Host "Ollama 启动脚本已创建: $startupPath"
```

### macOS - 使用 launchd

创建 plist 文件：

```bash
# 创建启动代理
cat > ~/Library/LaunchAgents/com.ollama.ollama.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.ollama</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ollama.out</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ollama.err</string>
</dict>
</plist>
EOF

# 加载并启动
launchctl load ~/Library/LaunchAgents/com.ollama.ollama.plist
launchctl start com.ollama.ollama

# 查看状态
launchctl list | grep ollama
```

### Linux - 使用 systemd

创建 systemd 服务：

```bash
# 创建服务文件
sudo tee /etc/systemd/system/ollama.service > /dev/null << 'EOF'
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=%u
Group=%g
Restart=always
RestartSec=3
Environment="HOME=%h"

[Install]
WantedBy=default.target
EOF

# 启用并启动
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

# 查看状态
sudo systemctl status ollama
```

---

## 方案 B: 插件级自动启动

修改 memory-lancedb-pro 插件，在插件初始化时检查并启动 Ollama。

### 配置扩展示例

```json
{
  "plugins": {
    "entries": {
      "memory-lancedb-pro": {
        "config": {
          "embedding": {
            "apiKey": "ollama",
            "model": "qwen3-embedding:4b",
            "baseURL": "http://localhost:11434/v1",
            "dimensions": 2560,
            "ollama": {
              "autoStart": true,
              "binaryPath": "ollama",
              "startTimeoutMs": 10000,
              "healthCheckRetries": 5
            }
          }
        }
      }
    }
  }
}
```

### 插件代码修改建议

在 `src/embedder.ts` 中添加 Ollama 启动逻辑：

```typescript
interface OllamaConfig {
  autoStart?: boolean;
  binaryPath?: string;
  startTimeoutMs?: number;
  healthCheckRetries?: number;
}

export class OllamaEmbedder {
  private ollamaConfig?: OllamaConfig;
  
  constructor(config: EmbeddingConfig) {
    this.ollamaConfig = config.ollama;
  }
  
  async ensureRunning(): Promise<void> {
    if (!this.ollamaConfig?.autoStart) return;
    
    // 检查 Ollama 是否已在运行
    const isRunning = await this.checkHealth();
    if (isRunning) return;
    
    // 启动 Ollama
    console.log('[OllamaEmbedder] Starting Ollama service...');
    await this.startOllama();
    
    // 等待服务就绪
    await this.waitForHealthy();
  }
  
  private async checkHealth(): Promise<boolean> {
    try {
      const response = await fetch('http://localhost:11434/api/tags', {
        signal: AbortSignal.timeout(2000)
      });
      return response.ok;
    } catch {
      return false;
    }
  }
  
  private async startOllama(): Promise<void> {
    const binary = this.ollamaConfig?.binaryPath || 'ollama';
    
    // 平台特定的启动命令
    const command = process.platform === 'win32'
      ? `start /min "" ${binary} serve`
      : `${binary} serve &`;
    
    const { exec } = await import('child_process');
    exec(command, (error) => {
      if (error) {
        console.error('[OllamaEmbedder] Failed to start Ollama:', error);
      }
    });
  }
  
  private async waitForHealthy(): Promise<void> {
    const maxRetries = this.ollamaConfig?.healthCheckRetries || 10;
    const timeout = this.ollamaConfig?.startTimeoutMs || 30000;
    const interval = timeout / maxRetries;
    
    for (let i = 0; i < maxRetries; i++) {
      await new Promise(r => setTimeout(r, interval));
      
      if (await this.checkHealth()) {
        console.log('[OllamaEmbedder] Ollama is ready');
        return;
      }
    }
    
    throw new Error('Ollama failed to start within timeout');
  }
}
```

---

## 方案 C: 包装启动脚本

创建一个脚本同时启动 Ollama 和 OpenClaw Gateway。

### Windows 批处理脚本

```batch
@echo off
chcp 65001 >nul
title OpenClaw + Ollama Launcher

echo ==========================================
echo   OpenClaw + Ollama Launcher
echo ==========================================
echo.

:: 检查 Ollama 是否运行
echo [1/3] 检查 Ollama 状态...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo      ✓ Ollama 已在运行
) else (
    echo      → 启动 Ollama...
    start /min "" ollama serve
    timeout /t 3 /nobreak >nul
    
    :: 验证启动
    curl -s http://localhost:11434/api/tags >nul 2>&1
    if "%ERRORLEVEL%"=="0" (
        echo      ✓ Ollama 启动成功
    ) else (
        echo      ✗ Ollama 启动失败，继续 anyway...
    )
)

echo.
echo [2/3] 清理 jiti 缓存...
if exist "%TEMP%\jiti" rmdir /s /q "%TEMP%\jiti" 2>nul
if exist "C:\tmp\jiti" rmdir /s /q "C:\tmp\jiti" 2>nul
echo      ✓ 缓存已清理

echo.
echo [3/3] 启动 OpenClaw Gateway...
echo.
openclaw gateway --port 18789 --verbose

echo.
echo 按任意键退出...
pause >nul
```

保存为 `start-openclaw-with-ollama.bat`，双击运行。

### PowerShell 脚本（更健壮）

```powershell
#Requires -Version 5.1

function Test-OllamaHealth {
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:11434/api/tags" -TimeoutSec 2
        return $true
    } catch {
        return $false
    }
}

function Start-OllamaService {
    param([int]$MaxWaitSeconds = 30)
    
    Write-Host "→ 启动 Ollama 服务..." -ForegroundColor Yellow
    
    # 启动 Ollama（后台）
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    
    # 等待服务就绪
    $elapsed = 0
    while ($elapsed -lt $MaxWaitSeconds) {
        if (Test-OllamaHealth) {
            Write-Host "  ✓ Ollama 已就绪" -ForegroundColor Green
            return $true
        }
        Start-Sleep -Seconds 1
        $elapsed++
        Write-Host "  等待 Ollama 就绪... ($elapsed/$MaxWaitSeconds)" -ForegroundColor Gray
    }
    
    Write-Host "  ✗ Ollama 启动超时" -ForegroundColor Red
    return $false
}

function Clear-JitiCache {
    Write-Host "→ 清理 jiti 缓存..." -ForegroundColor Yellow
    
    $cachePaths = @(
        "$env:TEMP\jiti",
        "$env:TEMP\jiti-*",
        "C:\tmp\jiti"
    )
    
    foreach ($path in $cachePaths) {
        if (Test-Path $path) {
            Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
    
    Write-Host "  ✓ 缓存已清理" -ForegroundColor Green
}

# ========== 主程序 ==========

Write-Host @"
╔══════════════════════════════════════════╗
║     OpenClaw + Ollama Launcher           ║
╚══════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# 1. 检查 Ollama
Write-Host "[1/3] 检查 Ollama 状态..." -ForegroundColor Cyan
if (Test-OllamaHealth) {
    Write-Host "  ✓ Ollama 已在运行" -ForegroundColor Green
} else {
    $started = Start-OllamaService -MaxWaitSeconds 30
    if (-not $started) {
        Write-Host "  警告: Ollama 可能未正常启动，继续 anyway..." -ForegroundColor Yellow
    }
}

# 2. 清理缓存
Write-Host "`n[2/3] 清理环境..." -ForegroundColor Cyan
Clear-JitiCache

# 3. 启动 Gateway
Write-Host "`n[3/3] 启动 OpenClaw Gateway..." -ForegroundColor Cyan
Write-Host "  按 Ctrl+C 停止服务`n" -ForegroundColor Gray

openclaw gateway --port 18789 --verbose

Write-Host "`nGateway 已停止" -ForegroundColor Yellow
```

保存为 `start-openclaw.ps1`，运行：
```powershell
.\start-openclaw.ps1
```

### Linux/macOS 脚本

```bash
#!/bin/bash

set -e

echo "=========================================="
echo "   OpenClaw + Ollama Launcher"
echo "=========================================="
echo

# 检查 Ollama
echo "[1/3] 检查 Ollama 状态..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  ✓ Ollama 已在运行"
else
    echo "  → 启动 Ollama..."
    ollama serve &
    OLLAMA_PID=$!
    
    # 等待就绪
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo "  ✓ Ollama 已就绪"
            break
        fi
        sleep 1
    done
fi

# 清理缓存
echo
echo "[2/3] 清理 jiti 缓存..."
rm -rf /tmp/jiti/* 2>/dev/null || true
echo "  ✓ 缓存已清理"

# 启动 Gateway
echo
echo "[3/3] 启动 OpenClaw Gateway..."
echo "  按 Ctrl+C 停止服务"
echo
openclaw gateway --port 18789 --verbose
```

保存为 `start-openclaw.sh`：
```bash
chmod +x start-openclaw.sh
./start-openclaw.sh
```

---

## 推荐配置

对于 Windows 用户，推荐使用 **方案 A（任务计划程序）+ 方案 C（启动脚本）** 组合：

1. 任务计划程序确保登录时 Ollama 自动启动
2. 启动脚本在手动启动 OpenClaw 时确保 Ollama 已运行

### 快捷方式设置

创建桌面快捷方式：

```powershell
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\OpenClaw+Ollama.lnk")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$env:USERPROFILE\.openclaw\start-openclaw.ps1`""
$Shortcut.WorkingDirectory = "$env:USERPROFILE\.openclaw"
$Shortcut.IconLocation = "%SystemRoot%\System32\shell32.dll,14"
$Shortcut.Save()

Write-Host "快捷方式已创建到桌面"
```

---

## 故障排除

### Ollama 端口被占用

```powershell
# 查找占用 11434 端口的进程
Get-NetTCPConnection -LocalPort 11434 | Select-Object LocalPort, OwningProcess, @{Name="ProcessName";Expression={(Get-Process -Id $_.OwningProcess).ProcessName}}

# 结束进程（如果必要）
Stop-Process -Id <PID> -Force
```

### Ollama 启动失败

检查日志：
- Windows: `%USERPROFILE%\.ollama\logs\`
- macOS/Linux: `~/.ollama/logs/`

### 验证配置

```powershell
# 测试 Ollama
ollama list
ollama run qwen3-embedding:4b "test"

# 测试 API
curl http://localhost:11434/v1/embeddings -d '{"model":"qwen3-embedding:4b","input":"test"}'

# 测试 OpenClaw
openclaw status
```
