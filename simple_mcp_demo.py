#!/usr/bin/env python3
"""
Simple MCP Demo using FastMCP
Based on official documentation - clean and simple
"""

import asyncio
import json
from fastmcp import Client


async def main():
    """Simple demonstration of MCP client"""
    
    print("🚀 Simple MCP Demo")
    print("=" * 40)
    
    # Load config
    with open("mcp.json", "r") as f:
        config = json.load(f)
    
    # Create client - that's it!
    client = Client(config)
    
    # Use async context manager
    async with client:
        print("✅ Connected!")
        
        # Test connection
        await client.ping()
        print("🏓 Ping: OK")
        
        # Discover tools
        print("\n🔧 Available tools:")
        tools = await client.list_tools()
        
        for tool in tools:
            print(f"  • {tool.name} - {tool.description}")
        
        print(f"\n📊 Total tools: {len(tools)}")
        
        # Try a simple tool call
        print("\n🎯 Testing tool call...")
        try:
            result = await client.call_tool("atlassianUserInfo", {})
            print("✅ Tool call successful!")
            print(f"📄 Result: {result}")
        except Exception as e:
            print(f"⚠️  Tool call failed: {e}")
            print("💡 This is expected without proper auth")


if __name__ == "__main__":
    asyncio.run(main()) 