import discord
from discord.ext import commands
import asyncio
import os
import logging

from config import TOKEN, PREFIX, SYNC_COMMANDS_ON_START
from database.database import init_database


# ==============================
# Logging Setup
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s"
)

logger = logging.getLogger("bot")


# ==============================
# Bot Intents
# ==============================

intents = discord.Intents.all()


# ==============================
# Custom Bot Class
# ==============================

class ModerationBot(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),
            intents=intents,
            help_command=None
        )


    async def setup_hook(self):

        logger.info("Running setup...")


        # Initialize database

        await init_database()

        logger.info("Database ready")


        # Load cogs

        await self.load_cogs()


        # Sync slash commands

        if SYNC_COMMANDS_ON_START:

            try:

                synced = await self.tree.sync()

                logger.info(
                    f"Synced {len(synced)} slash commands"
                )

            except Exception as e:

                logger.error(
                    f"Slash sync failed: {e}"
                )


    async def load_cogs(self):

        if not os.path.exists("cogs"):

            os.makedirs("cogs")


        for filename in os.listdir("./cogs"):


            if (
                filename.endswith(".py")
                and not filename.startswith("_")
            ):

                try:

                    await self.load_extension(
                        f"cogs.{filename[:-3]}"
                    )


                    logger.info(
                        f"Loaded cog: {filename}"
                    )


                except Exception as e:

                    logger.error(
                        f"Failed loading {filename}: {e}"
                    )


# ==============================
# Create Bot
# ==============================

bot = ModerationBot()


# ==============================
# Events
# ==============================

@bot.event
async def on_ready():

    logger.info(
        "=============================="
    )

    logger.info(
        f"Logged in as {bot.user}"
    )

    logger.info(
        f"Bot ID: {bot.user.id}"
    )

    logger.info(
        f"Servers: {len(bot.guilds)}"
    )

    logger.info(
        "=============================="
    )


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


    logger.error(
        f"Command error: {error}"
    )


    try:

        await ctx.send(
            f"❌ Error: `{error}`"
        )

    except:

        pass


@bot.event
async def on_app_command_error(
    interaction,
    error
):

    logger.error(
        f"Slash error: {error}"
    )


    try:

        if interaction.response.is_done():

            await interaction.followup.send(
                f"❌ Error: `{error}`",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                f"❌ Error: `{error}`",
                ephemeral=True
            )


    except:

        pass


# ==============================
# Run Bot
# ==============================

async def main():

    if not TOKEN:

        logger.error(
            "No Discord token found!"
        )

        return


    async with bot:

        await bot.start(TOKEN)



if __name__ == "__main__":

    asyncio.run(main())
