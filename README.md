# AdsPower RPA Flow Generator

Generate JSON automation flows for AdsPower browser RPA.

## Quick Start

```bash
# Generate a simple flow
openclaw skill adspower-rpa generate --name "amazon-search" --description "Search on Amazon"

# Generate with inline JSON definition
openclaw skill adspower-rpa generate '
{
  "name": "Auto Login",
  "description": "Login automation",
  "steps": [
    {"action": "visit", "url": "https://example.com/login"},
    {"action": "input", "selector": "#email", "content": "user@example.com"},
    {"action": "input", "selector": "#password", "content": "password123"},
    {"action": "click", "selector": "#login-btn"}
  ]
}'
```

## JSON Flow Structure

### Basic Node Format

```json
{
  "type": "actionType",
  "config": {
    "param1": "value1",
    "param2": "value2",
    "remark": "optional description"
  }
}
```

### Available Action Types

#### Page Operations (`page`)
| Type | Description | Key Params |
|------|-------------|------------|
| `newPage` | Open new tab | - |
| `closePage` | Close current tab | - |
| `closeOtherPage` | Close other tabs | - |
| `switchPage` | Switch tab | `condition`, `pageInfo` |
| `gotoUrl` | Visit URL | `url`, `timeout` |
| `refresh` | Refresh page | - |
| `goBack` | Page back | - |
| `screenshot` | Take screenshot | `name`, `fullScreen`, `format` |
| `hoverElement` | Mouse hover | `selector`, `selectorType` |
| `selectDropdown` | Select dropdown | `selector`, `value` |
| `focusElement` | Focus element | `selector` |
| `clickElement` | Click element | `selector`, `clickType`, `keyType` |
| `inputContent` | Input text | `selector`, `content`, `intervals` |
| `scrollPage` | Scroll page | `distance`, `type` |
| `uploadFile` | Upload file | `selector`, `filePath` |
| `executeJs` | Run JavaScript | `code`, `injectVariable` |

#### Keyboard Operations (`keyboard`)
| Type | Description | Key Params |
|------|-------------|------------|
| `keyPress` | Press key | `key` (Enter, Tab, Esc, etc.) |
| `keyCombination` | Key combo | `combination` (Ctrl+A, Ctrl+C, etc.) |

#### Wait Operations (`wait`)
| Type | Description | Key Params |
|------|-------------|------------|
| `waitTime` | Wait duration | `timeoutType` (fixed/randomInterval), `timeout` |
| `waitElement` | Wait for element | `selector`, `visible`, `timeout` |
| `waitRequest` | Wait for request | `url`, `timeout` |

#### Data Operations (`data`)
| Type | Description | Key Params |
|------|-------------|------------|
| `getUrl` | Extract URL info | `extractType` (full/root/param), `saveTo` |
| `getClipboard` | Get clipboard | `saveTo` |
| `elementData` | Extract element data | `selector`, `extractType` (text/object/src/attr/child) |
| `focusedElement` | Get focused element | `saveTo` |
| `saveToFile` | Save to txt | `filename`, `template` |
| `saveToExcel` | Save to Excel | `filename`, `columns` |
| `downloadFile` | Download file | `url`, `savePath` |
| `useExcel` | Import Excel | `path`, `variableList` |
| `importText` | Import txt | `path` |
| `getEmail` | Fetch email | `email`, `password`, `server` |
| `get2FACode` | 2FA code | `secret` |

#### Data Processing (`process`)
| Type | Description | Key Params |
|------|-------------|------------|
| `extractText` | Regex extract | `data`, `rule` |
| `toJson` | Convert to JSON | `variable` |
| `extractKey` | Extract field | `content`, `key` |
| `randomGet` | Random extract | `content` |

#### Flow Control (`flow`)
| Type | Description | Key Params |
|------|-------------|------------|
| `group` | Group nodes | `name` |
| `newBrowser` | Launch browser | `envId`, `onComplete` |
| `ifCondition` | If condition | `variable`, `condition`, `result` |
| `forElements` | For loop (elements) | `selector`, `variable`, `variableIndex` |
| `forCount` | For loop (count) | `count`, `variableIndex` |
| `forLists` | For loop (data) | `content`, `variable`, `variableIndex` |
| `breakLoop` | Exit loop | - |
| `closeBrowser` | Close browser | - |
| `whileLoop` | While loop | `variable`, `condition`, `result` |
| `useFlow` | Use other flow | `flowId` |

#### Environment Info (`env`)
| Type | Description | Key Params |
|------|-------------|------------|
| `updateRemark` | Update remark | `content`, `mode` (append/replace) |
| `updateTag` | Update tag | `tags`, `mode` (append/replace) |

## Selector Types

- `selector` - CSS selector (e.g., `#id`, `.class`, `input[type="text"]`)
- `xpath` - XPath expression (e.g., `//div[@class='item']`)
- `text` - Text content matching

## Variables

Use `${variableName}` to reference variables:

```json
{
  "type": "gotoUrl",
  "config": {
    "url": "${targetUrl}",
    "timeout": 30000
  }
}
```

## Condition Types

- `exists` / `notExists` - Variable existence
- `lt` / `lte` / `eq` / `neq` / `gt` / `gte` - Numeric comparison
- `contains` / `notContains` - String contains
- `in` / `notIn` - In array

## Complete Example

```json
{
  "name": "Amazon Product Search",
  "description": "Search products on Amazon and extract data",
  "flow": [
    {
      "type": "gotoUrl",
      "config": {
        "url": "https://www.amazon.com",
        "timeout": 30000,
        "remark": "Visit Amazon homepage"
      }
    },
    {
      "type": "waitTime",
      "config": {
        "timeoutType": "randomInterval",
        "timeoutMin": 2000,
        "timeoutMax": 3000
      }
    },
    {
      "type": "inputContent",
      "config": {
        "selector": "#twotabsearchtextbox",
        "content": "iPhone 15",
        "selectorType": "selector",
        "serialType": "fixedValue",
        "serial": 1,
        "intervals": 100
      }
    },
    {
      "type": "keyPress",
      "config": {
        "key": "Enter"
      }
    },
    {
      "type": "waitElement",
      "config": {
        "selector": ".s-result-item",
        "timeout": 10000
      }
    },
    {
      "type": "forElements",
      "config": {
        "selector": ".s-result-item",
        "variable": "product",
        "variableIndex": "index",
        "extractType": "object",
        "children": [
          {
            "type": "elementData",
            "config": {
              "element": "${product}",
              "extractType": "text",
              "selector": "h2 a span",
              "saveTo": "productTitle"
            }
          },
          {
            "type": "saveToExcel",
            "config": {
              "filename": "products.xlsx",
              "columns": ["productTitle"]
            }
          }
        ]
      }
    }
  ]
}
```

## Examples

The `examples/` folder contains ready-to-use flow definitions demonstrating various automation scenarios:

### 馃搧 Available Examples

| Example | Description | Key Features |
|---------|-------------|--------------|
| `template.json` | Basic template | Simple visit, wait, click, input actions |
| `test-google-search.json` | Google search automation | Random waits, typing simulation, screenshot |
| `amazon-search.json` | Amazon product search | Element loops, data extraction, Excel export |
| `auto-login.json` | Batch login with Excel | Excel import, data loop, form automation |
| `conditional-scraping.json` | Smart data scraping | Conditions, pagination, nested loops |
| `product-scraper-flow.json` | Product data extraction | XPath selectors, multi-field extraction |
| `product-scraper-js.json` | JavaScript extraction | JS data extraction, JSON parsing |
| `product-scraper-js-manualfixed.json` | **猸?Recommended** | CombineProcess grouping, visual organization |
| `social-media-poster.json` | Multi-platform posting | Conditional logic, image upload |
| `youtube-browser.json` | YouTube automation | Random selection, video browsing |

### 馃殌 How to Use Examples

#### 1. Direct Import to AdsPower

```bash
# Copy the JSON content from any example file
cat examples/amazon-search.json | pbcopy  # macOS
cat examples/amazon-search.json | xclip -selection clipboard  # Linux
type examples\amazon-search.json | clip  # Windows
```

Then in AdsPower:
1. Open **RPA Plus**
2. Click **"Import Flow"** (瀵煎叆娴佺▼)
3. Paste the JSON content
4. Click **"Confirm"** to import

#### 2. Generate Using the Skill

```bash
# Generate flow from example
openclaw skill adspower-rpa generate --file examples/amazon-search.json --output my-flow.json

# Or use the Python script directly
python generate.py examples/amazon-search.json --output my-flow.json
```

#### 3. Modify for Your Needs

Edit the example JSON to customize:
- **URLs**: Change target websites
- **Selectors**: Update CSS/XPath for your target page
- **Excel paths**: Update file paths for data import/export
- **Timeouts**: Adjust wait times based on page load speed

### 馃搳 Example: Product Scraper with Excel

The `product-scraper-js-manualfixed.json` is the most complete example showing:

1. **Excel Import** (`useExcel`): Import product data from Excel
2. **Data Loop** (`forLists`): Iterate through each product row
3. **Process Grouping** (`combineProcess`): Visually organize steps
   - Group 1: Extract fields (SKU, URL)
   - Group 2: Visit page and wait
   - Group 3: Extract data using JavaScript
4. **JavaScript Extraction**: Extract multiple fields in one JS execution
5. **Excel Export** (`exportExcel`): Save results to Excel

**Excel format expected:**
| SKU | URL |
|-----|-----|
| PD001 | https://example.com/pd001 |
| PD002 | https://example.com/pd002 |

### 馃И Quick Test Example

Start with `test-google-search.json` to verify your setup:

```bash
# Import this example to AdsPower
# It will:
# 1. Open Google
# 2. Search for "AdsPower RPA automation"
# 3. Take a screenshot
```

### 鈿狅笍 Important Notes

1. **Excel Paths**: Update file paths in examples to match your system:
   - Windows: `C:/data/accounts.xlsx` or `C:\\data\\accounts.xlsx`
   - macOS/Linux: `/Users/username/data/accounts.xlsx`

2. **Selectors**: Website structures change. If an example fails:
   - Open the target website in browser
   - Use DevTools (F12) to inspect elements
   - Update CSS/XPath selectors accordingly

3. **Timeouts**: Adjust based on your internet speed and page complexity

## Import/Export

The generated JSON can be imported directly into AdsPower RPA:
1. Open AdsPower 鈫?RPA Plus
2. Click "Import Flow" (瀵煎叆娴佺▼)
3. Paste the generated JSON
4. Review and save

## Advanced Features

### Nested Loops

```json
{
  "type": "forElements",
  "config": {
    "selector": ".category",
    "variable": "category",
    "children": [
      {
        "type": "forCount",
        "config": {
          "count": 3,
          "variableIndex": "itemNum",
          "children": [
            { "type": "clickElement", "config": { "selector": ".item" } }
          ]
        }
      }
    ]
  }
}
```

### Conditional Logic

```json
{
  "type": "ifCondition",
  "config": {
    "variable": "status",
    "condition": "eq",
    "result": "success",
    "children": [
      { "type": "executeJs", "config": { "code": "console.log('Success!')" } }
    ],
    "elseChildren": [
      { "type": "refresh", "config": {} }
    ]
  }
}
```

### Using Excel Data

```json
[
  {
    "type": "useExcel",
    "config": {
      "path": "C:/data/accounts.xlsx",
      "variableList": ["email", "password"],
      "variable": "accounts"
    }
  },
  {
    "type": "forLists",
    "config": {
      "content": "${accounts}",
      "variable": "account",
      "variableIndex": "idx",
      "children": [
        {
          "type": "extractKey",
          "config": {
            "content": "${account}",
            "key": "email",
            "variable": "userEmail"
          }
        },
        {
          "type": "inputContent",
          "config": {
            "selector": "#email",
            "content": "${userEmail}"
          }
        }
      ]
    }
  }
]
```
