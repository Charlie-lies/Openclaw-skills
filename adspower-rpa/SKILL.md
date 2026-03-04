# AdsPower RPA Skill

Generate RPA flow JSON for AdsPower fingerprint browser automation.

## Overview

This skill helps you create valid AdsPower RPA flow JSON files that can be imported directly into AdsPower's RPA module.

## JSON Format

AdsPower RPA uses a **JSON array** format where each element is a node:

```json
[
  {
    "type": "gotoUrl",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": { ... }
  },
  {
    "type": "clickElement",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": { ... }
  }
]
```

## Node Types Reference

### Navigation
- `gotoUrl` - Open a webpage
  ```json
  {
    "type": "gotoUrl",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "url": "https://example.com",
      "timeout": 30000,
      "remark": "Open website"
    }
  }
  ```

### Waiting
- `waitTime` - Wait for specified time
  ```json
  {
    "type": "waitTime",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "timeoutType": "randomInterval",
      "timeoutMin": 1500,
      "timeoutMax": 3000,
      "remark": "Random wait"
    }
  }
  ```
- `waitElement` - Wait for element to appear
  ```json
  {
    "type": "waitElement",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "selector": "#element-id",
      "selectorType": "selector",
      "visible": true,
      "timeout": 10000,
      "remark": "Wait for element"
    }
  }
  ```

### Interaction
- `clickElement` - Click on element
  ```json
  {
    "type": "clickElement",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "selector": "//button[@id='btn']",
      "selectorType": "xpath",
      "serialType": "fixedValue",
      "serial": 1,
      "remark": "Click button"
    }
  }
  ```
- `inputContent` - Type text into input field
  ```json
  {
    "type": "inputContent",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "selector": "input[name='q']",
      "selectorType": "selector",
      "serialType": "fixedValue",
      "serial": 1,
      "content": "search text",
      "clearInput": true,
      "intervals": 50,
      "remark": "Type text"
    }
  }
  ```
- `keyPress` - Press keyboard key
  ```json
  {
    "type": "keyPress",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "key": "Enter",
      "remark": "Press Enter"
    }
  }
  ```
- `scrollPage` - Scroll page
  ```json
  {
    "type": "scrollPage",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "distance": 666,
      "type": "smooth",
      "scrollType": "position",
      "position": "middle",
      "remark": "Scroll to middle"
    }
  }
  ```
- `uploadFile` - Upload file
  ```json
  {
    "type": "uploadFile",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "selector": "input[type='file']",
      "selectorType": "selector",
      "filePath": "C:/path/to/file.xlsx",
      "remark": "Upload file"
    }
  }
  ```

### Data Extraction
- `getText` / `getElement` - Extract text content
- `javaScript` - Execute JavaScript and return value
  ```json
  {
    "type": "javaScript",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "params": [],
      "content": "return document.title;",
      "srcContent": "return document.title;",
      "variable": "pageTitle",
      "remark": "Get page title"
    }
  }
  ```
- `screenshot` - Capture screenshot
  ```json
  {
    "type": "screenshot",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "name": "screenshot_name",
      "folder": "system",
      "fullScreen": true,
      "format": "png",
      "quality": 80,
      "remark": "Take screenshot"
    }
  }
  ```

### Excel Operations

#### useExcel - Import Excel as Data Source

Reads Excel file and converts it to a variable containing an array of objects.

**Rules:**
1. **Column headers become variable names** - Each column header is converted to a variable name for that column's data
2. **Header naming restrictions** - Headers can only contain letters, numbers, and underscores; cannot start with a number
3. **serial_number column** - If a column is named `serial_number`, the corresponding row content will be used as the material content for that browser environment
4. **Data format** - The entire Excel data is stored as an array of objects: `[{key1: value, key2: value...}, {key1: value, key2: value...}, ...]`

```json
{
  "type": "useExcel",
  "nodeInfo": { "search": false, "active": false, "error": false },
  "config": {
    "path": "data.xlsx",
    "variableList": ["username", "password", "email"],
    "isSkip": "0",
    "variable": "userData",
    "remark": "Import user data from Excel"
  }
}
```

**Example Excel Structure:**
| serial_number | username | password | email |
|--------------|----------|----------|-------|
| 001 | user1 | pass123 | user1@example.com |
| 002 | user2 | pass456 | user2@example.com |

**Resulting variable `userData`:**
```javascript
[
  { serial_number: "001", username: "user1", password: "pass123", email: "user1@example.com" },
  { serial_number: "002", username: "user2", password: "pass456", email: "user2@example.com" }
]
```

#### exportExcel - Export Data to Excel

Exports collected data to an Excel file.

```json
{
  "type": "exportExcel",
  "nodeInfo": { "search": false, "active": false, "error": false },
  "config": {
    "name": "output",
    "fields": ["field1", "field2"],
    "remark": "Export data"
  }
}
```

### Logic & Control
- `forLists` - Loop through list
  ```json
  {
    "type": "forLists",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "content": "excelData",
      "variableIndex": "index",
      "variable": "item",
      "hiddenChildren": false,
      "children": [ ...nested nodes... ],
      "remark": "Loop through items"
    }
  }
  ```
- `combineProcess` - Group nodes
  ```json
  {
    "type": "combineProcess",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "blocks": [
        {
          "id": "uuid",
          "data": { ...node data... },
          "selected": false
        }
      ]
    },
    "groupName": "Group Name"
  }
  ```
- `extractKey` - Extract value from object
  ```json
  {
    "type": "extractKey",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "content": "item",
      "key": "fieldName",
      "variable": "extractedValue",
      "remark": "Extract field"
    }
  }
  ```

## Variable Syntax

Use `${variableName}` to reference variables:
```json
{
  "config": {
    "url": "${productUrl}",
    "content": "${username}"
  }
}
```

## Common Selectors

- `selector` - CSS selector
- `xpath` - XPath expression
- `selectorType`: `"selector"` for CSS, `"xpath"` for XPath

## Working with Excel Data

### Import and Loop Pattern

Common pattern for processing Excel data row by row:

```json
[
  {
    "type": "useExcel",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "path": "accounts.xlsx",
      "variableList": ["username", "password"],
      "isSkip": "0",
      "variable": "accounts",
      "remark": "Load accounts from Excel"
    }
  },
  {
    "type": "forLists",
    "nodeInfo": { "search": false, "active": false, "error": false },
    "config": {
      "content": "accounts",
      "variableIndex": "index",
      "variable": "account",
      "hiddenChildren": false,
      "children": [
        {
          "type": "extractKey",
          "nodeInfo": { "search": false, "active": false, "error": false },
          "config": {
            "content": "account",
            "key": "username",
            "variable": "currentUser",
            "remark": "Get username"
          }
        },
        {
          "type": "extractKey",
          "nodeInfo": { "search": false, "active": false, "error": false },
          "config": {
            "content": "account",
            "key": "password",
            "variable": "currentPass",
            "remark": "Get password"
          }
        },
        {
          "type": "inputContent",
          "nodeInfo": { "search": false, "active": false, "error": false },
          "config": {
            "selector": "#username",
            "selectorType": "selector",
            "content": "${currentUser}",
            "clearInput": true,
            "remark": "Enter username"
          }
        }
      ],
      "remark": "Process each account"
    }
  }
]
```

## Tips

1. **Always include `nodeInfo`** with `search`, `active`, `error` fields
2. **Use `remark`** to document each step
3. **Variable references** use `${var}` syntax, not `{{var}}`
4. **Loops use `children`** array for nested nodes
5. **CombineProcess groups** related operations with `blocks` array
6. **Excel headers** must follow naming rules: letters, numbers, underscores only; no leading numbers
7. **Use `serial_number` column** to assign specific rows to browser environments
