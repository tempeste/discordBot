# Python Discord Music Bot

## Project Overview

This project centers on developing a versatile and engaging music player bot for Discord, with a focus on both entertainment and utility functionalities. The primary objectives of the project include:

- **Enhancing Python Programming Skills**: By creating and refining the bot, the project serves as a platform for refreshing and advancing Python programming capabilities, particularly in the realm of bot development.
  
- **Learning and Implementing DevOps Tools**: A key aspect of the project is to gain hands-on experience with various DevOps tools. This includes deploying and managing tools like Prometheus for monitoring, using Docker for containerization, and integrating CI/CD pipelines for streamlined development and deployment processes.

- **Self-Hosting on a Mini PC**: The bot is hosted on a mini PC, providing a compact and personalized hosting solution. This approach allows for direct management of the hosting environment and offers practical experience in server administration.

- **Utility Features for Game Servers**: Expanding its functionality, the bot now includes features aimed at simplifying the administration and troubleshooting of game servers, particularly Minecraft (Cobbleverse).

## Current Progress

- **Operational Basic Bot**: The bot is currently functional within a Discord server, demonstrating basic operational capabilities.

- **Voice Channel Interaction**: The bot has the ability to join and leave voice channels, providing an interactive experience for server members.

- **Modular Cog Architecture**: The bot has been refactored into a modular cog-based system for better organization and maintainability.

- **Cobbleverse Server Administration Features**: The bot includes specialized commands for managing and monitoring the Cobbleverse Minecraft server:
    - `/check_cobbleverse`: Retrieves and displays the Cobbleverse server's status, including player count, version, and resource usage.
    - `/restart_cobbleverse`: Allows for restarting the Cobbleverse server. This command is restricted to the bot owner for security reasons.
    - `/start_cobbleverse`: Allows users to start the Cobbleverse server.
    - `/stop_cobbleverse`: Stops the server. This command is restricted to only the bot owner.

## Project Structure

```
.
├── main_cogs.py       # Main bot entry point with cog system
├── cogs/              # Modular functionality organized into cogs
│   ├── music.py       # Music playback functionality
│   └── cobbleverse.py # Cobbleverse server management
├── utils.py           # Utility functions
├── bot_tasks.py       # Background tasks (status updates)
├── requirements.txt   # Python dependencies
├── .env               # Environment variables (BOT_TOKEN, GCP_API_KEY, OWNER_ID)
└── README.md          # Project documentation
```

## Bot Commands

### Music Commands
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

### Cobbleverse Server Commands
- `/check_cobbleverse` - Display server status, player count, and resource usage
- `/restart_cobbleverse` - Restart Cobbleverse server (owner only)
- `/start_cobbleverse` - Start Cobbleverse server
- `/stop_cobbleverse` - Stop Cobbleverse server (owner only)

## Usage

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Google Cloud Platform API Key (for YouTube search)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/discordBot.git
cd discordBot
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your credentials:
```
BOT_TOKEN=your_discord_bot_token
GCP_API_KEY=your_google_cloud_api_key
OWNER_ID=your_discord_user_id
```

5. Run the bot:
```bash
python main_cogs.py
```

### Running in Background

To run the bot in the background using screen:
```bash
screen -S discordbot
source venv/bin/activate
python main_cogs.py
# Press Ctrl+A then D to detach
# To reattach: screen -r discordbot
```

## Task Checklist
- [x] Set up basic Discord bot infrastructure.
- [x] Enable bot to join and leave voice channels.
- [x] Integrate YouTube API for searching and playing videos.
- [x] Implement a command to search for YouTube videos and display results.
- [x] Add functionality to play audio from YouTube videos in voice channels.
- [x] Develop a queue system for song playback.
- [x] Create additional playback control commands (e.g., pause, stop, skip).
- [x] Deploy the bot on a Beelink mini PC.
- [x] Refactor each functionality into a cog
- [x] Implement Minecraft (Cobbleverse) server management features
- [x] Allow new songs to be added while one is being played
- [x] Fix crash when /play command receives invalid input
- [ ] Implement OAuth 2.0 for YouTube Playlist management (optional).
- [ ] Set up a Docker container for the bot.
- [ ] Configure CI/CD pipeline for automated deployment.
- [ ] Integrate Prometheus for monitoring and metrics.

## Future Enhancements
- Enhance user interaction with more complex commands.
- Add more robust error handling and logging.
- Consider integrating other music streaming platforms.
- Explore advanced features like voice recognition or custom playlists.
- Add support for managing multiple game servers.
- Implement user permission systems for server commands.
- Add persistent storage for user preferences and playlists.
