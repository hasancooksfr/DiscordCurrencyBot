import os 
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all(), help_command=None)

# Prefix Commands
@bot.command(name="ping")
async def ping(ctx):
    await ctx.reply("Pong!")

@bot.command(name="hello")
async def hello(ctx):
    embed = discord.Embed(
        title=f"Hello, {ctx.author.name}!",
        description="My name is Currency and I handle banks and currency commands!\nIsn't it cool?",
        color=discord.Color.gold()
    )
    await ctx.reply(embed=embed)

# Tree Commands (SLASH)

@bot.tree.command(name="ping", description="Ping the bot")
async def ping_sl(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="hello", description="Ask the bot to say hello")
async def hello_sl(interaction: discord.Interaction):
    embed=discord.Embed(
        title=f"Hello, {interaction.user.name}!",
        description="My name is Currency and I handle banks and currency commands!\nIsn't it cool?",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

# Events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash commands')

    except Exception as e:
        print(e)
    

TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)