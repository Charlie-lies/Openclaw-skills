# AdsPower RPA Flow Generator - Quick Reference

## Quick Examples

### 1. Simple Website Visit
```json
{
  "steps": [
    {"action": "visit", "url": "https://example.com"},
    {"action": "wait", "timeout": 3000}
  ]
}
```

### 2. Click and Input
```json
{
  "steps": [
    {"action": "visit", "url": "https://example.com"},
    {"action": "click", "selector": "#login-btn"},
    {"action": "input", "selector": "#email", "content": "user@example.com"},
    {"action": "input", "selector": "#password", "content": "password123"},
    {"action": "click", "selector": "#submit"}
  ]
}
```

### 3. Extract Data
```json
{
  "steps": [
    {"action": "visit", "url": "https://example.com/products"},
    {"action": "extract", "selector": ".product-title", "extractType": "text", "saveTo": "title"},
    {"action": "extract", "selector": ".product-price", "extractType": "text", "saveTo": "price"},
    {"action": "saveExcel", "filename": "products.xlsx", "columns": ["title", "price"]}
  ]
}
```

### 4. Loop Through Elements
```json
{
  "steps": [
    {"action": "visit", "url": "https://example.com/list"},
    {
      "action": "forElements",
      "selector": ".item",
      "saveTo": "item",
      "do": [
        {"action": "extract", "element": "${item}", "extractType": "text", "selector": ".name", "saveTo": "name"},
        {"action": "click", "element": "${item}"},
        {"action": "wait", "timeout": 2000},
        {"action": "goBack"}
      ]
    }
  ]
}
```

### 5. Conditional Logic
```json
{
  "steps": [
    {"action": "extract", "selector": ".status", "extractType": "text", "saveTo": "status"},
    {
      "action": "if",
      "variable": "status",
      "condition": "eq",
      "value": "active",
      "then": [
        {"action": "click", "selector": ".process-btn"}
      ],
      "else": [
        {"action": "click", "selector": ".activate-btn"}
      ]
    }
  ]
}
```

### 6. Use Excel Data
```json
{
  "steps": [
    {"action": "importExcel", "path": "C:/data/users.xlsx", "variableList": ["name", "email"], "variable": "users"},
    {
      "action": "forData",
      "data": "${users}",
      "saveTo": "user",
      "do": [
        {"action": "getField", "data": "${user}", "key": "email", "saveTo": "userEmail"},
        {"action": "visit", "url": "https://example.com/register"},
        {"action": "input", "selector": "#email", "content": "${userEmail}"}
      ]
    }
  ]
}
```

### 7. Random Delays (Human-like)
```json
{
  "steps": [
    {"action": "visit", "url": "https://example.com"},
    {"action": "wait", "timeoutType": "random", "timeoutMin": 2000, "timeoutMax": 5000},
    {"action": "click", "selector": "#btn"},
    {"action": "wait", "timeoutType": "random", "timeoutMin": 1000, "timeoutMax": 3000}
  ]
}
```

### 8. Multiple Browser Windows
```json
{
  "steps": [
    {"action": "visit", "url": "https://site-a.com"},
    {"action": "newBrowser", "envId": "12345", "onComplete": "keep"},
    {"action": "visit", "url": "https://site-b.com"},
    {"action": "closeBrowser"}
  ]
}
```

### 9. Scrolling
```json
{
  "steps": [
    {"action": "visit", "url": "https://example.com"},
    {"action": "scroll", "position": "bottom", "scrollType": "smooth"},
    {"action": "scroll", "distance": 500, "type": "instant"}
  ]
}
```

### 10. Screenshot
```json
{
  "steps": [
    {"action": "visit", "url": "https://example.com"},
    {"action": "screenshot", "name": "homepage", "fullScreen": true, "format": "png"}
  ]
}
```

## Action Type Quick List

| Category | Actions |
|----------|---------|
| Navigation | `visit`, `newTab`, `closeTab`, `closeOtherTabs`, `switchTab`, `refresh`, `goBack` |
| Interaction | `click`, `input`, `scroll`, `hover`, `select`, `focus`, `upload`, `js` |
| Keyboard | `key` (Enter, Tab, Esc...), `hotkey` (Ctrl+A, Ctrl+C...) |
| Wait | `wait`, `waitFor`, `waitRequest` |
| Extract | `extract`, `getUrl`, `getClipboard`, `getFocused` |
| Save | `saveFile`, `saveExcel`, `download` |
| Import | `importExcel`, `importTxt` |
| Process | `regex`, `toJson`, `getField`, `randomPick` |
| Loop | `forElements`, `forCount`, `forData`, `while`, `break` |
| Logic | `if`, `group` |
| Browser | `newBrowser`, `closeBrowser` |
| Env | `setRemark`, `setTag` |

## Condition Types for IF/WHILE

- `exists` / `notExists` - Variable exists check
- `lt` / `lte` / `eq` / `neq` / `gt` / `gte` - Numeric comparison
- `contains` / `notContains` - String contains check
- `in` / `notIn` - Array membership check

## Variable Usage

Use `${variableName}` syntax:
```json
{"action": "input", "selector": "#email", "content": "${userEmail}"}
```

## Selector Types

- CSS: `"selector": "#id"` or `".class"` or `"input[type='text']"`
- XPath: `"selectorType": "xpath"`, `"selector": "//div[@class='item']"`
- Text: `"selectorType": "text"`, `"selector": "Click Here"`

## Extract Types

- `text` - Element text content
- `object` - Element as object
- `src` - Inner HTML
- `attr` - Attribute value (specify `attr` param)
- `child` - Child element
- `iframe` - As iframe object
