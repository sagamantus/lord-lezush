import nextcord as discord
from nextcord.ext import commands

class Ping(commands.Cog, name="Info"):

    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Bot's latency.
        """

        if ctx.author == self.client.user:
            return

        await ctx.reply(
            embed=discord.Embed(
                description=f"Pong: `{round(self.client.latency*1000)} ms`",
                color=0x2F3136,
                timestamp=ctx.message.created_at
            ), 
            mention_author=False
        )


def setup(client):
    client.add_cog(Ping(client))