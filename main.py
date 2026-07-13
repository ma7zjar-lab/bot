import discord
from discord.ext import commands
import asyncio
import os

from config import TOKEN, PREFIX


# ==============================
# Bot Setup
# ==============================

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(PREFIX),
    intents=intents
)

# ==============================
# Startup Event
# ==============================

@bot.event
async def on_ready():
    print("==============================")
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("==============================")


    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Slash sync error: {e}")


# ==============================
# Load Cogs
# ==============================

async def load_cogs():

    if not os.path.exists("cogs"):
        os.makedirs("cogs")

    for filename in os.listdir("./cogs"):

        if filename.endswith(".py"):

            try:
                await bot.load_extension(
                    f"cogs.{filename[:-3]}"
                )

                print(
                    f"Loaded cog: {filename}"
                )

            except Exception as e:
                print(
                    f"Failed loading {filename}: {e}"
                )


# ==============================
# Start Bot
# ==============================

async def main():

    await load_cogs()

    await bot.start(TOKEN)


asyncio.run(main())
