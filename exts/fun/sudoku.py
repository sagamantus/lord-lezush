import nextcord as discord
from nextcord.ext import commands
from utils import config
from sudoku import Sudoku

class Sdk(commands.Cog, name="Sudoku"):

    def __init__(self, client):
        self.client = client

    @commands.command(name="sudoku", aliases=["sdk"])
    async def sdk(self, ctx: commands.Context, width: int = 3 , height: int = 3 , difficulty: float = 0.2):
        """
        Generates a sudoku.
        """
        puzzle = Sudoku(width , height, difficulty=difficulty)
        await ctx.reply(f"**{width}x{height} SUDOKU**\n*Difficulty: {difficulty}*\n```\n{puzzle._Sudoku__format_board_ascii()}\n```", mention_author=False)

    @commands.command(name="sudokusolve" , aliases=["sdkslv", "sdksolve"])
    async def stdslv(self, ctx: commands.Context):
        """
        Solves the generated suduko in the message reference.
        """
        if ctx.message.reference is None:
            await ctx.reply(
                embed=discord.Embed(
                    description=f"You must reply to the sudoku puzzle that must be solved.",
                    color=config.EMBED_COLOR,
                    timestamp=ctx.message.created_at
                ), 
                mention_author=False
            )
            return
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        data = message.content.split("\n")
        width = int(data[0].split("x")[0][2:])
        height = int((data[0].split("x")[1]).split(" ")[0])
        difficulty = float(data[1].split(": ")[1][:-1])
        board = []
        for row in data[3:]:
            step = len(str(height*width))
            if row.startswith("|"):
                r = []
                element = 0
                while element<len(row):
                    if row[element] == '|':
                        element +=2
                    else:
                        if row[element: element+step] == " "*step: r.append(None)
                        else: r.append(int(row[element: element+step]))
                        element += step+1
                board.append(r)
        puzzle = Sudoku(width , height, difficulty=difficulty, board=board).solve()
        await ctx.send(f"**{width}x{height} SUDOKU (Solved)**\n*Difficulty: {difficulty}*\n```\n{puzzle._Sudoku__format_board_ascii()}\n```")


def setup(client):
    client.add_cog(Sdk(client))