# Mee6 Pro (Free & Open Source)

[![Discord](https://img.shields.io/discord/your_server_id?color=7289DA&label=Discord&logo=discord&logoColor=white)](https://discord.gg/support)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Stars](https://img.shields.io/github/stars/yourusername/mee6-pro?style=social)](https://github.com/superangelguy/Mee6-Pro)

A powerful, free, and open-source Discord bot inspired by MEE6, featuring leveling, moderation, custom commands, reaction roles, and more—all with beautiful embeds and interactive buttons.

## 📋 Description

Mee6 Pro is a feature-rich Discord bot designed to enhance your server's functionality without the premium price tag. It combines the best features of popular bots like MEE6 into a single, easy-to-use package that's completely free and open source.

### ✨ Why Choose Mee6 Pro?

- **Free Forever**: No hidden costs or premium features - everything is available to everyone
- **Modern Design**: Beautiful embeds and interactive buttons for a professional look
- **Easy Setup**: Simple installation process with clear documentation
- **Customizable**: Add your own commands and tailor the bot to your server's needs
- **Active Development**: Regular updates and improvements
- **Community Support**: Join our support server for help and suggestions

### 🎯 Key Benefits

- **Engagement**: Keep your community active with the leveling system
- **Moderation**: Keep your server safe with powerful moderation tools
- **Customization**: Create custom commands for your server's unique needs
- **Role Management**: Easy role assignment through reaction roles
- **Welcome System**: Make new members feel at home with custom welcome messages

## 🚀 Features

- **Leveling System**: XP, levels, rank cards, and leaderboard
- **Moderation**: Kick, ban, mute, warn, and view warnings
- **Custom Commands**: Add and delete your own commands
- **Reaction Roles**: Assign roles via emoji reactions
- **Welcome Messages**: Greet new members with a stylish embed
- **Professional Help Menu**: Modern embed with interactive buttons

## 🛠️ Setup

1. **Clone or Download** this repository to your computer.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Create a Discord Bot**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application and add a bot
   - Copy your bot's token and Application ID (Client ID)
4. **Configure your environment**:
   - Create a file named `.env` in the project folder:
     ```env
     DISCORD_TOKEN=your_token_here
     ```
   - Replace `your_token_here` with your actual bot token
5. **Update the Invite Link**:
   - In `bot.py`, replace `client_id=YOUR_CLIENT_ID` in the help command's Invite Bot button with your actual Client ID
6. **Run the bot**:
   ```bash
   python bot.py
   ```

## 📝 Usage

- **Leveling**: Earn XP by chatting. Use `!rank` to see your level, `!leaderboard` for the top users.
- **Moderation**: Use `!kick`, `!ban`, `!mute`, `!warn`, and `!warnings` for server management.
- **Custom Commands**: Add with `!addcommand <name> <response>`, remove with `!delcommand <name>`.
- **Reaction Roles**: Use `!reactionrole @RoleName 😃` to set up a reaction role.
- **Welcome Messages**: Create a channel named `welcome` for automatic greetings.
- **Help Menu**: Type `!help` for a modern, interactive help menu.

## 🔒 Permissions
Make sure your bot has the following permissions:
- Manage Roles
- Kick Members
- Ban Members
- Manage Messages
- Add Reactions
- Read Messages

## 👥 Credits
- Inspired by [MEE6](https://mee6.xyz)
- Developed by superangelguy

## 💖 Support the Project

If you find this bot useful and would like to support its development, consider making a donation:

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Donate-ff5e5b?logo=kofi&logoColor=white)](https://ko-fi.com/superangelguy)

Your support helps maintain and improve the bot, ensuring it remains free and accessible to everyone!


---

**Enjoy your free, powerful Discord bot!** 

<div align="center">
  <sub>Built with ❤️ by superangelguy</sub>
</div> 
