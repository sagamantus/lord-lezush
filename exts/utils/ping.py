import nextcord as discord
from nextcord.ext import commands
from utils import config

class Ping(commands.Cog, name="Ping"):

    def __init__(self, client):
        self.client = client

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """
        Bot's latency.
        """

        if ctx.author == self.client.user:
            return

        await ctx.reply(
            embed=discord.Embed(
                description=f"Pong: `{round(self.client.latency*1000)} ms`",
                color=config.EMBED_COLOR,
                timestamp=ctx.message.created_at
            ), 
            mention_author=False
        )


def setup(client):
    client.add_cog(Ping(client))