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
