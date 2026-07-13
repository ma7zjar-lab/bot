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

from database.database import add_case


class Moderation(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    # ==============================
    # Permission Check
    # ==============================

    async def check_bot_permission(
        self,
        interaction,
        permission
    ):

        if not getattr(
            interaction.guild.me.guild_permissions,
            permission
        ):

            await interaction.response.send_message(
                embed=error(
                    "Missing Permission",
                    f"I need `{permission}` permission."
                ),
                ephemeral=True
            )

            return False

        return True


    # ==============================
    # BAN
    # ==============================

    @app_commands.command(
        name="ban",
        description="Ban a member"
    )
    @owner_only()
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):

        if not await self.check_bot_permission(
            interaction,
            "ban_members"
        ):
            return


        view = Confirm(interaction.user)


        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Confirm Ban",
                description=(
                    f"User: {member.mention}\n"
                    f"Reason: {reason}\n\n"
                    "Continue?"
                ),
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
                    "Ban cancelled."
                ),
                view=None
            )

            return


        try:

            await member.ban(
                reason=reason
            )


            case = await add_case(
                interaction.guild.id,
                member.id,
                interaction.user.id,
                "BAN",
                reason
            )


            await interaction.edit_original_response(
                embed=success(
                    "Member Banned",
                    (
                        f"User: {member.mention}\n"
                        f"Reason: {reason}\n"
                        f"Case: #{case}"
                    )
                ),
                view=None
            )


        except discord.Forbidden:

            await interaction.edit_original_response(
                embed=error(
                    "Failed",
                    "I cannot ban this member."
                ),
                view=None
            )


    # ==============================
    # KICK
    # ==============================

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


        if not await self.check_bot_permission(
            interaction,
            "kick_members"
        ):
            return


        view = Confirm(interaction.user)


        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Confirm Kick",
                description=(
                    f"User: {member.mention}\n"
                    f"Reason: {reason}"
                ),
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

            await member.kick(
                reason=reason
            )


            case = await add_case(
                interaction.guild.id,
                member.id,
                interaction.user.id,
                "KICK",
                reason
            )


            await interaction.edit_original_response(
                embed=success(
                    "Member Kicked",
                    (
                        f"User: {member.mention}\n"
                        f"Reason: {reason}\n"
                        f"Case: #{case}"
                    )
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


    # ==============================
    # TIMEOUT
    # ==============================

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


        if not await self.check_bot_permission(
            interaction,
            "moderate_members"
        ):
            return


        if minutes > 40320:

            await interaction.response.send_message(
                embed=error(
                    "Invalid Duration",
                    "Maximum timeout is 28 days."
                ),
                ephemeral=True
            )

            return


        view = Confirm(interaction.user)


        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Confirm Timeout",
                description=(
                    f"User: {member.mention}\n"
                    f"Duration: {minutes} minutes\n"
                    f"Reason: {reason}"
                ),
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


            case = await add_case(
                interaction.guild.id,
                member.id,
                interaction.user.id,
                "TIMEOUT",
                reason
            )


            await interaction.edit_original_response(
                embed=success(
                    "Member Timed Out",
                    (
                        f"User: {member.mention}\n"
                        f"Duration: {minutes} minutes\n"
                        f"Case: #{case}"
                    )
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


# ==============================
# Setup
# ==============================

async def setup(bot):

    await bot.add_cog(
        Moderation(bot)
    )
