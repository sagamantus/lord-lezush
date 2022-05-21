from itertools import count
import discord
from discord.ext import commands
import random
import os

client = commands.Bot(command_prefix='^')

player1 = ''
player2 = ''
turn = ''
gameOver = True

board = []

winningConditions = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [0,3,6],
    [1,4,7],
    [2,5,8],
    [0,4,8],
    [2,4,6]
] 

@client.command()
async def ttt( ctx: commands.context , p1:discord.Member , p2:discord.Member ):
    
    global player1
    global player2
    global turn
    global gameOver
    global count
    global board

    if gameOver :
        """
            Game Start
        """
        global board
        board = [":purple_square:",":purple_square:",":purple_square:",
                 ":purple_square:",":purple_square:",":purple_square:",
                 ":purple_square:",":purple_square:",":purple_square:"]
        turn = ''
        gameOver = False
        count = 0
        player1 = p1
        player2 = p2
        #print board
        line = ''
        for x in range(len(board)):
            if x==2 or x==5 or x==8:
                line+= " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line+= " " + board[x]
        # who goes first
        num = random.randint(1,2)
        if num == 1 :
            turn = player1
            await ctx.send(f"It is {player1.mention}'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send(f"It is {player2.mention}'s turn.")
    else:
        await ctx.send("Game in Progress")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":white_chech_mark:"
            elif turn == player2:
                mark = ":x:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                check(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Choose int between 1 to 9 and choose a unmarked square.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the ^tictactoe command and ^place (num) to place.")

def check(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]]==mark and board[condition[1]]==mark and board[condition[2]]==mark :
            gameOver=True
        
@ttt.error
async def err(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Enter 2 players")
    elif isinstance(error,commands.BadArgument):
        await ctx.send("Please mention the players(eg. <@977439095380922388>)")

@place.error
async def palce(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Enter 2 players")
    elif isinstance(error,commands.BadArgument):
        await ctx.send("Please enter an integer")


client.run('OTc3NDM5MDk1MzgwOTIyMzg4.GFIZhf.ZJffev3HqB-wKrptZDBWKfLaR3TjQM2ENnvBso')