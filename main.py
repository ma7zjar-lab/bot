import os
import discord
from discord.ext import commands

from database.database import init_database

# ==============================
# Bot Configuration
# ==============================

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)


# ==============================
# Load Cogs
# ==============================

async def load_cogs():

    if not os.path.exists("cogs"):
        os.makedirs("cogs")

    for filename in os.listdir("./cogs"):

        if filename.endswith(".py") and not filename.startswith("_"):

            try:

                await bot.load_extension(
                    f"cogs.{filename[:-3]}"
                )

                print(
                    f"✅ Loaded {filename}"
                )

            except Exception as e:

                print(
                    f"❌ Failed loading {filename}"
                )

                print(e)


# ==============================
# Startup
# ==============================

@bot.event
async def setup_hook():

    await init_database()

    await load_cogs()


# ==============================
# Ready
# ==============================

@bot.event
async def on_ready():

    print("=" * 40)

    print(
        f"Logged in as {bot.user}"
    )

    print(
        f"ID: {bot.user.id}"
    )

    print(
        f"Servers: {len(bot.guilds)}"
    )

    print("=" * 40)


# ==============================
# Prefix Command Error Handler
# ==============================

@bot.event
async def on_command_error(
    ctx,
    error
):

    if isinstance(
        error,
        commands.CommandNotFound
    ):
        return


    elif isinstance(
        error,
        commands.MissingPermissions
    ):

        await ctx.send(
            "❌ You don't have permission to use that command."
        )


    elif isinstance(
        error,
        commands.BotMissingPermissions
    ):

        await ctx.send(
            "❌ I don't have the required permissions."
        )


    elif isinstance(
        error,
        commands.MissingRequiredArgument
    ):

        await ctx.send(
            "❌ Missing required arguments."
        )


    elif isinstance(
        error,
        commands.BadArgument
    ):

        await ctx.send(
            "❌ Invalid argument."
        )


    else:

        print(error)

        await ctx.send(
            "❌ An unexpected error occurred."
        )


# ==============================
# Startup Check
# ==============================

if TOKEN is None:

    raise RuntimeError(
        "DISCORD_TOKEN environment variable is missing."
    )


# ==============================
# Run Bot
# ==============================

bot.run(TOKEN)
