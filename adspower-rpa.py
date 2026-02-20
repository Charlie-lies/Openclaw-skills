#!/usr/bin/env python3
"""
OpenClaw Skill: AdsPower RPA Flow Generator
Entry point for OpenClaw skill system.
"""

import sys
import os
import json
import argparse

# Add skill directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate import AdsPowerRPAGenerator


def print_usage():
    print("""
AdsPower RPA Flow Generator
===========================

Generate JSON automation flows for AdsPower browser RPA.

Usage:
    openclaw skill adspower-rpa <command> [options]

Commands:
    generate    Generate a flow from JSON definition
    validate    Validate a flow definition
    template    Generate a template flow

Generate Options:
    --file, -f      Read definition from JSON file
    --output, -o    Output file path
    --pretty, -p    Pretty print JSON output

Examples:
    # Generate from inline JSON
    openclaw skill adspower-rpa generate '{"steps":[{"action":"visit","url":"https://example.com"}]}'
    
    # Generate from file
    openclaw skill adspower-rpa generate --file examples/amazon-search.json --output flow.json
    
    # Generate template
    openclaw skill adspower-rpa template --output template.json
    
    # Validate flow
    openclaw skill adspower-rpa validate --file my-flow.json

Action Types:
    Page:       visit, newTab, closeTab, refresh, goBack, screenshot
                click, input, scroll, hover, select, focus, upload, js
    Keyboard:   key, hotkey
    Wait:       wait, waitFor, waitRequest
    Data:       extract, getUrl, getClipboard, getFocused, saveFile
                saveExcel, download, importExcel, importTxt, getEmail, get2FA
    Process:    regex, toJson, getField, randomPick
    Flow:       if, forElements, forCount, forData, while, break
                group, newBrowser, closeBrowser, useFlow
    Env:        setRemark, setTag
""")


def cmd_generate(args):
    """Generate flow from definition."""
    generator = AdsPowerRPAGenerator()
    
    # Get definition
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            definition = json.load(f)
    elif args.definition:
        definition = json.loads(args.definition)
    else:
        print("Error: No definition provided. Use --file or provide JSON inline.")
        return 1
    
    # Generate
    flow = generator.generate(definition)
    
    # Output
    indent = 2 if args.pretty else None
    output = json.dumps(flow, indent=indent, ensure_ascii=False)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[OK] Flow saved to: {args.output}")
        print(f"  Steps: {len(flow)}")
    else:
        print(output)
    
    return 0


def cmd_validate(args):
    """Validate a flow definition."""
    if not args.file:
        print("Error: --file required for validation")
        return 1
    
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            definition = json.load(f)
        
        # Try to generate
        generator = AdsPowerRPAGenerator()
        flow = generator.generate(definition)
        
        print(f"[OK] Valid flow definition")
        print(f"  Name: {definition.get('name', 'N/A')}")
        print(f"  Steps: {len(definition.get('steps', []))}")
        print(f"  Generated nodes: {len(flow)}")
        return 0
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Validation error: {e}")
        return 1


def cmd_template(args):
    """Generate a template flow definition."""
    template = {
        "name": "My Automation Flow",
        "description": "Describe what this flow does",
        "steps": [
            {
                "action": "visit",
                "url": "https://example.com",
                "remark": "Open target website"
            },
            {
                "action": "wait",
                "timeout": 3000
            },
            {
                "action": "click",
                "selector": "#button-id",
                "remark": "Click the button"
            },
            {
                "action": "input",
                "selector": "#input-id",
                "content": "input text",
                "remark": "Enter text"
            }
        ]
    }
    
    output = json.dumps(template, indent=2, ensure_ascii=False)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[OK] Template saved to: {args.output}")
    else:
        print(output)
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="AdsPower RPA Flow Generator",
        add_help=False
    )
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("definition", nargs="?", help="JSON definition (for generate)")
    parser.add_argument("--file", "-f", help="Input file path")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--pretty", "-p", action="store_true", help="Pretty print")
    parser.add_argument("--help", "-h", action="store_true", help="Show help")
    
    args = parser.parse_args()
    
    if args.help or not args.command:
        print_usage()
        return 0
    
    commands = {
        "generate": cmd_generate,
        "validate": cmd_validate,
        "template": cmd_template,
    }
    
    cmd = commands.get(args.command)
    if not cmd:
        print(f"Unknown command: {args.command}")
        print_usage()
        return 1
    
    return cmd(args)


if __name__ == "__main__":
    sys.exit(main())
