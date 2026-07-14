import discord
from discord.ext import commands
from datetime import timedelta

from config import LOG_CHANNEL_ID


OWNER_ID = 972434666948808724


def owner_only():
    async def predicate(ctx):
        return ctx.author.id == OWNER_ID
    return commands.check(predicate)


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    async def log(
        self,
        guild,
        title,
        description,
        color=discord.Color.blurple()
    ):

        channel = guild.get_channel(LOG_CHANNEL_ID)

        if channel is None:
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        await channel.send(
            embed=embed
        )

    # ==============================
    # BAN
    # ==============================

    @commands.command(name="ban")
    @owner_only()
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):

        if member == ctx.author:
            return await ctx.send("❌ You can't ban yourself.")

        if member.top_role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't ban that member.")

        try:

            await member.send(
                embed=discord.Embed(
                    title="🔨 You have been banned",
                    description=f"**Server:** {ctx.guild.name}\n**Reason:** {reason}",
                    color=discord.Color.red()
                )
            )

        except:
            pass

        await member.ban(reason=reason)

        embed = discord.Embed(
            title="✅ Member Banned",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Member",
            value=f"{member} ({member.id})",
            inline=False
        )

        embed.add_field(
            name="Moderator",
            value=ctx.author.mention,
            inline=False
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        await ctx.send(embed=embed)

        await self.log(
            ctx.guild,
            "🔨 Member Banned",
            f"**Member:** {member}\n**Moderator:** {ctx.author}\n**Reason:** {reason}",
            discord.Color.red()
        )


    # ==============================
    # KICK
    # ==============================

    @commands.command(name="kick")
    @owner_only()
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):

        if member == ctx.author:
            return await ctx.send("❌ You can't kick yourself.")

        if member.top_role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't kick that member.")

        try:

            await member.send(
                embed=discord.Embed(
                    title="👢 You have been kicked",
                    description=f"**Server:** {ctx.guild.name}\n**Reason:** {reason}",
                    color=discord.Color.orange()
                )
            )

        except:
            pass

        await member.kick(reason=reason)

        embed = discord.Embed(
            title="✅ Member Kicked",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Member",
            value=f"{member} ({member.id})",
            inline=False
        )

        embed.add_field(
            name="Moderator",
            value=ctx.author.mention,
            inline=False
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        await ctx.send(embed=embed)

        await self.log(
            ctx.guild,
            "👢 Member Kicked",
            f"**Member:** {member}\n**Moderator:** {ctx.author}\n**Reason:** {reason}",
            discord.Color.orange()
        )


    # ==============================
    # SOFTBAN
    # ==============================

    @commands.command(name="softban")
    @owner_only()
    async def softban(self, ctx, member: discord.Member, *, reason="No reason provided"):

        if member == ctx.author:
            return await ctx.send("❌ You can't softban yourself.")

        if member.top_role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't softban that member.")

        try:

            await member.send(
                embed=discord.Embed(
                    title="🔨 You have been softbanned",
                    description=f"**Server:** {ctx.guild.name}\n**Reason:** {reason}",
                    color=discord.Color.red()
                )
            )

        except:
            pass

        await member.ban(reason=reason, delete_message_days=7)
        await ctx.guild.unban(member, reason="Softban complete")

        embed = discord.Embed(
            title="✅ Member Softbanned",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Member",
            value=f"{member} ({member.id})",
            inline=False
        )

        embed.add_field(
            name="Moderator",
            value=ctx.author.mention,
            inline=False
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        await ctx.send(embed=embed)

        await self.log(
            ctx.guild,
            "🔨 Member Softbanned",
            f"**Member:** {member}\n**Moderator:** {ctx.author}\n**Reason:** {reason}",
            discord.Color.red()
        )


    # ==============================
    # TIMEOUT
    # ==============================

    @commands.command(name="timeout")
    @owner_only()
    async def timeout(self, ctx, member: discord.Member, minutes: int, *, reason="No reason provided"):

        if member == ctx.author:
            return await ctx.send("❌ You can't timeout yourself.")

        if member.top_role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't timeout that member.")

        if minutes <= 0:
            return await ctx.send("❌ Minutes must be greater than 0.")

        if minutes > 40320:
            return await ctx.send("❌ Maximum timeout is 28 days (40320 minutes).")

        try:
            await member.send(
                embed=discord.Embed(
                    title="⏱️ You have been timed out",
                    description=f"**Server:** {ctx.guild.name}\n**Duration:** {minutes} minutes\n**Reason:** {reason}",
                    color=discord.Color.orange()
                )
            )
        except:
            pass

        await member.timeout(
            timedelta(minutes=minutes),
            reason=reason
        )

        embed = discord.Embed(
            title="✅ Member Timed Out",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Member",
            value=f"{member} ({member.id})",
            inline=False
        )

        embed.add_field(
            name="Duration",
            value=f"{minutes} minute(s)",
            inline=False
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        await ctx.send(embed=embed)

        await self.log(
            ctx.guild,
            "⏱️ Member Timed Out",
            f"**Member:** {member}\n**Moderator:** {ctx.author}\n**Duration:** {minutes} minute(s)\n**Reason:** {reason}",
            discord.Color.orange()
        )


    # ==============================
    # UNTIMEOUT
    # ==============================

    @commands.command(name="untimeout")
    @owner_only()
    async def untimeout(self, ctx, member: discord.Member):

        if member.top_role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't edit that member.")

        await member.timeout(
            None,
            reason=f"Untimeout by {ctx.author}"
        )

        embed = discord.Embed(
            title="✅ Timeout Removed",
            description=f"{member.mention} has been untimed out.",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

        await self.log(
            ctx.guild,
            "✅ Timeout Removed",
            f"**Member:** {member}\n**Moderator:** {ctx.author}",
            discord.Color.green()
        )


    # ==============================
    # UNBAN
    # ==============================

    @commands.command(name="unban")
    @owner_only()
    async def unban(self, ctx, user_id: int, *, reason="No reason provided"):

        try:
            user = await self.bot.fetch_user(user_id)

            await ctx.guild.unban(
                user,
                reason=reason
            )

            embed = discord.Embed(
                title="✅ Member Unbanned",
                color=discord.Color.green()
            )

            embed.add_field(
                name="User",
                value=f"{user} ({user.id})",
                inline=False
            )

            embed.add_field(
                name="Reason",
                value=reason,
                inline=False
            )

            await ctx.send(embed=embed)

            await self.log(
                ctx.guild,
                "✅ Member Unbanned",
                f"**User:** {user}\n**Moderator:** {ctx.author}\n**Reason:** {reason}",
                discord.Color.green()
            )

        except discord.NotFound:
            await ctx.send("❌ That user ID doesn't exist.")

        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to unban that user.")

        except Exception as e:
            await ctx.send(f"❌ Failed to unban user.\n```{e}```")

    # ==============================
    # WARN
    # ==============================

    @commands.command(name="warn")
    @owner_only()
    async def warn(self, ctx, member: discord.Member, *, reason):

        warning_id = await add_warning(
            ctx.guild.id,
            member.id,
            ctx.author.id,
            reason
        )

        try:
            await member.send(
                embed=discord.Embed(
                    title="⚠️ You have been warned",
                    description=f"**Server:** {ctx.guild.name}\n**Reason:** {reason}",
                    color=discord.Color.orange()
                )
            )
        except:
            pass

        embed = discord.Embed(
            title="⚠️ Warning Added",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="Member",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        embed.add_field(
            name="Warning ID",
            value=str(warning_id),
            inline=False
        )

        await ctx.send(embed=embed)

        await self.log(
            ctx.guild,
            "⚠️ Warning Added",
            f"**Member:** {member}\n**Moderator:** {ctx.author}\n**Reason:** {reason}"
        )


    # ==============================
    # WARNINGS
    # ==============================

    @commands.command(name="warnings")
    @owner_only()
    async def warnings(self, ctx, member: discord.Member):

        data = await get_warnings(
            ctx.guild.id,
            member.id
        )

        if not data:
            return await ctx.send(
                embed=discord.Embed(
                    title="Warnings",
                    description="This member has no warnings.",
                    color=discord.Color.green()
                )
            )

        embed = discord.Embed(
            title=f"Warnings for {member}",
            color=discord.Color.orange()
        )

        for warn in data:
            embed.add_field(
                name=f"Warning #{warn[0]}",
                value=warn[4],
                inline=False
            )

        await ctx.send(embed=embed)


    # ==============================
    # CLEAR
    # ==============================

    @commands.command(name="clear")
    @owner_only()
    async def clear(self, ctx, amount: int):

        if amount < 1:
            return await ctx.send("❌ Amount must be at least 1.")

        if amount > 100:
            return await ctx.send("❌ Maximum is 100 messages.")

        deleted = await ctx.channel.purge(limit=amount + 1)

        embed = discord.Embed(
            title="🧹 Messages Cleared",
            description=f"Deleted **{len(deleted)-1}** messages.",
            color=discord.Color.green()
        )

        msg = await ctx.send(embed=embed)
        await msg.delete(delay=5)

        await self.log(
            ctx.guild,
            "🧹 Messages Cleared",
            f"**Moderator:** {ctx.author}\n**Deleted:** {len(deleted)-1}"
        )


    # ==============================
    # NICKNAME
    # ==============================

    @commands.command(name="nickname")
    @owner_only()
    async def nickname(self, ctx, member: discord.Member, *, text=None):

        if member.top_role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't edit that member.")

        try:

            if text is None:
                await member.edit(nick=None)
            else:
                await member.edit(nick=text)

            await ctx.send(
                embed=discord.Embed(
                    title="✅ Nickname Updated",
                    description=f"{member.mention}'s nickname has been updated.",
                    color=discord.Color.green()
                )
            )

        except Exception as e:
            await ctx.send(f"❌ Failed.\n```{e}```")

from discord.ext import commands
import discord

OWNER_ID = 972434666948808724


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="nicknameall")
    async def nicknameall(self, ctx, *, text=None):

        if ctx.author.id != OWNER_ID:
            return

        changed = 0
        failed = 0

        msg = await ctx.send(
            embed=discord.Embed(
                title="📝 Updating Nicknames...",
                description="Please wait...",
                color=discord.Color.orange()
            )
        )

        for member in ctx.guild.members:

            if member.bot:
                continue

            try:

                if member.top_role >= ctx.guild.me.top_role:
                    failed += 1
                    continue

                if text is None:

                    await member.edit(
                        nick=None,
                        reason=f"Reset by {ctx.author}"
                    )

                else:

                    current = member.nick or member.name

                    if f"| {text}" in current:
                        continue

                    await member.edit(
                        nick=f"{current} | {text}",
                        reason=f"Nickname All by {ctx.author}"
                    )

                changed += 1

            except Exception:
                failed += 1

        embed = discord.Embed(
            title="✅ Nickname All Finished",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Changed",
            value=str(changed),
            inline=True
        )

        embed.add_field(
            name="Failed",
            value=str(failed),
            inline=True
        )

        if text is None:
            embed.add_field(
                name="Action",
                value="Reset all nicknames",
                inline=False
            )
        else:
            embed.add_field(
                name="Added",
                value=f"`| {text}`",
                inline=False
            )

        await msg.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
