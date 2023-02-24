from discord.ext import commands
from functions import  cardnamechecker, cardinfo, send_card_embed


class scry(commands.Cog):

    def __init__(self,client):
        self.client = client

    #commands
    @commands.command(brief='Card info in text format')
    async def scrytext(self, ctx, *, cardwanted):
        cardoutputname = await cardnamechecker(f'{cardwanted}')
        if "}" in str(f'{cardwanted}') or "{" in str(f'{cardwanted}'):
            await ctx.send('Hey now. You stop that!')
        elif "None" in str(cardoutputname):
            await ctx.send('The card name is incorrect')
        else:
            await ctx.send(await cardinfo(f'{cardoutputname}'))

    @commands.command(brief='Card info and picture of the card')
    async def scry(self, ctx, *, cardembed):
        cardoutputuuid = await cardnamechecker(f'{cardembed}')
        if "}" in str(f'{cardembed}') or "{" in str(f'{cardembed}'):
            await ctx.send('Hey now. You stop that!')
        elif "None" in str(cardoutputuuid):
            await ctx.send('The card name is incorrect')
        else:
            query = (
            f'SELECT name, manaCost,type,text,power,toughness,scryfallId,loyalty,side FROM cards WHERE uuid="{cardoutputuuid}" AND scryfallId is NOT NULL ORDER BY RAND() LIMIT 1')
        messege = await send_card_embed(ctx, query)
        await messege


    @commands.command(brief='What will you draw off the top of your deck?')
    async def topdeck(self, ctx):
        # so Lorenz only gets the power 9!
        if ctx.author.id == 147917366620192768:
            query = (
                f'SELECT name, manaCost,type,text,power,toughness,scryfallId,loyalty,side FROM cards Where scryfallId is NOT NULL AND (name = "Ancestral Recall" OR name = "Black Lotus" OR name = "Mox Emerald" OR name = "Mox Jet" OR name = "Mox Pearl" OR name = "Mox Ruby" OR name = "Mox Sapphire" OR name = "Timetwister" OR name = "Time Walk") ORDER BY RAND() LIMIT 1')

        else:
            query = (
                f'SELECT name, manaCost,type,text,power,toughness,scryfallId,loyalty,side FROM cards Where scryfallId is NOT NUll ORDER BY RAND() LIMIT 1')
        messege = await send_card_embed(ctx, query)
        await messege

async def setup(client):
    await client.add_cog(scry(client))

