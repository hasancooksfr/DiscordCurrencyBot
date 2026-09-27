import os 
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

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

@bot.command(name="botinfo", aliases=['bi'])
async def botinfo(ctx):
    embed = discord.Embed(
        title="Bot Info - Currency",
        description=f"Hello! My name is **Currency**.\nDeveloper: theysaykings (GitHub: hasancooksfr)\nI am open-sourced on GitHub.\nMy main function is to handle currency and bank commands, working as a discord economy bot.",
        color=discord.Color.green()
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

@bot.tree.command(name="botinfo", description="Get basic information about Currency")
async def botinfo_sl(interaction: discord.Interaction):
    embed=discord.Embed(
        title="Bot Info - Currency",
        description="Hello! My name is **Currency**.\nDeveloper: theysaykings (GitHub: hasancooksfr)\nI am open-sourced on GitHub.\nMy main function is to handle currency and bank commands, working as a discord economy bot.",
        color=discord.Color.green()
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