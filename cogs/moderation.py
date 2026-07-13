import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

from utils import (
    owner_only,
    success,
    error,
    Confirm
)


class Moderation(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    # ==========================
    # BAN SLASH COMMAND
    # ==========================

    @app_commands.command(
        name="ban",
        description="Ban a member from the server"
    )
    @owner_only()
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):

        view = Confirm(interaction.user)

        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Confirm Ban",
                description=f"""
User: {member.mention}

Reason:
{reason}

Are you sure?
""",
                color=0xFEE75C
            ),
            view=view,
            ephemeral=True
        )


        await view.wait()


        if view.value is None:

            await interaction.edit_original_response(
                embed=error(
                    "Cancelled",
                    "Confirmation timed out."
                ),
                view=None
            )

            return


        if view.value is False:

            await interaction.edit_original_response(
                embed=error(
                    "Cancelled",
                    "Ban cancelled."
                ),
                view=None
            )

            return


        try:

            await member.ban(reason=reason)


            await interaction.edit_original_response(
                embed=success(
                    "Member Banned",
                    f"""
User: {member.mention}

Reason:
{reason}

Moderator:
{interaction.user.mention}
"""
                ),
                view=None
            )


        except discord.Forbidden:

            await interaction.edit_original_response(
                embed=error(
                    "Failed",
                    "I do not have permission to ban this member."
                ),
                view=None
            )


    # ==========================
    # KICK SLASH COMMAND
    # ==========================

    @app_commands.command(
        name="kick",
        description="Kick a member"
    )
    @owner_only()
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):


        view = Confirm(interaction.user)


        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Confirm Kick",
                description=f"""
User:
{member.mention}

Reason:
{reason}
""",
                color=0xFEE75C
            ),
            view=view,
            ephemeral=True
        )


        await view.wait()


        if view.value != True:

            await interaction.edit_original_response(
                embed=error(
                    "Cancelled",
                    "Kick cancelled."
                ),
                view=None
            )

            return


        try:

            await member.kick(reason=reason)


            await interaction.edit_original_response(
                embed=success(
                    "Member Kicked",
                    f"""
User:
{member.mention}

Reason:
{reason}
"""
                ),
                view=None
            )


        except discord.Forbidden:

            await interaction.edit_original_response(
                embed=error(
                    "Failed",
                    "I cannot kick this member."
                ),
                view=None
            )


    # ==========================
    # TIMEOUT
    # ==========================

    @app_commands.command(
        name="timeout",
        description="Timeout a member"
    )
    @owner_only()
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: str = "No reason provided"
    ):


        view = Confirm(interaction.user)


        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Confirm Timeout",
                description=f"""
User:
{member.mention}

Duration:
{minutes} minutes

Reason:
{reason}
""",
                color=0xFEE75C
            ),
            view=view,
            ephemeral=True
        )


        await view.wait()


        if view.value != True:

            await interaction.edit_original_response(
                embed=error(
                    "Cancelled",
                    "Timeout cancelled."
                ),
                view=None
            )

            return


        try:

            await member.timeout(
                timedelta(minutes=minutes),
                reason=reason
            )


            await interaction.edit_original_response(
                embed=success(
                    "Member Timed Out",
                    f"""
User:
{member.mention}

Duration:
{minutes} minutes

Reason:
{reason}
"""
                ),
                view=None
            )


        except discord.Forbidden:

            await interaction.edit_original_response(
                embed=error(
                    "Failed",
                    "I cannot timeout this member."
                ),
                view=None
            )


async def setup(bot):

    await bot.add_cog(
        Moderation(bot)
    )
