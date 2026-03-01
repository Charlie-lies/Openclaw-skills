---
name: lancedb-ollama-setup
description: Configure memory-lancedb-pro plugin with Ollama local embedding models for OpenClaw. Use when setting up local embeddings with LanceDB, configuring Ollama embedding models (nomic-embed-text, qwen3-embedding), troubleshooting LanceDB memory storage/retrieval issues, or migrating from cloud to local embedding providers.
---

# LanceDB + Ollama 本地嵌入配置指南

配置 memory-lancedb-pro 插件使用 Ollama 本地嵌入模型，实现完全离线的长期记忆功能。

## 前置要求

- OpenClaw 已安装并运行
- memory-lancedb-pro 插件已安装
- Windows/macOS/Linux 系统

## 1. 安装 Ollama

### Windows

```powershell
# 使用 winget 安装
winget install Ollama.Ollama

# 或从官网下载安装包
# https://ollama.com/download
```

### macOS

```bash
# 使用 Homebrew
brew install ollama

# 或从官网下载
# https://ollama.com/download
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 验证安装

```bash
ollama --version
# 应显示版本号，如: ollama version 0.3.0
```

## 2. 下载嵌入模型

### 推荐模型

| 模型 | 适用场景 | 维度 | 命令 |
|------|---------|------|------|
| `nomic-embed-text` | 英文为主 | 768 | `ollama pull nomic-embed-text` |
| `qwen3-embedding:4b` | 中英双语 | 2560 | `ollama pull qwen3-embedding:4b` |

### 常用 Ollama 命令

```bash
# 下载模型
ollama pull nomic-embed-text
ollama pull qwen3-embedding:4b

# 查看已安装模型
ollama list

# 删除模型
ollama rm nomic-embed-text

# 测试嵌入功能
ollama run nomic-embed-text "Hello world"
ollama run qwen3-embedding:4b "你好世界"

# 查看模型详情
ollama show nomic-embed-text

# 启动 Ollama 服务（后台）
ollama serve
```

### 测试连通性

```bash
# 测试 API 端点
curl http://localhost:11434/api/tags

# 测试嵌入生成
curl -X POST http://localhost:11434/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3-embedding:4b", "input": "test"}'
```

**官方文档**: https://docs.ollama.com/capabilities/embeddings

## 3. OpenClaw 配置

### 基础配置 (openclaw.json)

```json
{
  "plugins": {
    "load": {
      "paths": ["C:/Users/<username>/.openclaw/extensions/memory-lancedb-pro"]
    },
    "entries": {
      "memory-lancedb-pro": {
        "enabled": true,
        "config": {
          "embedding": {
            "apiKey": "ollama",
            "model": "qwen3-embedding:4b",
            "baseURL": "http://localhost:11434/v1",
            "dimensions": 2560
          },
          "dbPath": "~/.openclaw/memory/lancedb-pro",
          "autoCapture": true,
          "autoRecall": false,
          "retrieval": {
            "mode": "hybrid",
            "vectorWeight": 0.7,
            "bm25Weight": 0.3,
            "minScore": 0.3,
            "rerank": "none",
            "candidatePoolSize": 50,
            "recencyHalfLifeDays": 14,
            "recencyWeight": 0.1,
            "filterNoise": true,
            "lengthNormAnchor": 500,
            "hardMinScore": 0.35,
            "timeDecayHalfLifeDays": 60
          },
          "scopes": {
            "default": "global"
          }
        }
      }
    },
    "slots": {
      "memory": "memory-lancedb-pro"
    }
  }
}
```

### 模型特定配置

#### nomic-embed-text (英文)

```json
{
  "embedding": {
    "apiKey": "ollama",
    "model": "nomic-embed-text",
    "baseURL": "http://localhost:11434/v1",
    "dimensions": 768
  }
}
```

#### qwen3-embedding:4b (中英双语)

```json
{
  "embedding": {
    "apiKey": "ollama",
    "model": "qwen3-embedding:4b",
    "baseURL": "http://localhost:11434/v1",
    "dimensions": 2560
  }
}
```

### 关键配置项说明

| 配置项 | 说明 | 建议值 |
|--------|------|--------|
| `apiKey` | Ollama 不需要真实 key，填 "ollama" 即可 | `"ollama"` |
| `model` | 嵌入模型名称 | `qwen3-embedding:4b` |
| `baseURL` | Ollama API 地址 | `http://localhost:11434/v1` |
| `dimensions` | 向量维度，必须与模型一致 | 2560 (qwen3) / 768 (nomic) |
| `candidatePoolSize` | 候选池大小，影响 category 过滤 | 50 (默认 20 偏小) |
| `hardMinScore` | 硬截断分数，低于此值丢弃 | 0.35 |

## 4. 应用配置

### 步骤 1: 清理 jiti 缓存（重要！）

```powershell
# Windows
Remove-Item -Recurse -Force $env:TEMP\jiti*
Remove-Item -Recurse -Force C:\tmp\jiti

# Linux/macOS
rm -rf /tmp/jiti/
```

### 步骤 2: 重启网关

```bash
openclaw gateway restart
```

### 步骤 3: 验证配置

```bash
openclaw status
```

应看到插件注册成功：
```
[plugins] memory-lancedb-pro@1.0.15: plugin registered
```

## 5. LanceDB 功能测试

### 基础功能测试

```javascript
// 测试存储
memory_store({
  text: "LanceDB Ollama 集成测试",
  category: "fact",
  importance: 0.8
})

// 测试检索
memory_recall({
  query: "LanceDB 测试",
  limit: 5
})

// 按 category 检索
memory_recall({
  query: "测试",
  category: "fact",
  limit: 5
})
```

### Scope 权限测试

```javascript
// 1. 配置自定义 scope（见下方配置）
// 2. 存储到自定义 scope
memory_store({
  text: "自定义 scope 测试",
  category: "fact",
  scope: "custom:my-scope"
})

// 3. 从自定义 scope 检索
memory_recall({
  query: "测试",
  scope: "custom:my-scope"
})
```

### 全面测试清单

| 测试项 | 命令 | 预期结果 |
|--------|------|---------|
| 基础存储 | `memory_store` | 成功返回存储确认 |
| 基础检索 | `memory_recall` | 返回匹配的记忆 |
| Category 过滤 | `memory_recall` + `category` | 只返回指定 category |
| Scope 存储 | `memory_store` + `scope` | 存储到指定 scope |
| Scope 检索 | `memory_recall` + `scope` | 只返回指定 scope |
| 更新记忆 | `memory_update` | 内容/category/importance 更新 |
| 删除记忆 | `memory_forget` | 成功删除 |
| 长文本 | 存储 >500 字符 | 正常存储检索 |
| 特殊字符 | 包含标点/emoji | 正常存储检索 |
| 多语言 | 中英混合 | 正常存储检索 |

## 6. 故障排除

### 问题 1: Connection error

**症状**: `Failed to generate embedding: Connection error`

**解决**:
1. 确认 Ollama 服务运行: `ollama serve`
2. 测试连通性: `curl http://localhost:11434/api/tags`
3. 清理 jiti 缓存: `rm -rf /tmp/jiti`
4. 重启网关: `openclaw gateway restart`

### 问题 2: Access denied to scope

**症状**: 存储到自定义 scope 时返回 `Access denied`

**解决**: 自定义 scope 必须使用内置前缀：
- ✅ `custom:my-scope`
- ❌ `my-scope`

配置示例：
```json
{
  "scopes": {
    "definitions": {
      "custom:my-scope": { "description": "我的 scope" }
    },
    "agentAccess": {
      "main": ["global", "custom:my-scope"]
    }
  }
}
```

### 问题 3: Category 过滤返回空

**症状**: `category: "preference"` 过滤返回空

**根因**: `candidatePoolSize` 太小，过滤后无结果

**解决**: 增加配置值
```json
{
  "retrieval": {
    "candidatePoolSize": 50
  }
}
```

### 问题 4: 向量维度不匹配

**症状**: `Vector dimension mismatch`

**解决**: 
1. 删除旧数据库: `rm -rf ~/.openclaw/memory/lancedb-pro`
2. 确认 `dimensions` 与模型一致
3. 重启网关

## 7. 高级配置

### 启用管理工具

```json
{
  "enableManagementTools": true
}
```

启用后可使用：
- `memory_stats` - 查看统计
- `memory_list` - 列出记忆

### 多 Scope 配置示例

```json
{
  "scopes": {
    "default": "global",
    "definitions": {
      "global": { "description": "共享知识" },
      "custom:project-a": { "description": "项目A私有" },
      "custom:project-b": { "description": "项目B私有" }
    },
    "agentAccess": {
      "main": ["global", "custom:project-a", "custom:project-b"],
      "discord-bot": ["global"]
    }
  }
}
```

### 自动捕获/回忆配置

```json
{
  "autoCapture": true,    // 自动提取对话中的偏好/决策
  "autoRecall": false     // 自动注入相关记忆到上下文
}
```

## 8. 自动启动配置（可选）

让 Ollama 随 OpenClaw 一起启动的三种方案：

| 方案 | 适用场景 | 复杂度 |
|------|---------|--------|
| **A. 系统服务** | 长期稳定使用 | 低 |
| **B. 插件级启动** | 需要精细控制 | 中 |
| **C. 包装脚本** | 临时/开发使用 | 低 |

详见 [ollama-autostart.md](references/ollama-autostart.md)：
- Windows 任务计划程序 / 启动文件夹配置
- macOS launchd 配置
- Linux systemd 服务配置
- PowerShell/Bash 启动脚本
- 完整故障排除指南

## 参考资源

- [Ollama 官方文档](https://docs.ollama.com/capabilities/embeddings)
- [memory-lancedb-pro 插件 README](references/lancedb-pro-readme.md)
- [Ollama 自动启动配置](references/ollama-autostart.md)
