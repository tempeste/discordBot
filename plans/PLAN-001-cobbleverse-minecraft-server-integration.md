# PLAN-001: Cobbleverse Minecraft Server Integration

## Executive Summary
This plan outlines the implementation of Discord bot commands to monitor and control the Cobbleverse Minecraft server located at `/home/tempeste/Drive2_symlink/cobbleverse`. The implementation will follow the existing pattern established by the Palworld server integration.

## Objectives
- [ ] Implement server status monitoring commands
- [ ] Add server control commands (start, stop, restart)
- [ ] Create server information display with player count and resource usage
- [ ] Ensure proper error handling and user feedback
- [ ] Maintain consistency with existing bot architecture

## Architecture
Following the existing pattern:
- **Commands**: Slash commands in `main.py` following the Palworld server pattern
- **Utilities**: Server interaction functions in `utils.py`
- **Permissions**: Use `@is_owner()` decorator for administrative commands
- **Display**: Discord embeds for status information

## Implementation Phases

### Phase 1: Foundation
- Research Minecraft server control methods (RCON, screen sessions, systemd)
- Identify the server management script/method used for Cobbleverse
- Determine available server metrics and status information

### Phase 2: Core Commands
- Implement `check_cobbleverse()` utility function
- Create `/cobbleverse_status` command
- Add server control utilities (start, stop, restart)
- Implement control commands with owner restrictions

### Phase 3: Enhanced Features
- Add player list functionality
- Include world information if available
- Add server console command execution (owner only)
- Implement backup status checking

## Technical Approach

### Server Detection
- Check for running Java processes with Minecraft server
- Identify the specific server management method used
- Parse server properties and configuration files

### Status Information
- Server online/offline status
- Player count and list
- CPU and memory usage
- Server version and mod information
- World size and backup status

### Control Methods
- Use existing server management scripts if available
- Fallback to screen/tmux session management
- Implement proper timeout handling (120 seconds like Palworld)

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Unknown server setup | High | Investigate server directory structure first |
| Different management tool | Medium | Create flexible implementation supporting multiple methods |
| Permission issues | Medium | Ensure bot user has necessary permissions |
| Server response delays | Low | Implement async operations with timeouts |

## Success Metrics
- All commands respond within 5 seconds
- Server status accurately reflects actual state
- Control commands successfully manage server lifecycle
- Error messages are user-friendly and actionable
- Implementation follows existing code patterns

## Notes
- Server location: `/home/tempeste/Drive2_symlink/cobbleverse`
- Should maintain consistency with Palworld server commands
- Consider future refactoring into cogs structure
- Ensure all commands have proper error handling