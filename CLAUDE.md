# Claude Code Project Instructions

## Project Overview

This is a versatile Discord bot that provides music playback functionality and game server management capabilities. The bot is designed to enhance Discord server experiences with entertainment features while also providing administrative tools for managing game servers.

## Key Objectives

- **Music Playback**: Provide YouTube music playback with queue management, playback controls, and search functionality
- **Cobbleverse Server Management**: Monitor and control a Minecraft Cobbleverse server with status checks, resource monitoring, and administrative controls
- **Self-Hosted Infrastructure**: Deploy and manage the bot on a Beelink mini PC with proper monitoring and reliability

## Project Structure

```
.
├── CLAUDE.md          # This file - project instructions for Claude
├── .claude/           # Claude Code configuration (auto-generated)
│   └── agents/        # Project-specific agent overrides
├── agents/            # Custom agents for specialized tasks
├── cogs/              # Bot functionality organized into cogs
│   ├── music.py       # Music playback commands and functionality
│   └── cobbleverse.py # Cobbleverse server management
├── docs/              # Project documentation
├── plans/             # Project plans and architectural documents
├── tickets/           # Task tickets and issues
├── main.py            # Legacy monolithic bot entry point
├── main_cogs.py       # Modern cog-based bot entry point
├── bot_tasks.py       # Background tasks (status updates)
├── utils.py           # Utility functions for server management and music
├── requirements.txt   # Python dependencies
├── .env               # Environment variables (BOT_TOKEN, GCP_API_KEY, OWNER_ID)
└── README.md          # Project documentation
```

## Development Guidelines

### Code Style

- Use Python 3.x with async/await patterns for Discord.py
- Follow PEP 8 conventions
- Use type hints where appropriate
- Keep functions focused and modular
- Never add comments to code - write self-documenting code

### Bot Architecture

- **Cog-Based Design**: Bot functionality is organized into Discord.py cogs for modularity and maintainability
- **Slash Commands**: All user interactions use Discord slash commands (via `@commands.Cog.slash_command`)
- **Owner-Only Commands**: Use the `@is_owner()` decorator for sensitive commands
- **Error Handling**: Implement proper error handling with user-friendly messages
- **Async Operations**: Use async/await for all Discord operations and subprocess calls

### Testing

- Test bot commands in a development Discord server
- Verify server management commands work correctly
- Test music playback with various YouTube URLs
- Check error handling for edge cases

### Git Workflow

- Create descriptive commit messages
- Keep commits focused and atomic
- Review changes before committing
- Update ticket status when completing features

## Common Commands

```bash
# Create virtual environment (first time setup)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the bot (modern cog-based version)
python main_cogs.py

# Run the bot in background using screen
screen -S discordbot
source venv/bin/activate
python main_cogs.py
# Press Ctrl+A then D to detach from screen
# To reattach: screen -r discordbot

# Check Cobbleverse server status (on host)
cd /home/tempeste/Drive2_symlink/cobbleverse && ./cobbleverse status

# Environment setup (create .env file with):
# BOT_TOKEN=your_discord_bot_token
# GCP_API_KEY=your_google_cloud_api_key
# OWNER_ID=your_discord_user_id
```

## Important Context

### Current Features

1. **Music Commands**:
   - `/join` - Join user's voice channel
   - `/leave` - Leave voice channel
   - `/play <query>` - Search and play YouTube music
   - `/search <query>` - Search YouTube and display results
   - `/pause` - Pause playback
   - `/resume` - Resume playback
   - `/stop` - Stop playback and clear queue
   - `/skip` - Skip current song
   - `/queue` - Display current queue
   - `/shuffle` - Shuffle the queue
   - `/loop` - Toggle loop mode

2. **Cobbleverse Server Commands**:
   - `/cobbleverse status` - Display server status and player count
   - `/cobbleverse start` - Start Cobbleverse server (owner only)
   - `/cobbleverse stop` - Stop Cobbleverse server (owner only)
   - `/cobbleverse restart` - Restart Cobbleverse server (owner only)

3. **Developer Commands** (available in main_cogs.py):
   - `/reload <cog>` - Reload a specific cog without restarting bot (owner only)
   - `/load <cog>` - Load a new cog (owner only)
   - `/unload <cog>` - Unload a cog (owner only)
   - `/list_cogs` - List all available cogs and their status

### Server Locations

- **Bot Location**: `/home/tempeste/dev/discordBot`
- **Cobbleverse Server**: `/home/tempeste/Drive2_symlink/cobbleverse`

### Dependencies

- **discord.py**: Modern Discord API wrapper with slash command support
- **yt-dlp**: YouTube video/audio downloader (replaces youtube-dl)
- **google-api-python-client**: For YouTube Data API v3
- **python-dotenv**: Environment variable management
- **PyNaCl**: Voice support for Discord

### Background Tasks

- Bot status updates every 10 minutes showing Cobbleverse server status and player count

### Upcoming Features

- Docker containerization
- Prometheus monitoring integration
- CI/CD pipeline setup

### Completed Features

- ✅ Cobbleverse (Minecraft) server management commands
- ✅ Refactor functionality into cogs for better organization

## Agents

See @agents/README.md for available agents and their purposes

## Agent Orchestration

The project uses specialized agents for different aspects of development:

### Recommended Workflows

1. **Adding Cobbleverse Server Features**:
   - Use **planner** to design the implementation approach
   - Use **coder** to implement the server management commands
   - Use **checker** to verify the implementation

2. **Bug Fixes**:
   - Use **researcher** to understand the issue
   - Use **debugger** to identify root cause
   - Use **coder** to implement fixes
   - Use **checker** to verify fixes

3. **Adding New Cogs**:
   - Use **planner** to design cog structure
   - Use **python-pro** for idiomatic Python patterns
   - Use **coder** to implement the new cog
   - Use **test-automator** to ensure functionality

## Tickets

See @tickets/README.md for ticket format and management approach

### Ticket Management
- **Ticket List**: Maintain @tickets/ticket-list.md as a centralized index of all tickets
- **Update ticket-list.md** whenever you:
  - Create a new ticket (add to appropriate priority section)
  - Change ticket status (update emoji and move if completed)
  - Complete a ticket (move to completed section with date)
- **Status Emojis**: 🔴 Todo | 🟡 In Progress | 🟢 Done | 🔵 Blocked | ⚫ Cancelled

## Plans

See @plans/README.md for planning documents and architectural decisions

## Development Context

- See @docs/ROADMAP.md for current status and next steps
- Task-based development workflow with tickets in `/tickets` directory
- Use `/plans` directory for architectural decisions and implementation roadmaps

## Important Instructions

Before starting any task:

1. **Confirm understanding**: Always confirm you understand the request and outline your plan before proceeding
2. **Ask clarifying questions**: Never make assumptions - ask questions when requirements are unclear
3. **Create planning documents**: Before implementing any code or features, create a markdown file documenting the approach
4. **Use plans directory**: When discussing ideas or next steps, create timestamped files in the plans directory (e.g., `plans/next-steps-YYYY-MM-DD-HH-MM-SS.md`) to maintain a record of decisions
5. **No code comments**: Never add comments to any code you write - code should be self-documenting
6. **Maintain ticket list**: Always update @tickets/ticket-list.md when creating, updating, or completing tickets to maintain a clear project overview

## Additional Notes

### Architecture Considerations

1. **Modular Design**: The bot uses a cog-based architecture with features organized into separate modules (Music, Cobbleverse). Each cog is self-contained and can be loaded/unloaded independently

2. **Error Handling**: Always provide user-friendly error messages in Discord embeds rather than raw error output

3. **Permissions**: Server management commands should have appropriate permission checks to prevent unauthorized use

4. **Resource Management**: Be mindful of subprocess calls for server management - use async operations to prevent blocking

5. **Voice Connections**: Properly handle voice channel disconnections and clean up resources

### Development Tips

- Use Discord Developer Portal to manage bot permissions and OAuth2 scopes
- Test with different YouTube URL formats (videos, playlists, searches)
- Monitor bot performance on the Beelink mini PC to ensure resource efficiency
- Keep sensitive commands (server stop/restart) owner-only for security
- When adding new functionality, create a new cog in the `/cogs` directory
- Use the bot's developer commands to reload cogs during development without restarting

### Future Considerations

- Implement proper logging system for debugging
- Add database for persistent settings and user preferences
- Consider rate limiting for resource-intensive commands
- Plan for scalability if bot is used in multiple Discord servers
