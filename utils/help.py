import nextcord as discord
import asyncio
import itertools
from nextcord.ext import commands
from utils import config

class HelpCommand(commands.HelpCommand):

    def HelpEmbed(self, ctx: commands.Context, description: str, footer: str = None):
        help_embed = discord.Embed(
            description=description,
            color=config.EMBED_COLOR,
            timestamp=ctx.message.created_at
        )

        help_embed.set_author(name=f"Command Help", icon_url=ctx.bot.user.avatar)

        if footer != None:
            help_embed.set_footer(text=footer)

        return help_embed

    def paginator(self, n, iterable):
        args = [iter(iterable)] * n
        return list([e for e in t if e != None] for t in itertools.zip_longest(*args))

    # .help
    async def send_bot_help(self, mapping):
        no_cog_commands = sorted(mapping.pop(None), key=lambda c: c.qualified_name)
        cogs = list(sorted(mapping, key=lambda c: c.qualified_name))
        cogs = self.paginator(4, cogs)

        total_pages, current_page = len(cogs), 1

        data = ''
        for cog in cogs[current_page-1]:
            data += "**"+cog.qualified_name+"**\n"
            if cog.description:
                data += "*"+cog.description+"*\n"
            for command in sorted(cog.get_commands()):
                data += "`"+config.PREFIX[0]+command.name+"`\n"
                data += "*"+command.help+"*\n"
            data += "\n"

        message = await self.context.reply(embed=self.HelpEmbed(
            ctx=self.context,
            description=data,
            footer=f"Page {current_page}/{total_pages}"
            ),
            mention_author=False
        )

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        await message.add_reaction("🗑️")

        def check(reaction, user):
            """
            This makes sure nobody except the command sender can interact with the "menu"
            """
            return str(reaction.emoji) in ["◀️", "▶️", "🗑️"] and user != self.context.bot.user

        while True:
            try:
                reaction, user = await self.context.bot.wait_for("reaction_add", timeout=120, check=check)

                if str(reaction.emoji) == "▶️" and current_page != total_pages and reaction.message.id == message.id:
                    current_page += 1
                    data = ''
                    for cog in cogs[current_page-1]:
                        data += "**"+cog.qualified_name+"**\n"
                        if cog.description:
                            data += "*"+cog.description+"*\n"
                        for command in sorted(cog.get_commands()):
                            data += "`"+config.PREFIX[0]+command.name+"`\n"
                            data += "*"+command.help+"*\n"
                        data += "\n"

                    await message.edit(embed=self.HelpEmbed(
                        ctx=self.context,
                        description=data,
                        footer=f"Page {current_page}/{total_pages}"
                        ),
                        mention_author=False
                    )
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and current_page > 1 and reaction.message.id == message.id:
                    current_page -= 1
                    data = ''
                    for cog in cogs[current_page-1]:
                        data += "**"+cog.qualified_name+"**\n"
                        if cog.description:
                            data += "*"+cog.description+"*\n"
                        for command in sorted(cog.get_commands()):
                            data += "`"+config.PREFIX[0]+command.name+"`\n"
                            data += "*"+command.help+"*\n"
                        data += "\n"

                    await message.edit(embed=self.HelpEmbed(
                        ctx=self.context,
                        description=data,
                        footer=f"Page {current_page}/{total_pages}"
                        ),
                        mention_author=False
                    )
                    await message.remove_reaction(reaction, user)

                elif user == self.context.author and str(reaction.emoji) == "🗑️" and reaction.message.id == message.id:
                    await message.delete()

                else:
                    await message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                try:
                    await message.clear_reactions()
                    break
                except Exception:
                    try:
                        await message.clear_reactions()
                        break
                    except Exception:
                        break

   # .help <command>
    async def send_command_help(self, command):
        embed = discord.Embed(colour=config.EMBED_COLOR, timestamp=self.context.message.created_at)
        embed.set_author(name=f"Command: {command}", icon_url=self.context.bot.user.avatar)
        embed.add_field(name="Description", value=command.help, inline=False)
        embed.add_field(name="Usage", value=self.get_command_signature(command), inline=False)
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)

        await self.context.reply(embed=embed, mention_author=False)

   # .help <cog>
    async def send_cog_help(self, cog):
        data = ''
        data += "**"+cog.qualified_name+"**\n"
        if cog.description:
            data += "*"+cog.description+"*\n"
        for command in sorted(cog.get_commands()):
            data += "`"+config.PREFIX[0]+command.name+"`\n"
            data += "*"+command.help+"*\n"
        data += "\n"

        await self.context.reply(embed=self.HelpEmbed(
            ctx=self.context,
            description=data
            ),
            mention_author=False
        )
