import discord

from discord.ext import commands

from config import (
    OWNER_IDS,
    SUCCESS_COLOR,
    ERROR_COLOR,
    WARNING_COLOR,
    INFO_COLOR,
    LOG_CHANNEL_ID
)


# ==============================
# Owner Only Check
# ==============================

def owner_only():

    async def predicate(interaction: discord.Interaction):

        if interaction.user.id in OWNER_IDS:
            return True

        raise app_commands.CheckFailure(
            "You are not allowed to use this command."
        )

    return app_commands.check(predicate)



# ==============================
# Embed Helpers
# ==============================

def success(
    title,
    description
):

    return discord.Embed(
        title=f"✅ {title}",
        description=description,
        color=SUCCESS_COLOR
    )



def error(
    title,
    description
):

    return discord.Embed(
        title=f"❌ {title}",
        description=description,
        color=ERROR_COLOR
    )



def warning(
    title,
    description
):

    return discord.Embed(
        title=f"⚠️ {title}",
        description=description,
        color=WARNING_COLOR
    )



def info(
    title,
    description
):

    return discord.Embed(
        title=f"ℹ️ {title}",
        description=description,
        color=INFO_COLOR
    )



# ==============================
# Confirmation Buttons
# ==============================

class Confirm(discord.ui.View):

    def __init__(
        self,
        author,
        timeout=60
    ):

        super().__init__(
            timeout=timeout
        )

        self.author = author
        self.value = None



    async def interaction_check(
        self,
        interaction
    ):

        if interaction.user.id != self.author.id:

            await interaction.response.send_message(
                "❌ You cannot use this confirmation.",
                ephemeral=True
            )

            return False


        return True



    @discord.ui.button(
        label="Confirm",
        style=discord.ButtonStyle.green
    )
    async def confirm(
        self,
        interaction,
        button
    ):

        self.value = True

        await interaction.response.defer()

        self.stop()



    @discord.ui.button(
        label="Cancel",
        style=discord.ButtonStyle.red
    )
    async def cancel(
        self,
        interaction,
        button
    ):

        self.value = False

        await interaction.response.defer()

        self.stop()



# ==============================
# Logging Helper
# ==============================

async def send_log(
    guild,
    title,
    description,
    color=INFO_COLOR
):

    if guild is None:
        return


    channel = guild.get_channel(
        LOG_CHANNEL_ID
    )


    if channel is None:
        return


    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )


    embed.set_footer(
        text="Moderation Bot Logs"
    )


    await channel.send(
        embed=embed
    )
