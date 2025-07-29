# Discord Command Timeout Fix Summary

## Issue
The `/check_cobbleverse` and `/check_server` commands were timing out with "Unknown interaction" errors because Discord slash commands have a 3-second response timeout.

## Root Cause
1. Both commands were using synchronous subprocess calls (`subprocess.run`) instead of async operations
2. Commands weren't deferring the response before executing potentially slow operations
3. This caused Discord to timeout while waiting for the initial response

## Solution Implemented

### 1. Fixed Discord Command Handlers (main.py)
- Added `await interaction.response.defer()` at the beginning of both commands
- Changed `interaction.response.send_message()` to `interaction.followup.send()` 
- Also fixed the `/skip` command which had a similar issue

### 2. Made Subprocess Calls Async (utils.py)
- Changed `subprocess.run()` to `asyncio.create_subprocess_shell()`
- Updated both `check_palworld_server()` and `check_cobbleverse_server()` functions
- Now properly awaits subprocess communication instead of blocking

## Commands Fixed
- `/check_server` - Palworld server status check
- `/check_cobbleverse` - Cobbleverse server status check  
- `/skip` - Skip current song (when calling play_next)

## Technical Details
Before:
```python
result = subprocess.run(command, shell=True, capture_output=True, text=True)
```

After:
```python
process = await asyncio.create_subprocess_shell(
    command,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
)
stdout, stderr = await process.communicate()
```

This ensures the bot remains responsive and doesn't block the event loop while executing server commands.