import os 
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from pymongo import MongoClient
from datetime import timedelta
import time

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client['Cluster0']
economy = db['economy']
countdown = db['countdown']

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all(), help_command=None)

# Prefix Commands

# BASIC COMMANDS
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

# ECONOMY COMMANDS

@bot.command(name="open")
async def open(ctx):
    acc = economy.find_one({
        "userid": ctx.author.id
    })
    if acc:
        embed=discord.Embed(
            title="Account already exists!",
            description="You already have an account in my database and cannot create another.",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    economy.insert_one({
        "userid": ctx.author.id,
        "balance": 1000,
        "job": 0,
        "createdat": int(time.time())
    })

    countdown.update_one({
        "userid": ctx.author.id,
    },
    {
        "$setOnInsert": {
            'rob': int(time.time()),
            'daily': int(time.time()),
            'heist': int(time.time()),
            'job': 0
        }
    }, upsert=True)

    embed = discord.Embed(
        title="Account Opened!",
        description="Account has successfully opened!\nWe have added `1000` coins to your bank account as welcome bonus.\nThank you for banking with us!",
        color=discord.Color.green()
    )
    await ctx.reply(embed=embed)

@bot.command(name="balance")
async def balance(ctx):
    acc = economy.find_one({
        "userid": ctx.author.id
    }, {"_id": 0})
    if not acc:
        embed=discord.Embed(
            title="You don't have an open currency account!",
            description="Use `.open` to open a currency account.",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)
    
    embed=discord.Embed(
        title=f"Available balance of {ctx.author}",
        description=f"You currently have `{acc['balance']}` in your currency account!",
        color=discord.Color.green()
    )
    await ctx.reply(embed=embed)
    

# Tree Commands (SLASH)

# BASIC COMMANDS
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

# ECONOMY COMMANDS

@bot.tree.command(name="open", description="Open a currency account")
async def open_sl(interaction: discord.Interaction):
    acc = economy.find_one({
        "userid": interaction.user.id
    })
    if acc:
        embed=discord.Embed(
            title="Account already exists!",
            description="You already have an account in my database and cannot create another.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    economy.insert_one({
        "userid": interaction.user.id,
        "balance": 1000,
        "job": 0,
        "createdat": int(time.time())
    })

    countdown.update_one(
        {
            "userid": interaction.user.id
        },
        {
            "$setOnInsert": {
                "rob": int(time.time()),
                "daily": int(time.time()),
                "heist": int(time.time()),
                "job": 0
            }
        },
        upsert=True
    )

    embed=discord.Embed(
        title="Account Opened!",
        description="Account has successfully opened!\nWe have added `1000` coins to your bank account as welcome bonus.\nThank you for banking with us!",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="balance", description="Get your available currency balance")
async def balance(interaction: discord.Interaction):
    acc = economy.find_one({"userid": interaction.user.id})
    if not acc:
        embed=discord.Embed(
            title="You don't have an open currency account!",
            description="Use `/open` to open a currency account.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    embed=discord.Embed(
        title=f"Available balance of {interaction.user}",
        description=f"You currently have `{acc['balance']}` in your currency account!",
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