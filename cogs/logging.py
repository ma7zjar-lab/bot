import discord
from discord.ext import commands

from config import LOG_CHANNEL_ID
from utils import info


class Logging(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    # ==============================
    # Send Log Function
    # ==============================

    async def send_log(
        self,
        guild,
        title,
        description,
        color=0x5865F2
    ):

        if not guild:
            return


        channel = guild.get_channel(
            LOG_CHANNEL_ID
        )


        if not channel:
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


    # ==============================
    # Member Join Logs
    # ==============================

    @commands.Cog.listener()
    async def on_member_join(
        self,
        member
    ):

        await self.send_log(
            member.guild,
            "📥 Member Joined",
            (
                f"User: {member.mention}\n"
                f"ID: `{member.id}`"
            ),
            0x57F287
        )


    # ==============================
    # Member Leave Logs
    # ==============================

    @commands.Cog.listener()
    async def on_member_remove(
        self,
        member
    ):

        await self.send_log(
            member.guild,
            "📤 Member Left",
            (
                f"User: {member}\n"
                f"ID: `{member.id}`"
            ),
            0xED4245
        )


    # ==============================
    # Message Delete Logs
    # ==============================

    @commands.Cog.listener()
    async def on_message_delete(
        self,
        message
    ):

        if message.author.bot:
            return


        await self.send_log(
            message.guild,
            "🗑️ Message Deleted",
            (
                f"Author: {message.author.mention}\n"
                f"Channel: {message.channel.mention}\n\n"
                f"{message.content[:1000]}"
            )
        )


    # ==============================
    # Message Edit Logs
    # ==============================

    @commands.Cog.listener()
    async def on_message_edit(
        self,
        before,
        after
    ):

        if before.author.bot:
            return


        if before.content == after.content:
            return


        await self.send_log(
            before.guild,
            "✏️ Message Edited",
            (
                f"Author: {before.author.mention}\n"
                f"Channel: {before.channel.mention}\n\n"
                f"Before:\n{before.content[:500]}\n\n"
                f"After:\n{after.content[:500]}"
            )
        )


    # ==============================
    # Nickname Logs
    # ==============================

    @commands.Cog.listener()
    async def on_member_update(
        self,
        before,
        after
    ):

        if before.nick != after.nick:

            await self.send_log(
                after.guild,
                "📝 Nickname Changed",
                (
                    f"User: {after.mention}\n"
                    f"Old: `{before.nick}`\n"
                    f"New: `{after.nick}`"
                )
            )


# ==============================
# Setup
# ==============================

async def setup(bot):

    await bot.add_cog(
        Logging(bot)
    )
