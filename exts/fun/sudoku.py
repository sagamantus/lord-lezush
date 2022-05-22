import nextcord as discord
from nextcord.ext import commands
from utils import config

class Sudoku(commands.Cog, name="Sudoku"):

    def __init__(self, client):
        self.client = client

    @commands.command(name="sudoku", aliases=["sdk"])
    async def sudoku(self, ctx):
        pass


def setup(client):
    client.add_cog(Sudoku(client))