import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime
from discord import app_commands
from discord.ui import View, Button

# Load environment variables
load_dotenv()

# Bot configuration
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# Data storage
users_data = {}
server_config = {}
custom_commands = {}
reaction_roles = {}

# Load data from file
def load_data():
    global users_data, server_config, custom_commands, reaction_roles
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            users_data = data.get('users', {})
            server_config = data.get('servers', {})
            custom_commands = data.get('custom_commands', {})
            reaction_roles = data.get('reaction_roles', {})
    except FileNotFoundError:
        save_data()

# Save data to file
def save_data():
    data = {
        'users': users_data,
        'servers': server_config,
        'custom_commands': custom_commands,
        'reaction_roles': reaction_roles
    }
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Leveling system
def calculate_xp_for_level(level):
    return 5 * (level ** 2) + 50 * level + 100

def get_level(xp):
    level = 0
    while calculate_xp_for_level(level) <= xp:
        level += 1
    return level

# Events
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    load_data()
    await bot.change_presence(activity=discord.Game(name="!help"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_member_join(member):
    # Welcome message
    welcome_channel = discord.utils.get(member.guild.channels, name="welcome")
    if welcome_channel:
        embed = discord.Embed(
            title=f"Welcome to {member.guild.name}!",
            description=f"Hello {member.mention}! We're glad to have you here!",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Member Count", value=f"You are our {len(member.guild.members)}th member!")
        embed.set_footer(text=f"Joined at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await welcome_channel.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Process commands
    await bot.process_commands(message)
    
    # XP system
    if message.guild:
        user_id = str(message.author.id)
        # Ensure user data has XP and level keys
        if user_id not in users_data:
            users_data[user_id] = {'xp': 0, 'level': 1}
        else:
            if 'xp' not in users_data[user_id]:
                users_data[user_id]['xp'] = 0
            if 'level' not in users_data[user_id]:
                users_data[user_id]['level'] = 1
        
        users_data[user_id]['xp'] += random.randint(1, 3)
        current_level = users_data[user_id]['level']
        new_level = get_level(users_data[user_id]['xp'])
        
        if new_level > current_level:
            users_data[user_id]['level'] = new_level
            embed = discord.Embed(
                title="Level Up! 🎉",
                description=f"Congratulations {message.author.mention}!",
                color=discord.Color.gold()
            )
            embed.add_field(name="New Level", value=str(new_level))
            embed.add_field(name="XP", value=f"{users_data[user_id]['xp']} XP")
            await message.channel.send(embed=embed)
            save_data()

# Commands
@bot.command(name='rank')
async def rank(ctx, member: discord.Member = None):
    member = member or ctx.author
    user_id = str(member.id)
    
    if user_id not in users_data:
        await ctx.send(f"{member.mention} hasn't earned any XP yet!")
        return
    
    data = users_data[user_id]
    level = data['level']
    xp = data['xp']
    next_level_xp = calculate_xp_for_level(level)
    
    embed = discord.Embed(
        title=f"{member.name}'s Rank",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="Level", value=str(level))
    embed.add_field(name="XP", value=f"{xp}/{next_level_xp}")
    embed.add_field(name="Progress", value=f"{int((xp/next_level_xp)*100)}% to next level")
    await ctx.send(embed=embed)

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    sorted_users = sorted(
        users_data.items(),
        key=lambda x: x[1]['xp'],
        reverse=True
    )[:10]
    
    embed = discord.Embed(
        title="Server Leaderboard",
        color=discord.Color.gold()
    )
    
    for i, (user_id, data) in enumerate(sorted_users, 1):
        member = ctx.guild.get_member(int(user_id))
        if member:
            embed.add_field(
                name=f"{i}. {member.name}",
                value=f"Level {data['level']} - {data['xp']} XP",
                inline=False
            )
    
    await ctx.send(embed=embed)

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title="Member Kicked",
        color=discord.Color.red()
    )
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Reason", value=reason or "No reason provided")
    embed.add_field(name="Moderator", value=ctx.author.mention)
    
    await member.kick(reason=reason)
    await ctx.send(embed=embed)

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    embed = discord.Embed(
        title="Member Banned",
        color=discord.Color.red()
    )
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Reason", value=reason or "No reason provided")
    embed.add_field(name="Moderator", value=ctx.author.mention)
    
    await member.ban(reason=reason)
    await ctx.send(embed=embed)

@bot.command(name='mute')
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: int, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)
    
    embed = discord.Embed(
        title="Member Muted",
        color=discord.Color.orange()
    )
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Duration", value=f"{duration} minutes")
    embed.add_field(name="Reason", value=reason or "No reason provided")
    embed.add_field(name="Moderator", value=ctx.author.mention)
    
    await member.add_roles(muted_role)
    await ctx.send(embed=embed)
    
    await asyncio.sleep(duration * 60)
    await member.remove_roles(muted_role)
    
    unmute_embed = discord.Embed(
        title="Member Unmuted",
        color=discord.Color.green()
    )
    unmute_embed.add_field(name="User", value=member.mention)
    await ctx.send(embed=unmute_embed)

@bot.command(name='warn')
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    user_id = str(member.id)
    if user_id not in users_data:
        users_data[user_id] = {'warnings': []}
    
    users_data[user_id]['warnings'].append({
        'reason': reason,
        'moderator': ctx.author.id,
        'timestamp': datetime.datetime.now().isoformat()
    })
    
    embed = discord.Embed(
        title="Warning Issued",
        color=discord.Color.orange()
    )
    embed.add_field(name="User", value=member.mention)
    embed.add_field(name="Reason", value=reason or "No reason provided")
    embed.add_field(name="Moderator", value=ctx.author.mention)
    embed.add_field(name="Total Warnings", value=str(len(users_data[user_id]['warnings'])))
    
    await ctx.send(embed=embed)
    save_data()

@bot.command(name='warnings')
async def warnings(ctx, member: discord.Member = None):
    member = member or ctx.author
    user_id = str(member.id)
    
    if user_id not in users_data or not users_data[user_id].get('warnings'):
        await ctx.send(f"{member.mention} has no warnings!")
        return
    
    embed = discord.Embed(
        title=f"{member.name}'s Warnings",
        color=discord.Color.orange()
    )
    
    for i, warning in enumerate(users_data[user_id]['warnings'], 1):
        moderator = ctx.guild.get_member(warning['moderator'])
        embed.add_field(
            name=f"Warning #{i}",
            value=f"Reason: {warning['reason']}\nModerator: {moderator.mention if moderator else 'Unknown'}\nTime: {warning['timestamp']}",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='addcommand')
@commands.has_permissions(manage_messages=True)
async def add_command(ctx, command_name: str, *, response: str):
    custom_commands[command_name.lower()] = response
    save_data()
    
    embed = discord.Embed(
        title="Custom Command Added",
        color=discord.Color.green()
    )
    embed.add_field(name="Command", value=f"!{command_name}")
    embed.add_field(name="Response", value=response)
    await ctx.send(embed=embed)

@bot.command(name='delcommand')
@commands.has_permissions(manage_messages=True)
async def del_command(ctx, command_name: str):
    if command_name.lower() in custom_commands:
        del custom_commands[command_name.lower()]
        save_data()
        await ctx.send(f"Command !{command_name} has been deleted!")
    else:
        await ctx.send(f"Command !{command_name} doesn't exist!")

@bot.command(name='reactionrole')
@commands.has_permissions(manage_roles=True)
async def reaction_role(ctx, role: discord.Role, emoji: str, *, message_id: int = None):
    if message_id:
        message = await ctx.channel.fetch_message(message_id)
    else:
        message = await ctx.send("React to this message to get the role!")
    
    await message.add_reaction(emoji)
    reaction_roles[str(message.id)] = {
        'role_id': role.id,
        'emoji': emoji
    }
    save_data()
    
    embed = discord.Embed(
        title="Reaction Role Added",
        color=discord.Color.blue()
    )
    embed.add_field(name="Role", value=role.mention)
    embed.add_field(name="Emoji", value=emoji)
    await ctx.send(embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    if str(payload.message_id) in reaction_roles:
        role_data = reaction_roles[str(payload.message_id)]
        if str(payload.emoji) == role_data['emoji']:
            guild = bot.get_guild(payload.guild_id)
            role = guild.get_role(role_data['role_id'])
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    if str(payload.message_id) in reaction_roles:
        role_data = reaction_roles[str(payload.message_id)]
        if str(payload.emoji) == role_data['emoji']:
            guild = bot.get_guild(payload.guild_id)
            role = guild.get_role(role_data['role_id'])
            member = guild.get_member(payload.user_id)
            if role and member:
                await member.remove_roles(role)

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="Mee6 Pro Help Menu",
        description="Here are the available commands and features:",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url=ctx.guild.me.avatar.url if ctx.guild.me.avatar else discord.Embed.Empty)
    embed.add_field(name="Leveling & XP", value="`!rank`, `!leaderboard`", inline=False)
    embed.add_field(name="Moderation", value="`!kick`, `!ban`, `!mute`, `!warn`, `!warnings`", inline=False)
    embed.add_field(name="Custom Commands", value="`!addcommand`, `!delcommand`", inline=False)
    embed.add_field(name="Reaction Roles", value="`!reactionrole`", inline=False)
    embed.add_field(name="Other", value="`!help` (this menu)", inline=False)
    embed.set_footer(text="Mee6 Pro • Made with ❤️ by your team")

    class HelpView(View):
        def __init__(self):
            super().__init__(timeout=None)
            self.add_item(Button(label="Invite Bot", url="https://discord.com/oauth2/authorize?client_id=BOT_ID&scope=bot&permissions=8", style=discord.ButtonStyle.link))
            self.add_item(Button(label="Support Server", url="https://discord.gg/", style=discord.ButtonStyle.link))
            self.add_item(Button(label="Website", url="https://mee6.xyz", style=discord.ButtonStyle.link))

    await ctx.send(embed=embed, view=HelpView())

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN')) 