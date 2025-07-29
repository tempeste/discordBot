#\!/usr/bin/env python3
"""
Test script for Cobbleverse server control functions
Run this to validate the implementation works correctly
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import check_cobbleverse_server, start_cobbleverse_server, stop_cobbleverse_server, restart_cobbleverse_server

async def test_check_server():
    print("=" * 50)
    print("Testing check_cobbleverse_server()...")
    print("=" * 50)
    
    try:
        ip, cpu, mem, status = await check_cobbleverse_server()
        print(f"IP Address: {ip}")
        print(f"CPU Usage: {cpu}")
        print(f"Memory Usage: {mem}")
        print(f"Server Status: {status}")
        
        if ip.startswith("Error"):
            print("\n⚠️  Server check returned an error - this is expected if server is not running")
        else:
            print("\n✅ Server check completed successfully")
            
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()

async def test_server_controls():
    print("\n" + "=" * 50)
    print("Server Control Tests (Manual Confirmation Required)")
    print("=" * 50)
    
    while True:
        print("\nSelect a test:")
        print("1. Test start_cobbleverse_server()")
        print("2. Test stop_cobbleverse_server()")
        print("3. Test restart_cobbleverse_server()")
        print("4. Re-run check_cobbleverse_server()")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            confirm = input("⚠️  This will attempt to START the server. Continue? (y/n): ")
            if confirm.lower() == 'y':
                print("\nStarting server...")
                returncode, stdout, stderr = await start_cobbleverse_server()
                print(f"Return code: {returncode}")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                
        elif choice == "2":
            confirm = input("⚠️  This will attempt to STOP the server. Continue? (y/n): ")
            if confirm.lower() == 'y':
                print("\nStopping server...")
                returncode, stdout, stderr = await stop_cobbleverse_server()
                print(f"Return code: {returncode}")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                
        elif choice == "3":
            confirm = input("⚠️  This will attempt to RESTART the server. Continue? (y/n): ")
            if confirm.lower() == 'y':
                print("\nRestarting server...")
                returncode, stdout, stderr = await restart_cobbleverse_server()
                print(f"Return code: {returncode}")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                
        elif choice == "4":
            await test_check_server()
            
        elif choice == "5":
            print("\nExiting tests...")
            break
            
        else:
            print("Invalid choice. Please try again.")

async def main():
    print("Cobbleverse Server Control Test Suite")
    print("====================================\n")
    
    # First test the check function
    await test_check_server()
    
    # Then offer interactive testing
    print("\nWould you like to test server control functions?")
    print("⚠️  WARNING: This will actually start/stop/restart the server\!")
    
    proceed = input("\nProceed with control tests? (y/n): ")
    if proceed.lower() == 'y':
        await test_server_controls()
    else:
        print("\nSkipping control tests. Test suite complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
EOF < /dev/null
