# Python Discord Music Bot

## Project Overview

This project centers on developing a versatile and engaging music player bot for Discord, with a focus on both entertainment and utility functionalities. The primary objectives of the project include:

- **Enhancing Python Programming Skills**: By creating and refining the bot, the project serves as a platform for refreshing and advancing Python programming capabilities, particularly in the realm of bot development.
  
- **Learning and Implementing DevOps Tools**: A key aspect of the project is to gain hands-on experience with various DevOps tools. This includes deploying and managing tools like Prometheus for monitoring, using Docker for containerization, and integrating CI/CD pipelines for streamlined development and deployment processes.

- **Self-Hosting on a Mini PC**: The bot is hosted on a mini PC, providing a compact and personalized hosting solution. This approach allows for direct management of the hosting environment and offers practical experience in server administration.

- **Utility Features for Palworld Server**: Expanding its functionality, the bot now includes features aimed at simplifying the administration and troubleshooting of the Palworld server.

## Current Progress

- **Operational Basic Bot**: The bot is currently functional within a Discord server, demonstrating basic operational capabilities.

- **Voice Channel Interaction**: The bot has the ability to join and leave voice channels, providing an interactive experience for server members.

- **Palworld Server Administration Features**: The bot includes specialized commands for managing and monitoring the Palworld server:
    - `check_server`: Retrieves and displays the Palworld server's status, including the Internet IP and resource usage, formatted in an engaging Discord embed.
    - `restart_server`: Allows for restarting the Palworld server, ensuring that this critical administrative function is easily accessible. This command is restricted to the bot owner for security reasons.
    - `start_server`: Allows for non-bot owners to start the Palworld server as I intend to turn it off if not in use
    - `stop_server`: Stops the server. This command is restricted to only the bot owner.

## Task Checklist
- [x] Set up basic Discord bot infrastructure.
- [x] Enable bot to join and leave voice channels.
- [x] Integrate YouTube API for searching and playing videos.
- [x] Implement a command to search for YouTube videos and display results.
~~ [x] Implement a command that outputs the host machine's ip address.~~
- [x] Implement a command to query palworld server status and usage
- [x] Implement a command to restart, start, and stop palworld server
- [x] Add functionality to play audio from YouTube videos in voice channels.
- [ ] Develop a queue system for song playback.
- [ ] Create additional playback control commands (e.g., pause, stop, skip).
- [ ] Implement OAuth 2.0 for YouTube Playlist management (optional).
- [ ] Set up a Docker container for the bot.
- [ ] Configure CI/CD pipeline for automated deployment.
- [ ] Integrate Prometheus for monitoring and metrics.
- [x] Deploy the bot on a Beelink mini PC.
- [ ] Refactor each functionality into a cog
- [ ] Implement minecraft server management features

## Future Enhancements
- Enhance user interaction with more complex commands.
- Add more robust error handling and logging.
- Consider integrating other music streaming platforms.
- Explore advanced features like voice recognition or custom playlists.
- Enable the bot to modify palworld server params.