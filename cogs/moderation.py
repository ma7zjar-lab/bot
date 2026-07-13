import discord
from discord.ext import commands
from discord import app_commands

from datetime import timedelta

from config import OWNER_IDS, DM_PUNISHMENTS

from utils import (
    success,
    error,
    Confirm,
    send_log
)

from database.database import (
    add_case,
    add_warning,
    get_warnings
)


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    # ==============================
    # Permission / Safety Checks
    # ==============================

    async def owner_check(
        self,
        interaction
    ):

        if interaction.user.id not in OWNER_IDS:

            await interaction.response.send_message(
                embed=error(
                    "Access Denied",
                    "You are not allowed to use this command."
                ),
                ephemeral=True
            )

            return False

        return True


    async def can_punish(
        self,
        interaction,
        member
    ):

        if member.id == interaction.user.id:

            await interaction.response.send_message(
                embed=error(
                    "Failed",
                    "You cannot punish yourself."
                ),
                ephemeral=True
            )

            return False


        if member.top_role >= interaction.guild.me.top_role:

            await interaction.response.send_message(
                embed=error(
                    "Failed",
                    "I cannot punish this member because their role is higher than mine."
                ),
                ephemeral=True
            )

            return False


        return True


    async def send_dm(
        self,
        member,
        title,
        reason
    ):

        if not DM_PUNISHMENTS:
            return

        try:

            embed = discord.Embed(
                title=title,
                description=f"Reason: {reason}",
                color=0x5865F2
            )

            await member.send(
                embed=embed
            )

        except:

            pass



    # ==============================
    # BAN
    # ==============================

    @app_commands.command(
        name="ban",
        description="Ban a member"
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):

        if not await self.owner_check(interaction):
            return


        if not await self.can_punish(interaction, member):
            return


        view = Confirm(interaction.user)


        await interaction.response.send_message(
            embed=discord.Embed(
                title="⚠️ Confirm Ban",
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


        if view.value is not True:

            await interaction.edit_original_response(
                embed=error(
                    "Cancelled",
                    "Ban cancelled."
                ),
                view=None
            )

            return


        try:

            await self.send_dm(
                member,
                "🔨 You were banned",
                reason
            )


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


            await send_log(
                interaction.guild,
                "🔨 Member Banned",
                (
                    f"User: {member.mention}\n"
                    f"Moderator: {interaction.user.mention}\n"
                    f"Reason: {reason}\n"
                    f"Case: #{case}"
                ),
                0xED4245
            )


            await interaction.edit_original_response(
                embed=success(
                    "Ban Successful",
                    (
                        f"User: {member}\n"
                        f"Case: #{case}"
                    )
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



    # ==============================
    # KICK
    # ==============================

    @app_commands.command(
        name="kick",
        description="Kick a member"
    )
    async def kick(
        self,
        interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):

        if not await self.owner_check(interaction):
            return


        if not await self.can_punish(interaction, member):
            return


        try:

            await self.send_dm(
                member,
                "👢 You were kicked",
                reason
            )


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


            await send_log(
                interaction.guild,
                "👢 Member Kicked",
                (
                    f"User: {member.mention}\n"
                    f"Moderator: {interaction.user.mention}\n"
                    f"Reason: {reason}\n"
                    f"Case: #{case}"
                )
            )


            await interaction.response.send_message(
                embed=success(
                    "Kick Successful",
                    f"Case: #{case}"
                )
            )


        except discord.Forbidden:

            await interaction.response.send_message(
                embed=error(
                    "Failed",
                    "Missing permissions."
                ),
                ephemeral=True
            )



    # ==============================
    # TIMEOUT
    # ==============================

    @app_commands.command(
        name="timeout",
        description="Timeout a member"
    )
    async def timeout(
        self,
        interaction,
        member: discord.Member,
        minutes: int,
        reason: str = "No reason provided"
    ):

        if not await self.owner_check(interaction):
            return


        if not await self.can_punish(interaction, member):
            return


        if minutes > 40320:

            await interaction.response.send_message(
                embed=error(
                    "Invalid Time",
                    "Maximum timeout is 28 days."
                ),
                ephemeral=True
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


            await send_log(
                interaction.guild,
                "⏱️ Member Timeout",
                (
                    f"User: {member.mention}\n"
                    f"Duration: {minutes} minutes\n"
                    f"Reason: {reason}\n"
                    f"Case: #{case}"
                )
            )


            await interaction.response.send_message(
                embed=success(
                    "Timeout Applied",
                    f"Case: #{case}"
                )
            )


        except discord.Forbidden:

            await interaction.response.send_message(
                embed=error(
                    "Failed",
                    "Missing permissions."
                ),
                ephemeral=True
            )



    # ==============================
    # WARN
    # ==============================

    @app_commands.command(
        name="warn",
        description="Warn a member"
    )
    async def warn(
        self,
        interaction,
        member: discord.Member,
        reason: str
    ):

        if not await self.owner_check(interaction):
            return


        warning = await add_warning(
            interaction.guild.id,
            member.id,
            interaction.user.id,
            reason
        )


        await send_log(
            interaction.guild,
            "⚠️ Warning Added",
            (
                f"User: {member.mention}\n"
                f"Reason: {reason}\n"
                f"Warning ID: #{warning}"
            )
        )


        await interaction.response.send_message(
            embed=success(
                "Warning Added",
                f"Warning ID: #{warning}"
            )
        )



    # ==============================
    # WARNINGS
    # ==============================

    @app_commands.command(
        name="warnings",
        description="View warnings"
    )
    async def warnings(
        self,
        interaction,
        member: discord.Member
    ):

        data = await get_warnings(
            interaction.guild.id,
            member.id
        )


        if not data:

            await interaction.response.send_message(
                embed=success(
                    "Warnings",
                    "No warnings found."
                )
            )

            return


        text = ""

        for warn in data:

            text += (
                f"ID: #{warn[0]}\n"
                f"Reason: {warn[4]}\n\n"
            )


        await interaction.response.send_message(
            embed=discord.Embed(
                title=f"Warnings for {member}",
                description=text,
                color=0xFEE75C
            )
        )



# ==============================
# Setup
# ==============================

async def setup(bot):

    await bot.add_cog(
        Moderation(bot)
    )
