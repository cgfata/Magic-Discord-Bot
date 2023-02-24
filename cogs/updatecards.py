from discord.ext import commands
from functions import updatecarddatabase


class updatecards(commands.Cog):

    def __init__(self,client):
        self.client = client


    #commands
    @commands.command(brief='Will update the card database')
    async def updatecards(self, ctx):
        await ctx.send("Downloading the most recent cards from MTGjson and updating the database")
        await updatecarddatabase()
        await ctx.send("Updated the card database!")

async def setup(client):
    await client.add_cog(updatecards(client))