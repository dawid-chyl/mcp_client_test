#!/usr/bin/env python3
"""
Universal MCP Client Template
Works with any MCP server - just update mcp.json
"""

import asyncio
import json
import sys
from fastmcp import Client


async def demo_mcp_server():
    """Demo any MCP server"""
    
    print("🌐 Universal MCP Client")
    print("=" * 40)
    
    # Load MCP config
    try:
        with open("mcp.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Create mcp.json with your server config")
        return
    
    # Show configured servers
    servers = list(config.get("mcpServers", {}).keys())
    print(f"🔗 Servers: {', '.join(servers)}")
    
    # Connect
    client = Client(config)
    
    async with client:
        print("✅ Connected!")
        
        # Basic info
        await client.ping()
        print("🏓 Ping: OK")
        
        # Discovery
        tools = await client.list_tools()
        print(f"\n🛠️  Tools found: {len(tools)}")
        
        # List all tools
        if tools:
            for i, tool in enumerate(tools, 1):
                print(f"  {i:2d}. {tool.name}")
                if hasattr(tool, 'description') and tool.description:
                    print(f"      {tool.description}")
        
        # Interactive tool selection
        if tools and len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            await interactive_tool_usage(client, tools)


async def interactive_tool_usage(client, tools):
    """Interactive tool testing"""
    print(f"\n🎮 Interactive Mode")
    print("=" * 40)
    
    while True:
        try:
            print(f"\nEnter tool number (1-{len(tools)}) or 'q' to quit:")
            choice = input("> ").strip()
            
            if choice.lower() == 'q':
                break
            
            try:
                tool_index = int(choice) - 1
                if 0 <= tool_index < len(tools):
                    tool = tools[tool_index]
                    print(f"\n🎯 Calling: {tool.name}")
                    
                    # Try calling with empty params first
                    result = await client.call_tool(tool.name, {})
                    
                    if result:
                        print("✅ Success!")
                        # Show first part of result
                        if hasattr(result[0], 'text'):
                            text = result[0].text
                            if len(text) > 500:
                                print(f"📄 Result (first 500 chars): {text[:500]}...")
                            else:
                                print(f"📄 Result: {text}")
                    else:
                        print("⚠️  No result returned")
                        
                else:
                    print("❌ Invalid number")
                    
            except ValueError:
                print("❌ Enter a number")
            except Exception as e:
                print(f"⚠️  Tool failed: {e}")
                
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    print("🚀 Universal MCP Client")
    print("📋 Add any MCP server to mcp.json")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage:")
        print("  python universal_mcp.py              # List tools")
        print("  python universal_mcp.py --interactive # Interactive mode")
    else:
        asyncio.run(demo_mcp_server()) 