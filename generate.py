#!/usr/bin/env python3
"""
AdsPower RPA Flow Generator
Generates JSON automation flows for AdsPower browser RPA.
"""

import json
import sys
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime


class AdsPowerRPAGenerator:
    """Generator for AdsPower RPA JSON flows."""
    
    # Action type mappings (simplified -> actual)
    ACTION_MAP = {
        # Page operations
        "visit": "gotoUrl",
        "newTab": "newPage",
        "closeTab": "closePage",
        "closeOtherTabs": "closeOtherPage",
        "switchTab": "switchPage",
        "refresh": "refresh",
        "goBack": "goBack",
        "screenshot": "screenshot",
        "hover": "hoverElement",
        "select": "selectDropdown",
        "focus": "focusElement",
        "click": "clickElement",
        "input": "inputContent",
        "scroll": "scrollPage",
        "upload": "uploadFile",
        "js": "executeJs",
        
        # Keyboard
        "key": "keyPress",
        "hotkey": "keyCombination",
        
        # Wait
        "wait": "waitTime",
        "waitFor": "waitElement",
        "waitRequest": "waitRequest",
        
        # Data extraction
        "getUrl": "getUrl",
        "getClipboard": "getClipboard",
        "extract": "elementData",
        "getFocused": "focusedElement",
        "saveFile": "saveToFile",
        "saveExcel": "saveToExcel",
        "download": "downloadFile",
        "importExcel": "useExcel",
        "importTxt": "importText",
        "getEmail": "getEmail",
        "get2FA": "get2FACode",
        
        # Data processing
        "regex": "extractText",
        "toJson": "toJson",
        "getField": "extractKey",
        "randomPick": "randomGet",
        
        # Flow control
        "group": "group",
        "newBrowser": "newBrowser",
        "if": "ifCondition",
        "forElements": "forElements",
        "forCount": "forCount",
        "forData": "forLists",
        "break": "breakLoop",
        "closeBrowser": "closeBrowser",
        "while": "whileLoop",
        "useFlow": "useFlow",
        
        # Environment
        "setRemark": "updateRemark",
        "setTag": "updateTag",
    }
    
    # Default timeouts
    DEFAULT_TIMEOUT = 30000
    DEFAULT_WAIT_MIN = 2000
    DEFAULT_WAIT_MAX = 5000
    
    def __init__(self):
        self.variables = set()
    
    def generate(self, definition: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate AdsPower RPA JSON flow from simplified definition.
        
        Args:
            definition: Dict with 'name', 'description', and 'steps'
        
        Returns:
            List of flow nodes in AdsPower format
        """
        steps = definition.get("steps", [])
        flow = []
        
        for step in steps:
            node = self._convert_step(step)
            if node:
                flow.append(node)
        
        return flow
    
    def _convert_step(self, step: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Convert a simplified step to AdsPower node format."""
        action = step.get("action", "")
        actual_type = self.ACTION_MAP.get(action, action)
        
        # Route to specific converter based on action type
        converters = {
            "gotoUrl": self._make_visit,
            "newPage": self._make_new_tab,
            "closePage": self._make_close_tab,
            "closeOtherPage": self._make_close_other_tabs,
            "switchPage": self._make_switch_tab,
            "refresh": self._make_refresh,
            "goBack": self._make_go_back,
            "screenshot": self._make_screenshot,
            "hoverElement": self._make_hover,
            "selectDropdown": self._make_select,
            "focusElement": self._make_focus,
            "clickElement": self._make_click,
            "inputContent": self._make_input,
            "scrollPage": self._make_scroll,
            "uploadFile": self._make_upload,
            "executeJs": self._make_js,
            "keyPress": self._make_key_press,
            "keyCombination": self._make_hotkey,
            "waitTime": self._make_wait,
            "waitElement": self._make_wait_for,
            "waitRequest": self._make_wait_request,
            "getUrl": self._make_get_url,
            "getClipboard": self._make_get_clipboard,
            "elementData": self._make_extract,
            "focusedElement": self._make_get_focused,
            "saveToFile": self._make_save_file,
            "saveToExcel": self._make_save_excel,
            "downloadFile": self._make_download,
            "useExcel": self._make_import_excel,
            "importText": self._make_import_txt,
            "getEmail": self._make_get_email,
            "get2FACode": self._make_get_2fa,
            "extractText": self._make_regex,
            "toJson": self._make_to_json,
            "extractKey": self._make_get_field,
            "randomGet": self._make_random_pick,
            "group": self._make_group,
            "newBrowser": self._make_new_browser,
            "ifCondition": self._make_if,
            "forElements": self._make_for_elements,
            "forCount": self._make_for_count,
            "forLists": self._make_for_data,
            "breakLoop": self._make_break,
            "closeBrowser": self._make_close_browser,
            "whileLoop": self._make_while,
            "useFlow": self._make_use_flow,
            "updateRemark": self._make_set_remark,
            "updateTag": self._make_set_tag,
        }
        
        converter = converters.get(actual_type)
        if converter:
            return converter(step)
        
        # Generic fallback
        return {"type": actual_type, "config": {k: v for k, v in step.items() if k != "action"}}
    
    # ==================== Page Operations ====================
    
    def _make_visit(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "gotoUrl",
            "config": {
                "url": step.get("url", ""),
                "timeout": step.get("timeout", self.DEFAULT_TIMEOUT),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_new_tab(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "newPage", "config": {"remark": step.get("remark", "")}}
    
    def _make_close_tab(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "closePage", "config": {"remark": step.get("remark", "")}}
    
    def _make_close_other_tabs(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "closeOtherPage", "config": {"remark": step.get("remark", "")}}
    
    def _make_switch_tab(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "switchPage",
            "config": {
                "condition": step.get("condition", "title"),
                "pageInfo": step.get("pageInfo", ""),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_refresh(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "refresh", "config": {"remark": step.get("remark", "")}}
    
    def _make_go_back(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "goBack", "config": {"remark": step.get("remark", "")}}
    
    def _make_screenshot(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "screenshot",
            "config": {
                "name": step.get("name", ""),
                "folder": step.get("folder", "system"),
                "fullScreen": step.get("fullScreen", False),
                "format": step.get("format", "png"),
                "quality": step.get("quality", 80),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_hover(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "hoverElement",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "element": step.get("element", ""),
                "serialType": step.get("serialType", "fixedValue"),
                "serial": step.get("serial", 1),
                "serialMin": step.get("serialMin", 1),
                "serialMax": step.get("serialMax", 10),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_select(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "selectDropdown",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "element": step.get("element", ""),
                "value": step.get("value", ""),
                "serialType": step.get("serialType", "fixedValue"),
                "serial": step.get("serial", 1),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_focus(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "focusElement",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "element": step.get("element", ""),
                "serialType": step.get("serialType", "fixedValue"),
                "serial": step.get("serial", 1),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_click(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "clickElement",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "element": step.get("element", ""),
                "serialType": step.get("serialType", "fixedValue"),
                "serial": step.get("serial", 1),
                "serialMin": step.get("serialMin", 1),
                "serialMax": step.get("serialMax", 10),
                "clickType": step.get("clickType", "left"),
                "keyType": step.get("keyType", "click"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_input(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "inputContent",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "element": step.get("element", ""),
                "serialType": step.get("serialType", "fixedValue"),
                "serial": step.get("serial", 1),
                "content": step.get("content", ""),
                "isRandom": step.get("isRandom", False),
                "randomContent": step.get("randomContent", ""),
                "clearInput": step.get("clearInput", False),
                "intervals": step.get("intervals", 0),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_scroll(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "scrollPage",
            "config": {
                "distance": step.get("distance", 0),
                "type": step.get("scrollType", "smooth"),
                "scrollType": step.get("positionType", "pixel"),
                "position": step.get("position", "bottom"),
                "scrollDistance": step.get("scrollDistance", 100),
                "stopTime": step.get("stopTime", 500),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_upload(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "uploadFile",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "serialType": step.get("serialType", "fixedValue"),
                "serial": step.get("serial", 1),
                "filePath": step.get("filePath", ""),
                "fileMode": step.get("fileMode", "local"),
                "timeout": step.get("timeout", self.DEFAULT_TIMEOUT),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_js(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "executeJs",
            "config": {
                "code": step.get("code", ""),
                "injectVariable": step.get("injectVariable", ""),
                "saveTo": step.get("saveTo", ""),
                "remark": step.get("remark", "")
            }
        }
    
    # ==================== Keyboard Operations ====================
    
    def _make_key_press(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "keyPress",
            "config": {
                "key": step.get("key", "Enter"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_hotkey(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "keyCombination",
            "config": {
                "combination": step.get("combination", "Ctrl+A"),
                "remark": step.get("remark", "")
            }
        }
    
    # ==================== Wait Operations ====================
    
    def _make_wait(self, step: Dict[str, Any]) -> Dict[str, Any]:
        timeout_type = step.get("timeoutType", "fixed")
        config = {
            "timeoutType": "fixed" if timeout_type == "fixed" else "randomInterval",
            "remark": step.get("remark", "")
        }
        
        if timeout_type == "fixed":
            config["timeout"] = step.get("timeout", 3000)
        else:
            config["timeoutMin"] = step.get("timeoutMin", self.DEFAULT_WAIT_MIN)
            config["timeoutMax"] = step.get("timeoutMax", self.DEFAULT_WAIT_MAX)
        
        return {"type": "waitTime", "config": config}
    
    def _make_wait_for(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "waitElement",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "serialType": step.get("serialType", "fixedValue"),
                "serial": step.get("serial", 1),
                "visible": step.get("visible", True),
                "timeout": step.get("timeout", self.DEFAULT_TIMEOUT),
                "saveTo": step.get("saveTo", ""),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_wait_request(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "waitRequest",
            "config": {
                "url": step.get("url", ""),
                "timeout": step.get("timeout", self.DEFAULT_TIMEOUT),
                "remark": step.get("remark", "")
            }
        }
    
    # ==================== Data Operations ====================
    
    def _make_get_url(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "getUrl",
            "config": {
                "extractType": step.get("extractType", "full"),
                "param": step.get("param", ""),
                "saveTo": step.get("saveTo", "url"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_get_clipboard(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "getClipboard",
            "config": {
                "saveTo": step.get("saveTo", "clipboard"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_extract(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "elementData",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "element": step.get("element", ""),
                "serialType": step.get("serialType", "fixedValue"),
                "serial": step.get("serial", 1),
                "serialMin": step.get("serialMin", 1),
                "serialMax": step.get("serialMax", 10),
                "extractType": step.get("extractType", "text"),
                "attr": step.get("attr", ""),
                "childSelector": step.get("childSelector", ""),
                "saveTo": step.get("saveTo", "data"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_get_focused(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "focusedElement",
            "config": {
                "saveTo": step.get("saveTo", "focused"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_save_file(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "saveToFile",
            "config": {
                "filename": step.get("filename", "output.txt"),
                "template": step.get("template", ""),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_save_excel(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "saveToExcel",
            "config": {
                "filename": step.get("filename", "output.xlsx"),
                "columns": step.get("columns", []),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_download(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "downloadFile",
            "config": {
                "url": step.get("url", ""),
                "savePath": step.get("savePath", ""),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_import_excel(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "useExcel",
            "config": {
                "path": step.get("path", ""),
                "variableList": step.get("variableList", []),
                "variable": step.get("variable", "excel_data"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_import_txt(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "importText",
            "config": {
                "path": step.get("path", ""),
                "variable": step.get("variable", "txt_data"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_get_email(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "getEmail",
            "config": {
                "email": step.get("email", ""),
                "password": step.get("password", ""),
                "server": step.get("server", ""),
                "port": step.get("port", 993),
                "clientId": step.get("clientId", ""),
                "clientSecret": step.get("clientSecret", ""),
                "refreshToken": step.get("refreshToken", ""),
                "status": step.get("status", "all"),
                "markRead": step.get("markRead", False),
                "includeSpam": step.get("includeSpam", False),
                "timeRange": step.get("timeRange", ""),
                "sender": step.get("sender", ""),
                "subject": step.get("subject", ""),
                "rule": step.get("rule", ""),
                "saveTo": step.get("saveTo", "email"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_get_2fa(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "get2FACode",
            "config": {
                "secret": step.get("secret", ""),
                "saveTo": step.get("saveTo", "code2fa"),
                "remark": step.get("remark", "")
            }
        }
    
    # ==================== Data Processing ====================
    
    def _make_regex(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "extractText",
            "config": {
                "data": step.get("data", ""),
                "rule": step.get("rule", ""),
                "firstOnly": step.get("firstOnly", True),
                "saveTo": step.get("saveTo", "extracted"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_to_json(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "toJson",
            "config": {
                "variable": step.get("data", ""),
                "saveTo": step.get("saveTo", "jsonData"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_get_field(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "extractKey",
            "config": {
                "content": step.get("data", ""),
                "key": step.get("key", ""),
                "variable": step.get("saveTo", "field"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_random_pick(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "randomGet",
            "config": {
                "content": step.get("data", ""),
                "variable": step.get("saveTo", "random"),
                "remark": step.get("remark", "")
            }
        }
    
    # ==================== Flow Control ====================
    
    def _make_group(self, step: Dict[str, Any]) -> Dict[str, Any]:
        children = []
        for child_step in step.get("steps", []):
            child_node = self._convert_step(child_step)
            if child_node:
                children.append(child_node)
        
        return {
            "type": "group",
            "config": {
                "name": step.get("name", "Group"),
                "children": children,
                "remark": step.get("remark", "")
            }
        }
    
    def _make_new_browser(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "newBrowser",
            "config": {
                "envId": step.get("envId", ""),
                "onComplete": step.get("onComplete", "keep"),
                "onError": step.get("onError", "skip"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_if(self, step: Dict[str, Any]) -> Dict[str, Any]:
        children = []
        for child_step in step.get("then", []):
            child_node = self._convert_step(child_step)
            if child_node:
                children.append(child_node)
        
        else_children = []
        for child_step in step.get("else", []):
            child_node = self._convert_step(child_step)
            if child_node:
                else_children.append(child_node)
        
        return {
            "type": "ifCondition",
            "config": {
                "variable": step.get("variable", ""),
                "condition": step.get("condition", "eq"),
                "result": step.get("value", ""),
                "children": children,
                "elseChildren": else_children,
                "remark": step.get("remark", "")
            }
        }
    
    def _make_for_elements(self, step: Dict[str, Any]) -> Dict[str, Any]:
        children = []
        for child_step in step.get("do", []):
            child_node = self._convert_step(child_step)
            if child_node:
                children.append(child_node)
        
        return {
            "type": "forElements",
            "config": {
                "selector": step.get("selector", ""),
                "selectorType": step.get("selectorType", "selector"),
                "extractType": step.get("extractType", "object"),
                "variable": step.get("saveTo", "item"),
                "variableIndex": step.get("saveIndexTo", "index"),
                "children": children,
                "remark": step.get("remark", "")
            }
        }
    
    def _make_for_count(self, step: Dict[str, Any]) -> Dict[str, Any]:
        children = []
        for child_step in step.get("do", []):
            child_node = self._convert_step(child_step)
            if child_node:
                children.append(child_node)
        
        return {
            "type": "forCount",
            "config": {
                "count": step.get("count", 1),
                "variableIndex": step.get("saveIndexTo", "index"),
                "children": children,
                "remark": step.get("remark", "")
            }
        }
    
    def _make_for_data(self, step: Dict[str, Any]) -> Dict[str, Any]:
        children = []
        for child_step in step.get("do", []):
            child_node = self._convert_step(child_step)
            if child_node:
                children.append(child_node)
        
        return {
            "type": "forLists",
            "config": {
                "content": step.get("data", ""),
                "variable": step.get("saveTo", "item"),
                "variableIndex": step.get("saveIndexTo", "index"),
                "children": children,
                "remark": step.get("remark", "")
            }
        }
    
    def _make_break(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "breakLoop", "config": {"remark": step.get("remark", "")}}
    
    def _make_close_browser(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {"type": "closeBrowser", "config": {"remark": step.get("remark", "")}}
    
    def _make_while(self, step: Dict[str, Any]) -> Dict[str, Any]:
        children = []
        for child_step in step.get("do", []):
            child_node = self._convert_step(child_step)
            if child_node:
                children.append(child_node)
        
        return {
            "type": "whileLoop",
            "config": {
                "variable": step.get("variable", ""),
                "condition": step.get("condition", "eq"),
                "result": step.get("value", ""),
                "children": children,
                "remark": step.get("remark", "")
            }
        }
    
    def _make_use_flow(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "useFlow",
            "config": {
                "flowId": step.get("flowId", ""),
                "remark": step.get("remark", "")
            }
        }
    
    # ==================== Environment ====================
    
    def _make_set_remark(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "updateRemark",
            "config": {
                "content": step.get("content", ""),
                "mode": step.get("mode", "append"),
                "remark": step.get("remark", "")
            }
        }
    
    def _make_set_tag(self, step: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": "updateTag",
            "config": {
                "tags": step.get("tags", []),
                "mode": step.get("mode", "append"),
                "remark": step.get("remark", "")
            }
        }


def main():
    parser = argparse.ArgumentParser(description="Generate AdsPower RPA JSON flow")
    parser.add_argument("definition", nargs="?", help="JSON flow definition")
    parser.add_argument("--file", "-f", help="Read definition from file")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--pretty", "-p", action="store_true", help="Pretty print JSON")
    
    args = parser.parse_args()
    
    # Read definition
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            definition = json.load(f)
    elif args.definition:
        definition = json.loads(args.definition)
    else:
        # Default example
        definition = {
            "name": "Example Flow",
            "description": "A simple example flow",
            "steps": [
                {"action": "visit", "url": "https://example.com"},
                {"action": "wait", "timeout": 3000},
                {"action": "click", "selector": "#btn"}
            ]
        }
    
    # Generate flow
    generator = AdsPowerRPAGenerator()
    flow = generator.generate(definition)
    
    # Output
    indent = 2 if args.pretty else None
    output = json.dumps(flow, indent=indent, ensure_ascii=False)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Flow saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
