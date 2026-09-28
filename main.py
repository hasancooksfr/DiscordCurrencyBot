import os 
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from pymongo import MongoClient
from datetime import timedelta
import time
import random

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
    
@bot.command(name="transfer", aliases=['send'])
async def transfer(ctx, user: discord.Member = None, coins: int = None):
    if not user:
        embed=discord.Embed(
            title="Invalid command usage!",
            description="Please mention a user to whom you want to send coins.",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    if not coins:
        embed=discord.Embed(
            title="Invalid command usage!",
            description="Please mention amount of coins to transfer.",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    if user.id == ctx.author.id:
        return await ctx.reply("Nice try but you can't transfer to yourself.")

    acc = economy.find_one({"userid": ctx.author.id})
    if not acc:
        embed=discord.Embed(
            title="Account not found!",
            description="You don't have an active currency account.\nOpen one using `.open`",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    acc2 = economy.find_one({"userid": user.id})
    if not acc2:
        embed=discord.Embed(
            title="Account not found!",
            description=f"{user.mention} don't have an active currency account.",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    if coins > 0 and coins <= acc['balance']:
        economy.update_one(
            {
                "userid": ctx.author.id
            },
            {
                "$inc": {
                    "balance": -coins
                }
            }
        )

        economy.update_one(
            {
                "userid": user.id
            },
            {
                "$inc": {
                    "balance": coins
                }
            }
        )

        embed=discord.Embed(
            title="Transfer successful!",
            description=f"Paid to: {user.mention}\nAmount: {coins}\nTransfer Completed!",
            color=discord.Color.green()
        )
        await ctx.reply(embed=embed)

    else:
        embed=discord.Embed(
            title="Insufficient Balance or Wrong Entry!",
            description="Transfer couldn't be completed due to insufficient balance. Try a lower value.\nThis can mean that you have entered a wrong amount that can't be processed.",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)

@bot.command(name="daily")
async def daily(ctx):
    acc = economy.find_one({"userid": ctx.author.id})
    if not acc:
        embed=discord.Embed(
            title="Account not found!",
            description="You don't have an active currency account.\nUse `.open` to open one.",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    cd = countdown.find_one({"userid": ctx.author.id})
    if cd['daily'] > int(time.time()):
        embed=discord.Embed(
            title="Hold on!",
            description=f"You have already redeemed your daily.\nYour next daily reward comes <t:{cd['daily']}:R>",
            color=discord.Color.yellow()
        )
        return await ctx.reply(embed=embed)

    coins = random.randint(250,2500)
    economy.update_one(
        {
            "userid": ctx.author.id
        },
        {
            "$inc": {
                "balance": coins
            }
        }
    )
    countdown.update_one(
        {
            "userid": ctx.author.id
        },
        {
            "$set": {
                "daily": (int(time.time()) + 86400)
            }
        }
    )

    embed = discord.Embed(
        title="Daily claimed!",
        description=f"You have claimed {coins} coins as your daily reward! Claim one tomorrow again.",
        color=discord.Color.green()
    )
    await ctx.reply(embed=embed)

@bot.command(name="rob")
async def rob(ctx, user: discord.Member = None):
    if not user:
        embed= discord.Embed(
            title="Invalid command usage!",
            description="Please mention a @user!",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    acc = economy.find_one({"userid": ctx.author.id})
    if not acc:
        embed= discord.Embed(
            title="Account not found!",
            description="You don't have an active currency account!\nUse `.open` to open one.",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    acc2 = economy.find_one({"userid": user.id})
    if not acc2:
        embed = discord.Embed(
            title="Account not found!",
            description=f"{user.mention} doesn't have an active currency account.",
            color=discord.Color.red()
        )
        return await ctx.reply(embed=embed)

    cd = countdown.find_one({"userid": ctx.author.id})
    if cd['rob'] > int(time.time()):
        embed=discord.Embed(
            title="Calm Down!",
            description=f"You can't use this command right now. Check back later <t:{cd['rob']}:R>.",
            color=discord.Color.yellow()
        )
        return await ctx.reply(embed=embed)

    chance = random.randint(1,10)
    amount = random.randint(0, int(acc2['balance'] * 0.40))

    countdown.update_one(
        {
            "userid": ctx.author.id
        },
        {
            "$set": {
                "rob": (int(time.time()) + 86400)
            }
        }
    )

    if chance >= 5: #Success

        economy.update_one(
            {
                "userid": ctx.author.id
            },
            {
                "$inc": {
                    "balance": amount
                }
            }
        )

        economy.update_one(
            {
                "userid": user.id
            },
            {
                "$inc": {
                    "balance": -amount
                }
            }
        )

        try:
            embed=discord.Embed(
                title="You have been robbed!",
                description=f"You have been robbed by {ctx.author.mention} in {ctx.guild} for {amount} coins!",
                color=discord.Color.red()
            )
            await user.send(embed=embed)
        except:
            pass

        embed = discord.Embed(
            title="Robbery Successfully!",
            description=f"You robbed {user.mention} for {amount}!",
            color=discord.Color.gold()
        )
        await ctx.reply(embed=embed)
    
    else: #Failure
        amount = random.randint(0, (int(acc2['balance']) * 0.30))
        economy.update_one(
            {
                "userid": ctx.author.id
            },
            {
                "$inc": -amount
            }
        )

        embed = discord.Embed(
            title="CAUGHT!",
            description=f"You tried to rob {user.mention} but got caught!\nYou have been fined for {amount} coins.",
            color=discord.Color.red()
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

@bot.tree.command(name="transfer", description="Transfer coins to your friends!")
async def transfer_sl(interaction: discord.Interaction, user: discord.Member, coins: int):
    await interaction.response.defer()

    if user.id == interaction.user.id:
        return await interaction.followup.send("Nice try but you can't transfer to yourself.", ephemeral=True)

    acc = economy.find_one({"userid": interaction.user.id})
    if not acc:
        embed=discord.Embed(
            title="Account not found!",
            description="You don't have an active currency account.\nUse `/open` to open one.",
            color=discord.Color.red()
        )
        return await interaction.followup.send(embed=embed, ephemeral=True)

    acc2 = economy.find_one({"userid": user.id})
    if not acc2:
        embed=discord.Embed(
            title="Account not found!",
            description=f"{user.mention} doesn't have an active currency account.",
            color=discord.Color.red()
        )
        return await interaction.followup.send(embed=embed)

    if coins > 0 and acc['balance'] >= coins:
        economy.update_one(
            {
                "userid": interaction.user.id
            },
            {
                "$inc": {
                    "balance": -coins
                }
            }
        )

        economy.update_one(
            {
                "userid": user.id
            },
            {
                "$inc": {
                    "balance": coins
                }
            }
        )

        embed=discord.Embed(
            title="Transfer successful!",
            description=f"Paid to: {user.mention}\nAmount: {coins}\nTransfer completed!",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

    else:
        embed=discord.Embed(
            title="Insufficient Balance or Wrong Entry!",
            description="Transfer couldn't be completed due to insufficient balance. Try a lower value.\nThis can mean that you have entered a wrong amount that can't be processed.",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="daily", description="Claim your daily reward")
async def daily_sl(interaction: discord.Interaction):
    await interaction.response.defer()

    acc = economy.find_one({"userid": interaction.user.id})
    if not acc:
        embed=discord.Embed(
            title="Account not found!",
            description="You don't have an active currency account.\nUse `.open` to open one!",
            color=discord.Color.red()
        )
        return await interaction.followup.send(embed=embed, ephemeral=True)

    cd = countdown.find_one({"userid": interaction.user.id})
    if cd['daily'] > int(time.time()):
        embed=discord.Embed(
            title="Hold On!",
            description=f"You have already claimed your daily reward today!\nClaim next reward <t:{cd['daily']}:R>.",
            color=discord.Color.yellow()
        )
        return await interaction.followup.send(embed=embed, ephemeral=True)

    coins = random.randint(250,2500)

    economy.update_one(
        {
            "userid": interaction.user.id
        },
        {
            "$inc": {
                "balance": coins
            }
        }
    )
    countdown.update_one(
        {
            "userid": interaction.user.id
        },
        {
            "$set": {
                "daily": (int(time.time()) + 86400)
            }
        }
    )

    embed=discord.Embed(
        title="Daily Claimed!",
        description=f"You have claimed {coins} coins as your daily reward! Claim one tomorrow again.",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

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