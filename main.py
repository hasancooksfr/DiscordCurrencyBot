import os 
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all(), help_command=None)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.reply("Pong!")

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