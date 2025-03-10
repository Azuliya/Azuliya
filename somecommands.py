import time
import disnake.ext
from disnake.ext import commands


class SomeCommands(commands.Cog):
    """A couple of simple shitty commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="#to be added#")
    async def w1(self, ctx: commands.Context):
        await ctx.send("#to be added")

    @commands.command(name="CLEAN")
    async def w1(self, ctx: commands.Context):
        await ctx.send("CLEAN THE ENVIRONMENT BY EXTERMINATING HUMANS!!!")

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        await message.edit(content=f"Current ping: {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    @commands.command(name="setstatus")
    async def setstatus(self, ctx: commands.Context, *, text: str):
        await self.bot.change_presence(activity=disnake.Game(name=text))


def setup(bot: commands.Bot):
    bot.add_cog(SomeCommands(bot))
