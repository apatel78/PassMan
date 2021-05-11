import discord
from discord.ext import commands
import platform
from pathlib import Path
import json

import cogs._json

cwd = Path(__file__).parents[1]
cwd = str(cwd)
outer = {}
outer = json.load(open(cwd+'\localstorage\\smurfs.json'))
outerKey = 0

#Potential Improvements:
#Sort the Dictionary
#React to message depending on successful or not

#Smurf channel checker
def smurfchannelcheck(channel):
    if channel == 840414501660917790 or channel == 840705049444483102:
        return True
    return False

class Smurf(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Sends a help message to the user about the smurf account commands
    @commands.command()
    @commands.cooldown(1,30, commands.BucketType.guild)
    async def shelp(self, ctx):
        if smurfchannelcheck(ctx.channel.id):
            help1 = open(cwd+'\\textfiles\\help1.txt', "r")
            help2 = open(cwd+'\\textfiles\\help2.txt', "r")
            await ctx.send(help1.read())
            await ctx.send(help2.read())

    #MAKE IT SO NO K NUMBERS CAN BE THE SAME
    #Adds a smurf account to the Dicitionary
    @commands.command(name='sadd')
    async def _sadd(self, ctx, username, password, rank, number):
        if smurfchannelcheck(ctx.channel.id):
            global outerKey
            for k, v in outer.items():
                for x, y in v.items():
                    if y == username:
                        await ctx.send(f"{username} already exists")
                        return
            #Loop through all keys in outer Dictionary
            temp = {int(k):v for k,v in outer.items()}
            seen = True
            while seen:
                seen = False
                for k,v in temp.items():
                    if k == outerKey:
                        outerKey = k + 1
                        seen = True
            if (number == '0' or number == '1' or number == '2' or number == '3') and (not any(i.isdigit() for i in rank)):
                    rank = rank.upper()
                    inner = {
                        'Username': username,
                        'Password': password,
                        'Rank': rank,
                        'Rank Number': number,
                        'Status': False,
                        'Last User': ''
                    }
                    outer.update({outerKey: inner})
                    cogs._json.write_json(outer, "smurfs")
                    outerKey = outerKey + 1
                    await ctx.send(f"{username} added")
            else:
                await ctx.send(f"Invalid Rank Format")


    #Removes a smurf account from the Dictionary
    @commands.command(name='sremove')
    async def _sremove(self, ctx, username):
        if smurfchannelcheck(ctx.channel.id):
            for k, v in outer.items():
                for x, y in v.items():
                    if y == username:
                        outer.pop(k)
                        cogs._json.write_json(outer, "smurfs")
                        await ctx.send(f"{username} was deleted")
                        return
            await ctx.send(f"{username} does not exist")


    #Changes the rank of a smurf account
    @commands.command(name='serank')
    async def _serank(self, ctx, username, rank, number):
        if smurfchannelcheck(ctx.channel.id):
            if (number == '0' or number == '1' or number == '2' or number == '3') and (not any(i.isdigit() for i in rank)):
                rank = rank.upper()
                for k, v in outer.items():
                    for x, y in v.items():
                        if y == username:
                            v['Rank'] = rank
                            v['Rank Number'] = number
                            cogs._json.write_json(outer, "smurfs")
                            await ctx.send(f"{username} had its rank changed to {rank} {number}")
                            return
                await ctx.send(f"{username} does not exist")
            else:
                await ctx.send(f"Invalid Rank Format")


    #Updates the account username
    @commands.command(name='seusername')
    async def _seusername(self, ctx, username, newusername):
        if smurfchannelcheck(ctx.channel.id):
            for k, v in outer.items():
                for x, y in v.items():
                    if y == username:
                        v['Username'] = newusername
                        cogs._json.write_json(outer, "smurfs")
                        await ctx.send(f"{username} had its username changed to {newusername}")
                        return
            await ctx.send(f"{username} does not exist")


    #Updates the account password
    @commands.command(name='sepassword')
    async def _sepassword(self, ctx, username, newpassword):
        if smurfchannelcheck(ctx.channel.id):
            for k, v in outer.items():
                for x, y in v.items():
                    if y == username:
                        v['Password'] = newpassword
                        cogs._json.write_json(outer, "smurfs")
                        await ctx.send(f"{username} had its username changed to {newpassword}")
                        return
            await ctx.send(f"{username} does not exist")


    #Updates all information about the account
    @commands.command(name='seall')
    async def _seall(self, ctx, username, newusername, newpassword, newrank, newnumber):
        if smurfchannelcheck(ctx.channel.id):
            newrank = newrank.upper()
            if (newnumber == '0' or newnumber == '1' or newnumber == '2' or newnumber == '3') and (not any(i.isdigit() for i in newrank)):
                for k, v in outer.items():
                    for x, y in v.items():
                        if y == username:
                            v['Username'] = newusername
                            v['Password'] = newpassword
                            v['Rank'] = newrank
                            v['Rank Number'] = newnumber
                            cogs._json.write_json(outer, "smurfs")
                            await ctx.send(f"{username} became: ```Username: {v['Username']}\nPassword: {v['Password']}\nRank: {v['Rank']} {v['Rank Number']}```")
                            return
            else:
                await ctx.send(f"Invalid Rank Format")
            await ctx.send(f"{username} does not exist")


    #Update the status of an account
    @commands.command(name='susing')
    async def _susing(self, ctx, username):
        if smurfchannelcheck(ctx.channel.id):
            for k, v in outer.items():
                for x, y in v.items():
                    if v['Last User'] == ctx.author.name and v['Status'] and v['Username'] != username:
                        await ctx.send(f"You can't use two accounts, please update the status of {v['Username']}")
                        return
            for k, v in outer.items():
                for x, y in v.items():
                    if y == username:
                        if  v['Status'] == True:
                            v['Status'] = False
                        else:
                            v['Status'] = True
                        v['Last User'] = ctx.author.name
                        cogs._json.write_json(outer, "smurfs")
                        if v['Status'] == False:
                            await ctx.send(f"{username} is no longer in use")
                        else:
                            await ctx.send(f"{username} is now in use")
                        return
            await ctx.send(f"{username} does not exist")


    #Finds all accounts with the wanted rank
    @commands.command(name='ssrank')
    async def _sranksearch(self, ctx, rank):
        if smurfchannelcheck(ctx.channel.id):
            if not any(i.isdigit() for i in rank):
                found = False
                rank = rank.upper()
                for k, v in outer.items():
                    for x, y in v.items():
                        if y == rank:
                            await ctx.send(f"```Username: {v['Username']}\nPassword: {v['Password']}\nRank: {v['Rank']} {v['Rank Number']}\nStatus: {v['Status']}\nLast User: {v['Last User']}```")
                            found = True
                if not found:
                    await ctx.send(f"No accounts found in {rank}")
            else:
                await ctx.send(f"Invalid Rank Format")


    #Finds the account with the wanted username
    @commands.command(name='ssusername')
    async def _susernamesearch(self, ctx, username):
        if smurfchannelcheck(ctx.channel.id):
            for k, v in outer.items():
                for x, y in v.items():
                    if y == username:
                        if v['Status']:
                            status = "In Use"
                        else:
                            status = "Not In Use"
                        await ctx.send(f"```Username: {v['Username']}\nPassword: {v['Password']}\nRank: {v['Rank']} {v['Rank Number']}\nStatus: {v['Status']}\nLast User: {v['Last User']}```")
                        return
            await ctx.send(f"{username} was not found")


    #Prints every account in the database
    @commands.command(name='sprint')
    @commands.cooldown(1,10, commands.BucketType.guild)
    async def _sprint(self, ctx):
        if smurfchannelcheck(ctx.channel.id):
            for k, v in outer.items():
                if v['Status']:
                    status = "In Use"
                else:
                    status = "Not In Use"
                await ctx.send(f"```Username: {v['Username']}\nPassword: {v['Password']}\nRank: {v['Rank']} {v['Rank Number']}\nStatus: {status}\nLast User: {v['Last User']}```")


    #Clears the entire list (ONLY FOR BOT OWNER)
    @commands.command(name='sclear')
    @commands.is_owner()
    async def _sclear(self, ctx):
        outer.clear()
        cogs._json.write_json(outer, "smurfs")
        await ctx.send(f"List Cleared")

def setup(bot):
    bot.add_cog(Smurf(bot))