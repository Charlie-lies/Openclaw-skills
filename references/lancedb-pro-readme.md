# memory-lancedb-pro 插件参考

## 功能特性

- **混合检索**: Vector + BM25 融合
- **跨编码器 Rerank**: Jina Reranker API 支持
- **多 Scope 隔离**: 支持 `global`、`agent:<id>`、`custom:<name>` 等
- **时效性加成**: 新记忆分数更高
- **时间衰减**: 旧条目逐渐降权
- **长度归一化**: 防止长条目霸占结果
- **MMR 多样性**: 避免近似重复结果
- **噪声过滤**: 过滤低质量记忆

## 数据库 Schema

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | UUID 主键 |
| `text` | string | 记忆文本（FTS 索引）|
| `vector` | float[] | Embedding 向量 |
| `category` | string | preference/fact/decision/entity/other |
| `scope` | string | Scope 标识 |
| `importance` | float | 0-1 重要性分数 |
| `timestamp` | int64 | 创建时间戳 |
| `metadata` | string | JSON 扩展元数据 |

## 核心工具

- `memory_store` - 存储记忆
- `memory_recall` - 检索记忆
- `memory_forget` - 删除记忆
- `memory_update` - 更新记忆
- `memory_stats` - 统计信息（需启用 management tools）
- `memory_list` - 列出记忆（需启用 management tools）

## CLI 命令

```bash
openclaw memory-pro list [--scope global] [--category fact]
openclaw memory-pro search "query" [--scope global]
openclaw memory-pro stats [--scope global]
openclaw memory-pro delete <id>
openclaw memory-pro export [--output memories.json]
openclaw memory-pro import memories.json
```

## 支持的 Embedding 提供商

| 提供商 | 模型示例 | Base URL |
|--------|---------|----------|
| Ollama | nomic-embed-text, qwen3-embedding:4b | http://localhost:11434/v1 |
| Jina | jina-embeddings-v5-text-small | https://api.jina.ai/v1 |
| OpenAI | text-embedding-3-small | https://api.openai.com/v1 |
| Gemini | gemini-embedding-001 | https://generativelanguage.googleapis.com/v1beta/openai/ |

## 常见错误

### "Cannot mix BigInt and other types"

升级到 memory-lancedb-pro >= 1.0.14，已修复数值类型转换问题。

### "Vector dimension mismatch"

确保 `embedding.dimensions` 与实际模型输出维度一致，或删除旧数据库重建。
