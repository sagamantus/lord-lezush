import nextcord as discord, datetime, requests, time
from nextcord.ext import commands
from utils import config

class Github(commands.Cog, name="Github"):

    def __init__(self, client):
        self.client = client

    @commands.command(name="github")
    async def github(self, ctx: commands.Context, *, user: str):
        """
        Get information about a GitHub User/Organisation.
        """

        if ctx.author == self.client.user: return

        data = requests.get(f"https://api.github.com/users/{user}").json()

        try: 
            if data["message"].lower() == "not found": git_embed = discord.Embed(description = f"No user named **{user}** found.", color = config.EMBED_COLOR, timestamp=ctx.message.created_at)

        except KeyError:
            git_embed = discord.Embed(color = config.EMBED_COLOR, timestamp=ctx.message.created_at)

            if data['bio']: git_embed.description = data["bio"]
            git_embed.set_author(name=data["login"], icon_url = data["avatar_url"], url=data["html_url"])
            git_embed.set_thumbnail(url=data["avatar_url"])

            git_embed.add_field(name="Public Repos",value=data["public_repos"])
            git_embed.add_field(name="Public Gists",value=data["public_gists"])
            git_embed.add_field(name="Repos Url",value=f"[Click Me.]({data['html_url']}?tab=repositories)")
            git_embed.add_field(name="Followers",value=data["followers"])
            git_embed.add_field(name="Following",value=data["following"])
            git_embed.add_field(name="Account Type",value=data['type'])
            git_embed.add_field(name="Created At",value=f"<t:{int(datetime.datetime.timestamp(datetime.datetime.strptime(data['created_at'],'%Y-%m-%dT%H:%M:%SZ')))}:f>")
            git_embed.add_field(name="Updated At",value=f"<t:{int(datetime.datetime.timestamp(datetime.datetime.strptime(data['updated_at'],'%Y-%m-%dT%H:%M:%SZ')))}:f>")

        git_embed.set_footer(text=f"Requested by {ctx.author}")

        await ctx.reply(embed=git_embed)
    
    @github.error
    async def github_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user': await ctx.reply(embed = discord.Embed(description=f"I expect a user or organisation's name.", color = config.EMBED_COLOR, timestamp = ctx.message.created_at)); return
        else:
            await ctx.reply(embed = discord.Embed(description=f"```{error.__name__}:{error}```", color = config.EMBED_COLOR, timestamp = ctx.message.created_at))


def setup(client):
    client.add_cog(Github(client))
