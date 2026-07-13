import discord
from datetime import datetime

from config import (
    SUCCESS_COLOR,
    ERROR_COLOR,
    WARNING_COLOR,
    INFO_COLOR,
    FOOTER_TEXT,
    OWNER_IDS
)


# ==============================
# EMBED SYSTEM
# ==============================

def create_embed(title, description, color):

    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )

    embed.set_footer(
        text=FOOTER_TEXT
    )

    return embed


def success(title, description):

    return create_embed(
        f"✅ {title}",
        description,
        SUCCESS_COLOR
    )


def error(title, description):

    return create_embed(
        f"❌ {title}",
        description,
        ERROR_COLOR
    )


def warning(title, description):

    return create_embed(
        f"⚠️ {title}",
        description,
        WARNING_COLOR
    )


def info(title, description):

    return create_embed(
        f"ℹ️ {title}",
        description,
        INFO_COLOR
    )


# ==============================
# ID LOCK SYSTEM
# ==============================

def owner_only():

    async def predicate(
        interaction: discord.Interaction
    ):

        if interaction.user.id not in OWNER_IDS:

            await interaction.response.send_message(
                embed=error(
                    "Access Denied",
                    "You are not authorized to use this command."
                ),
                ephemeral=True
            )

            return False

        return True

    return discord.app_commands.check(predicate)


# ==============================
# CONFIRMATION BUTTON SYSTEM
# ==============================

class Confirm(discord.ui.View):

    def __init__(self, author):

        super().__init__(timeout=60)

        self.author = author
        self.value = None


    async def interaction_check(
        self,
        interaction
    ):

        if interaction.user.id != self.author.id:

            await interaction.response.send_message(
                "You cannot use these buttons.",
                ephemeral=True
            )

            return False

        return True


    @discord.ui.button(
        label="Yes",
        style=discord.ButtonStyle.green,
        emoji="✅"
    )
    async def yes(
        self,
        interaction,
        button
    ):

        self.value = True

        await interaction.response.defer()

        self.stop()


    @discord.ui.button(
        label="No",
        style=discord.ButtonStyle.red,
        emoji="❌"
    )
    async def no(
        self,
        interaction,
        button
    ):

        self.value = False

        await interaction.response.defer()

        self.stop()
