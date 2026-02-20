# AdsPower RPA Flow Generator

Generate JSON automation flows for AdsPower browser RPA.

## Overview

This skill generates JSON flow definitions that can be imported directly into AdsPower's RPA Plus system. It provides a simplified, human-readable format for defining browser automation workflows.

## Installation

Place this skill folder in your OpenClaw skills directory:
```
skills/
  adspower-rpa/
    SKILL.md
    README.md
    generate.py
    adspower-rpa.py
    examples/
```

## Usage

### Generate from Definition File

```bash
openclaw skill adspower-rpa generate --file examples/amazon-search.json --output flow.json
```

### Generate from Inline JSON

```bash
openclaw skill adspower-rpa generate '{"steps":[{"action":"visit","url":"https://example.com"}]}' --output flow.json
```

### Validate Flow

```bash
openclaw skill adspower-rpa validate --file my-flow.json
```

### Generate Template

```bash
openclaw skill adspower-rpa template --output template.json
```

## Definition Format

### Basic Structure

```json
{
  "name": "Flow Name",
  "description": "What this flow does",
  "steps": [
    {"action": "visit", "url": "https://example.com"},
    {"action": "wait", "timeout": 3000},
    {"action": "click", "selector": "#btn"}
  ]
}
```

### Supported Actions

#### Page Operations
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `visit` | Navigate to URL | `url` |
| `newTab` | Open new tab | - |
| `closeTab` | Close current tab | - |
| `refresh` | Refresh page | - |
| `goBack` | Go back | - |
| `screenshot` | Take screenshot | `name` |
| `click` | Click element | `selector` |
| `input` | Input text | `selector`, `content` |
| `scroll` | Scroll page | `position` or `distance` |
| `hover` | Hover element | `selector` |
| `select` | Select dropdown | `selector`, `value` |
| `upload` | Upload file | `selector`, `filePath` |
| `js` | Execute JavaScript | `code` |
| `javaScript` | Execute JavaScript (extended) | `content`, `variable` |

#### Keyboard
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `key` | Press key | `key` |
| `hotkey` | Key combination | `combination` |

#### Wait
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `wait` | Wait time | `timeout` |
| `waitFor` | Wait for element | `selector` |
| `waitRequest` | Wait for request | `url` |

#### Data Extraction
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `extract` | Extract element data | `selector`, `extractType` |
| `getUrl` | Get URL info | `extractType` |
| `saveExcel` | Save to Excel | `filename`, `columns` |
| `exportExcel` | Export data to Excel with fields | `name`, `fields` |
| `saveFile` | Save to file | `filename` |
| `download` | Download file | `url` |

#### Data Import
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `importExcel` | Import Excel | `path`, `variableList` |
| `importTxt` | Import text file | `path` |
| `useExcel` | Import Excel as material source | `path`, `variableList`, `variable` |

**useExcel (Excel素材导入) 详细说明：**

用于将Excel文件作为素材数据源导入，支持为每个浏览器环境分配不同行的数据。

- **表头命名规则**：表头只能是字母、数字、下划线，且不能以数字开头
- **自动生成变量**：根据表头名称自动生成对应列的变量名
- **serial_number特殊处理**：表头名为 `serial_number` 时，可指定对应行内容为该浏览器环境使用的素材内容
- **数据格式**：整个Excel的数据以数组形式存储到变量，格式为 `[{key1:value, key2:value...}, {key1:value, key2:value...}...]`

```json
{
  "action": "useExcel",
  "path": "产品信息.xlsx",
  "variableList": ["SKU", "URL"],
  "variable": "products"
}
```

#### Data Processing
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `regex` | Regex extract | `data`, `rule` |
| `getField` | Extract field from object | `data`, `key`, `saveTo` |
| `randomPick` | Random selection | `data` |
| `toJson` | Convert to JSON | `data` |
| `extractKey` | Extract key from object (alias for getField) | `content`, `key`, `variable` |

#### Flow Control
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `if` | Conditional | `variable`, `condition`, `value` |
| `forElements` | Loop elements | `selector`, `do` |
| `forCount` | Loop count | `count`, `do` |
| `forData` | Loop data | `data`, `do` |
| `forLists` | Loop through list data | `content`, `variable`, `do` |
| `while` | While loop | `variable`, `condition`, `value`, `do` |
| `break` | Exit loop | - |
| `group` | Group steps | `steps` |
| `combineProcess` | Group processes visually | `blocks`, `groupName` |

#### Browser
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `newBrowser` | Launch browser | `envId` |
| `closeBrowser` | Close browser | - |

#### Environment
| Action | Description | Required Params |
|--------|-------------|-----------------|
| `setRemark` | Update remark | `content` |
| `setTag` | Update tag | `tags` |

## Advanced Examples

### Data Scraping with Excel Export

```json
{
  "name": "Product Scraper",
  "steps": [
    {"action": "visit", "url": "https://example.com/products"},
    {
      "action": "forElements",
      "selector": ".product",
      "do": [
        {"action": "extract", "selector": ".name", "extractType": "text", "saveTo": "name"},
        {"action": "extract", "selector": ".price", "extractType": "text", "saveTo": "price"},
        {"action": "saveExcel", "filename": "products.xlsx", "columns": ["name", "price"]}
      ]
    }
  ]
}
```

### Conditional Logic

```json
{
  "name": "Smart Login",
  "steps": [
    {"action": "visit", "url": "https://example.com"},
    {"action": "extract", "selector": "#status", "extractType": "text", "saveTo": "status"},
    {
      "action": "if",
      "variable": "status",
      "condition": "eq",
      "value": "logged_out",
      "then": [
        {"action": "click", "selector": "#login-btn"},
        {"action": "input", "selector": "#email", "content": "user@example.com"},
        {"action": "click", "selector": "#submit"}
      ]
    }
  ]
}
```

### Using Excel Data (importExcel)

```json
{
  "name": "Bulk Registration",
  "steps": [
    {"action": "importExcel", "path": "C:/data/users.xlsx", "variableList": ["email", "password"], "variable": "users"},
    {
      "action": "forData",
      "data": "${users}",
      "do": [
        {"action": "getField", "data": "${account}", "key": "email", "saveTo": "email"},
        {"action": "visit", "url": "https://example.com/register"},
        {"action": "input", "selector": "#email", "content": "${email}"}
      ]
    }
  ]
}
```

### Using Excel Material Source (useExcel + forLists)

结合 `useExcel` 和 `forLists` 实现批量数据处理：

```json
{
  "name": "Product Scraper with Excel",
  "steps": [
    {
      "action": "useExcel",
      "path": "产品信息.xlsx",
      "variableList": ["SKU", "URL"],
      "variable": "products",
      "remark": "Import product data from Excel"
    },
    {
      "action": "forLists",
      "content": "products",
      "variable": "for_list_item",
      "variableIndex": "for_list_index",
      "remark": "Loop through each product",
      "do": [
        {"action": "getField", "data": "${for_list_item}", "key": "SKU", "saveTo": "sku"},
        {"action": "getField", "data": "${for_list_item}", "key": "URL", "saveTo": "url"},
        {"action": "visit", "url": "${url}"},
        {"action": "extract", "selector": ".price", "extractType": "text", "saveTo": "price"},
        {"action": "saveExcel", "filename": "results.xlsx", "columns": ["sku", "url", "price"]}
      ]
    }
  ]
}
```

### Process Grouping (combineProcess)

使用 `combineProcess` 将相关步骤视觉分组，提高可读性：

```json
{
  "action": "combineProcess",
  "groupName": "提取字段",
  "blocks": [
    {"action": "getField", "data": "${for_list_item}", "key": "SKU", "saveTo": "sku"},
    {"action": "getField", "data": "${for_list_item}", "key": "URL", "saveTo": "url"}
  ]
}
```

完整示例（含多个分组）：

```json
{
  "name": "Complete Product Scraper",
  "steps": [
    {
      "action": "useExcel",
      "path": "产品信息.xlsx",
      "variableList": ["SKU", "URL"],
      "variable": "products"
    },
    {
      "action": "forLists",
      "content": "products",
      "variable": "for_list_item",
      "do": [
        {
          "action": "combineProcess",
          "groupName": "提取字段",
          "blocks": [
            {"action": "getField", "data": "${for_list_item}", "key": "SKU", "saveTo": "sku"},
            {"action": "getField", "data": "${for_list_item}", "key": "URL", "saveTo": "url"}
          ]
        },
        {
          "action": "combineProcess",
          "groupName": "访问页面",
          "blocks": [
            {"action": "visit", "url": "${url}", "timeout": 10000},
            {"action": "wait", "timeout": 5000},
            {"action": "scroll", "position": "middle"}
          ]
        },
        {
          "action": "combineProcess",
          "groupName": "提取页面数据",
          "blocks": [
            {"action": "js", "code": "return document.querySelector('.price').textContent", "saveTo": "price"},
            {"action": "js", "code": "return document.querySelector('.shipping').textContent", "saveTo": "shipmethod"}
          ]
        },
        {"action": "saveExcel", "filename": "产品抓取结果.xlsx", "columns": ["sku", "url", "price", "shipmethod"]}
      ]
    }
  ]
}
```

### Export Excel with Fields

使用 `exportExcel` 将数据导出到Excel，指定要导出的字段：

```json
{
  "action": "exportExcel",
  "name": "产品抓取结果",
  "fields": ["sku", "url", "price", "shipmethod", "QnA", "Review"],
  "remark": "Save extracted data to Excel"
}
```

### JavaScript Execution

使用 `javaScript` 执行复杂的数据提取：

```json
{
  "action": "javaScript",
  "content": "let result={}; try { let priceEl = document.evaluate('//div[@class=\"price\"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; result.price = priceEl ? priceEl.textContent.trim() : ''; } catch(e) { result.price = ''; } return JSON.stringify(result);",
  "variable": "productData",
  "remark": "Extract all product info using JavaScript"
}
```

提取单个字段：

```json
{
  "action": "javaScript",
  "params": ["productData"],
  "content": "return JSON.parse(productData).price",
  "variable": "price",
  "remark": "Extract price from JSON"
}
```

## Condition Types

- `exists` / `notExists` - Check variable existence
- `lt` / `lte` / `eq` / `neq` / `gt` / `gte` - Numeric comparison
- `contains` / `notContains` - String contains check
- `in` / `notIn` - Array membership

## Variables

Use `${variableName}` syntax to reference variables:

```json
{"action": "input", "selector": "#email", "content": "${userEmail}"}
```

## Importing to AdsPower

1. Open AdsPower
2. Navigate to RPA Plus
3. Click "Import Flow"
4. Paste or upload the generated JSON
5. Review and save

## See Also

- `README.md` - Full documentation
- `QUICKREF.md` - Quick reference guide
- `examples/` - Example flow definitions
