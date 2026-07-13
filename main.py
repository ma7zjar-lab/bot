import discord
from discord.ext import commands
from discord import app_commands

import os


from database.database import init_database


# ==============================
# Config
# ==============================

TOKEN = os.getenv(
    "DISCORD_TOKEN"
)


PREFIX = "!"


# ==============================
# Intents
# ==============================

intents = discord.Intents.all()



# ==============================
# Bot Setup
# ==============================

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(PREFIX),
    intents=intents
)



# ==============================
# Load Cogs
# ==============================

async def load_cogs():

    if not os.path.exists(
        "cogs"
    ):

        os.makedirs(
            "cogs"
        )


    for filename in os.listdir(
        "./cogs"
    ):


        if (
            filename.endswith(".py")
            and not filename.startswith("_")
        ):

            try:

                await bot.load_extension(
                    f"cogs.{filename[:-3]}"
                )


                print(
                    f"✅ Loaded cog: {filename}"
                )


            except Exception as e:

                print(
                    f"❌ Failed loading {filename}: {e}"
                )



# ==============================
# Startup
# ==============================

@bot.event
async def setup_hook():

    await init_database()

    await load_cogs()


    try:

        synced = await bot.tree.sync()

        print(
            f"✅ Synced {len(synced)} slash commands"
        )


    except Exception as e:

        print(
            f"❌ Slash sync failed: {e}"
        )



# ==============================
# Ready Event
# ==============================

@bot.event
async def on_ready():

    print(
        "================================"
    )

    print(
        f"🤖 Logged in as {bot.user}"
    )

    print(
        f"🆔 Bot ID: {bot.user.id}"
    )

    print(
        "================================"
    )



# ==============================
# Global Error Handler
# ==============================

@bot.tree.error
async def on_app_command_error(
    interaction,
    error
):

    if isinstance(
        error,
        app_commands.MissingPermissions
    ):

        message = (
            "You do not have permission "
            "to use this command."
        )


    elif isinstance(
        error,
        app_commands.CommandOnCooldown
    ):

        message = (
            "Command is on cooldown."
        )


    else:

        print(
            error
        )

        message = (
            "An unexpected error occurred."
        )


    if interaction.response.is_done():

        await interaction.followup.send(
            message,
            ephemeral=True
        )

    else:

        await interaction.response.send_message(
            message,
            ephemeral=True
        )



# ==============================
# Start Bot
# ==============================

if TOKEN is None:

    raise Exception(
        "DISCORD_TOKEN is missing!"
    )


bot.run(
    TOKEN
)
