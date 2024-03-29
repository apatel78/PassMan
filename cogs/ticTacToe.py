import discord
from discord.ext import commands
import platform
from pathlib import Path
import json
import math
import random

cwd = Path(__file__).parents[1]
cwd = str(cwd)

#Characters for each user
human = 'x'
robot = 'o'

#If there is a game going on right now
inProgress = False

#Game type
isImpossible = False
isEasy = False
isHuman = False

#If the player is going second
isFirst = False

#If the player is player one
isPlayerOne = False

#The gameboard
gameboard = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

#Return 2 if AI wins, -2 if humann wins, 1 if the game can still be played, 0 if draw
def findWinner(gameboard, human, robot):

    for row in range(3):
        if(gameboard[row][0] == gameboard[row][1] == gameboard[row][2]):
            if gameboard[row][0] == human:
                return -2
            elif gameboard[row][0] == robot:
                return 2

    for col in range(3):
        if(gameboard[0][col] == gameboard[1][col] == gameboard[2][col]):
            if gameboard[0][col] == human:
                return -2
            elif gameboard[0][col] == robot:
                return 2

    if(gameboard[0][0] == gameboard[1][1] == gameboard[2][2]):
        if gameboard[0][0] == human:
            return -2
        elif gameboard[0][0] == robot:
            return 2

    if(gameboard[0][2] == gameboard[1][1] == gameboard[2][0]):
        if gameboard[0][2] == human:
            return -2
        elif gameboard[0][2] == robot:
            return 2

    for row in range(3):
        for col in range(3):
            if gameboard[row][col] == '-':
                return 1

    return 0

#Determines the best move for the AI
def minimax(gameboard, depth, isRobot, human, robot):

    winner = findWinner(gameboard, human, robot)

    #If the game is over
    if (winner == 2 or winner == -2 or winner == 0):
        return winner

    if isRobot:
        best = -math.inf

        for i in range(3) :
            for j in range(3) :
                if gameboard[i][j] == '-' :

                    gameboard[i][j] = robot
                    best = max(best, minimax(gameboard, depth + 1, not isRobot, human, robot))
                    gameboard[i][j] = '-'

    else:
        best = math.inf

        for i in range(3) :
            for j in range(3) :
                if gameboard[i][j] == '-' :

                    gameboard[i][j] = human
                    best = min(best, minimax(gameboard, depth + 1, not isRobot, human, robot))
                    gameboard[i][j] = '-'

    return best

#Simulates the Impossible AI Turn
def simulateImpossible(gameboard, human, robot):

    best = -math.inf
    bestcoord = (-1, -1)

    for i in range(3):
        for j in range(3):
            if gameboard[i][j] == '-':

                gameboard[i][j] = robot
                temp = minimax(gameboard, 0, False, human, robot)
                gameboard[i][j] = '-'

                if temp > best:
                    bestcoord = (i, j)
                    best = temp

    gameboard[bestcoord[0]][bestcoord[1]] = robot

#Simulates the Easy AI Turn
def simulateEasy(gameboard, human, robot):
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2]
    }

    numbernotWorking = True

    while(numbernotWorking):
        number = random.randint(1, 9)
        coordinate = moves[number]
        if not taken(gameboard, coordinate):
            numbernotWorking = False

    gameboard[coordinate[0]][coordinate[1]] = robot



#Determines if the tile is taken
def taken(gameboard, input):
    if (gameboard[input[0]][input[1]] != '-'):
        return True
    return False

class TicTacToe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Prints a helpful message about this game
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.guild)
    async def thelp(self, ctx):
        await ctx.send(f"```Welcome to TicTacToe. There are three ways to play this game: Versus another human (h), an easy robot (e), and an impossible robot (i). Start the game by having Player One use tbegin gamemode.\nEx: tbegin e```")
        await ctx.send(f"```If you would like to change your symbol, Player One should use tsymbol symbol before using tbegin.\nEx: tsymbol x or tsymbol o```")
        await ctx.send(f"```At any time, you can view where to place a tile using tboard. You may also end any game by using tend.```")


    #Allows the user to select the gamemode
    @commands.command()
    async def tbegin(self, ctx, gamemode):

        global isImpossible
        global isEasy
        global isHuman
        global isFirst
        global gameboard
        global inProgress

        if inProgress:
            await ctx.send(f"There is currently a game in progress so you may not set the gamemode")
            return

        gamemode = gamemode.lower()

        if gamemode == 'e':
            isEasy = True
            await ctx.send(f"You have selected the easy robot. Use tbegin f to go first or tbegin s to go second")
        elif gamemode == 'h':
            isHuman = True
            inProgress = True
            await ctx.send(f"You have selected the Human vs Human. Player One, use tadd tilespot to begin. Ex: tadd 4")
        elif gamemode == 'i':
            isImpossible = True
            await ctx.send(f"You have selected the impossible robot. Use tbegin f to go first or tbegin s to go second")

        elif gamemode == 'f':
            if isEasy or isImpossible and not isHuman:
                await ctx.send(f"You will go first. Use tadd tilespot to begin. Ex: tadd 4 ")
            else:
                await ctx.send(f"Wrong gamemode")
            inProgress = True
            isFirst = True

        elif gamemode == 's':
            if isEasy or isImpossible and not isHuman:
                await ctx.send(f"You will go second. Use tadd tilespot to place your tile. Ex: tadd 4 ")
            else:
                await ctx.send(f"Wrong gamemode")
                return

            if isImpossible:
                simulateImpossible(gameboard, human, robot)
            elif isEasy:
                simulateEasy(gameboard, human, robot)
            #Print the current state of the gameboard
            await ctx.send(f"[   {gameboard[0][0]}   ] [   {gameboard[0][1]}   ] [   {gameboard[0][2]}   ]\n[   {gameboard[1][0]}   ] [   {gameboard[1][1]}   ] [   {gameboard[1][2]}   ]\n[   {gameboard[2][0]}   ] [   {gameboard[2][1]}   ] [   {gameboard[2][2]}   ]")

            inProgress = True

        else:
            await ctx.send(f"Invalid gamemode, please try again.")

    #Lets the user set their symbol. Only allowed if there is not a game currently going on
    @commands.command()
    async def tsymbol(self, ctx, symbol):

        global human
        global robot

        if inProgress:
            await ctx.send(f"There is currently a game in progress so you may not set your symbol")
            return
        if symbol == 'x':
            await ctx.send(f"Your symbol is 'x'")
            human = 'x'
            robot = 'o'
        elif symbol == 'o':
            await ctx.send(f"Your symbol is 'o'")
            human = 'o'
            robot = 'x'
        else:
            await ctx.send(f"Invalid symbol, please try again.")

    #Lets the input which tile they want to select
    @commands.command()
    async def tadd(self, ctx, number):

        global inProgress
        global gameboard
        global isImpossible
        global isEasy
        global isHuman
        global isPlayerOne
        global isFirst

        if not inProgress:
            await ctx.send(f"A game has not been started. Please use thelp for more information")
            return

        number = int(number)

        #Check if the number is in the given range
        if number < 1 or number > 9:
            await ctx.send(f"Invalid tile, please try again.")
            return

        #Input to gameboard Spot Dictionary
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2]
        }

        coordinate = moves[number]

        #Check if the tile has already been taken
        if taken(gameboard, coordinate):
            await ctx.send(f"This tile has been taken. Please select another tile")
            return

        #Add the human choice to the gameboard
        if isHuman:
            if isPlayerOne:
                gameboard[coordinate[0]][coordinate[1]] = robot
                isPlayerOne = False
            else:
                gameboard[coordinate[0]][coordinate[1]] = human
                isPlayerOne = True
        else:
            gameboard[coordinate[0]][coordinate[1]] = human

        isDone = True
        #If game can still continue
        if findWinner(gameboard, human, robot) == 1:
            if isImpossible:
                simulateImpossible(gameboard, human, robot)
            elif isEasy:
                simulateEasy(gameboard, human, robot)
            isDone = False
            #Print the current state of the gameboard
            await ctx.send(f"[   {gameboard[0][0]}   ] [   {gameboard[0][1]}   ] [   {gameboard[0][2]}   ]\n[   {gameboard[1][0]}   ] [   {gameboard[1][1]}   ] [   {gameboard[1][2]}   ]\n[   {gameboard[2][0]}   ] [   {gameboard[2][1]}   ] [   {gameboard[2][2]}   ]")

        #If the game was a draw
        if findWinner(gameboard, human, robot) == 0:
            if isFirst or isDone:
                await ctx.send(f"[   {gameboard[0][0]}   ] [   {gameboard[0][1]}   ] [   {gameboard[0][2]}   ]\n[   {gameboard[1][0]}   ] [   {gameboard[1][1]}   ] [   {gameboard[1][2]}   ]\n[   {gameboard[2][0]}   ] [   {gameboard[2][1]}   ] [   {gameboard[2][2]}   ]")

            await ctx.send(f"The game ended in a draw!")

            inProgress = False
            isImpossible = False
            isHuman = False
            isEasy = False
            isFirst = False

            gameboard = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

        #If the AI won
        elif findWinner(gameboard, human, robot) == 2:
            if isFirst or isDone:
                await ctx.send(f"[   {gameboard[0][0]}   ] [   {gameboard[0][1]}   ] [   {gameboard[0][2]}   ]\n[   {gameboard[1][0]}   ] [   {gameboard[1][1]}   ] [   {gameboard[1][2]}   ]\n[   {gameboard[2][0]}   ] [   {gameboard[2][1]}   ] [   {gameboard[2][2]}   ]")

            if isHuman:
                await ctx.send(f"Player Two has won!")
            else:
                await ctx.send(f"Unlucky, you lost")

            inProgress = False
            isImpossible = False
            isHuman = False
            isEasy = False
            isFirst = False

            gameboard = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

        #If the human won
        elif findWinner(gameboard, human, robot) == -2:
            if isFirst or isDone:
                await ctx.send(f"[   {gameboard[0][0]}   ] [   {gameboard[0][1]}   ] [   {gameboard[0][2]}   ]\n[   {gameboard[1][0]}   ] [   {gameboard[1][1]}   ] [   {gameboard[1][2]}   ]\n[   {gameboard[2][0]}   ] [   {gameboard[2][1]}   ] [   {gameboard[2][2]}   ]")
            if isHuman:
                await ctx.send(f"Player One has won!")
            else:
                await ctx.send(f"Congrats, you won!")

            inProgress = False
            isImpossible = False
            isHuman = False
            isEasy = False
            isFirst = False

            gameboard = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

    #Clear the gameboard and set inProgress to false
    @commands.command()
    async def tend(self, ctx):

        global inProgress
        global gameboard
        global isImpossible
        global isEasy
        global isHuman
        global isFirst

        await ctx.send(f"The game has ended, please use tbegin to start a new one")
        gameboard = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

        inProgress = False
        isImpossible = False
        isHuman = False
        isEasy = False
        isFirst = False

    #Print which number corresponds to which spot on the gameboard
    @commands.command()
    @commands.cooldown(1,10, commands.BucketType.guild)
    async def tboard(self, ctx):
        await ctx.send("[   1   ] [   2   ] [   3   ]\n[  4   ] [   5   ] [   6   ]\n[   7  ] [   8   ] [   9   ]")


def setup(bot):
    bot.add_cog(TicTacToe(bot))
