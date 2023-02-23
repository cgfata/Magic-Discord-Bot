import mysql.connector
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from functions import wantcardsuser, cardnamechecker, cardnamecheckername,cardinfo, emojimana

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')


class scry(commands.Cog):

    def __init__(self,client):
        self.client = client

    #commands
    @commands.command(brief='Card info in text format')
    async def scrytext(self, ctx, *, cardwanted):
        cardoutputname = cardnamechecker(f'{cardwanted}')
        if "}" in str(f'{cardwanted}') or "{" in str(f'{cardwanted}'):
            await ctx.send('Hey now. You stop that!')
        elif "None" in str(cardoutputname):
            await ctx.send('The card name is incorrect')
        else:
            await ctx.send(cardinfo(f'{cardoutputname}'))

    @commands.command(brief='Card info and picture of the card')
    async def scry(self, ctx, *, cardembed):
        cardoutputuuid = cardnamechecker(f'{cardembed}')
        if "}" in str(f'{cardembed}') or "{" in str(f'{cardembed}'):
            await ctx.send('Hey now. You stop that!')
        elif "None" in str(cardoutputuuid):
            await ctx.send('The card name is incorrect')
        else:
            db = mysql.connector.connect(
                host=MAGIC_INVENTORY_HOST,
                user=MAGIC_INVENTORY_USER,
                passwd=MAGIC_INVENTORY_PASSWORD,
                database=MAGIC_INVENTORY_DATABASE
            )
            mycursor = db.cursor()
            infoquery = (
                f'SELECT name, manaCost,type,text,power,toughness,scryfallId,loyalty,side FROM cards WHERE uuid="{cardoutputuuid}" AND scryfallId is NOT NULL ORDER BY RAND() LIMIT 1')
            mycursor.execute(infoquery)
            for (name, manaCost, type, text, power, toughness, scryfallId, loyalty, side) in mycursor:
                if "b" in str(side):
                    cardsideurl = "back"
                else:
                    cardsideurl = "front"
            mycursor.execute(infoquery)
            for (name, manaCost, type, text, power, toughness, scryfallId, loyalty, side) in mycursor:
                emoji_cost = emojimana(ctx,manaCost)
                emoji_text = emojimana(ctx,text)
                firstletterforurl = scryfallId[0]
                secondletterforurl = scryfallId[1]
                scryfallURL = f'https://c1.scryfall.com/file/scryfall-cards/large/{cardsideurl}/{firstletterforurl}/{secondletterforurl}/{scryfallId}.jpg'
                if "None" in str(scryfallId):
                    await ctx.send(
                        "The card does not have a picture in the database." + "\n\n" + cardinfo(f'{cardembed}'))
                elif "None" in str(loyalty):
                    if "None" in str(manaCost) and "None" in str(power):
                        embed = discord.Embed(
                            title=f'{name}',
                        )
                        embed.add_field(name='Type', value=f'{type}', inline=False)
                        embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                        embed.set_thumbnail(url=f'{scryfallURL}')
                        await ctx.send(embed=embed)
                    elif "None" in str(power):
                        embed = discord.Embed(
                            title=f'{name}          {emoji_cost}',
                        )
                        embed.add_field(name='Type', value=f'{type}', inline=False)
                        embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                        embed.set_thumbnail(url=f'{scryfallURL}')
                        await ctx.send(embed=embed)
                    elif "None" in str(manaCost):
                        embed = discord.Embed(
                            title=f'{name}',
                        )
                        embed.add_field(name='Type', value=f'{type}', inline=False)
                        embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                        embed.add_field(name="Stats", value=f'{power}/{toughness}', inline=True)
                        embed.set_thumbnail(url=f'{scryfallURL}')
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title=f'{name}          {emoji_cost}',
                        )
                        embed.add_field(name='Type', value=f'{type}', inline=False)
                        embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                        embed.add_field(name="Stats", value=f'{power}/{toughness}', inline=True)
                        embed.set_thumbnail(url=f'{scryfallURL}')
                        await ctx.send(embed=embed)
                elif "None" in str(manaCost):
                    embed = discord.Embed(
                        title=f'{name}',
                    )
                    embed.add_field(name='Type', value=f'{type}', inline=False)
                    embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                    embed.add_field(name="Loyalty", value=f'{loyalty}', inline=True)
                    embed.set_thumbnail(url=f'{scryfallURL}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f'{name}          {emoji_cost}',
                    )
                    embed.add_field(name='Type', value=f'{type}', inline=False)
                    embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                    embed.add_field(name="Loyalty", value=f'{loyalty}', inline=True)
                    embed.set_thumbnail(url=f'{scryfallURL}')
                    await ctx.send(embed=embed)
            mycursor.close()

    @commands.command(brief='What will you draw off the top of your deck?')
    async def topdeck(self, ctx):
        # so Lorenz only gets the power 9!
        if ctx.author.id == 147917366620192768:
            randominfoquery = (
                f'SELECT name, manaCost,type,text,power,toughness,scryfallId,loyalty FROM cards Where scryfallId is NOT NULL AND (name = "Ancestral Recall" OR name = "Black Lotus" OR name = "Mox Emerald" OR name = "Mox Jet" OR name = "Mox Pearl" OR name = "Mox Ruby" OR name = "Mox Sapphire" OR name = "Timetwister" OR name = "Time Walk") ORDER BY RAND() LIMIT 1')

        else:
            randominfoquery = (
                f'SELECT name, manaCost,type,text,power,toughness,scryfallId,loyalty FROM cards Where scryfallId is NOT NUll ORDER BY RAND() LIMIT 1')
        db = mysql.connector.connect(
            host=MAGIC_INVENTORY_HOST,
            user=MAGIC_INVENTORY_USER,
            passwd=MAGIC_INVENTORY_PASSWORD,
            database=MAGIC_INVENTORY_DATABASE
        )
        mycursor = db.cursor()
        mycursor.execute(randominfoquery)
        for (name, manaCost, type, text, power, toughness, scryfallId, loyalty) in mycursor:
            emoji_cost = emojimana(ctx, manaCost)
            emoji_text = emojimana(ctx, text)
            firstletterforurl = scryfallId[0]
            secondletterforurl = scryfallId[1]
            scryfallURL = f'https://c1.scryfall.com/file/scryfall-cards/large/front/{firstletterforurl}/{secondletterforurl}/{scryfallId}.jpg'
            if "None" in str(loyalty):
                if "None" in str(manaCost) and "None" in str(power):
                    embed = discord.Embed(
                        title=f'{name}',
                    )
                    embed.add_field(name='Type', value=f'{type}', inline=False)
                    embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                    embed.set_thumbnail(url=f'{scryfallURL}')
                    await ctx.send(embed=embed)
                elif "None" in str(power):
                    embed = discord.Embed(
                        title=f'{name}          {emoji_cost }',
                    )
                    embed.add_field(name='Type', value=f'{type}', inline=False)
                    embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                    embed.set_thumbnail(url=f'{scryfallURL}')
                    await ctx.send(embed=embed)
                elif "None" in str(manaCost):
                    embed = discord.Embed(
                        title=f'{name}',
                    )
                    embed.add_field(name='Type', value=f'{type}', inline=False)
                    embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                    embed.add_field(name="Stats", value=f'{power}/{toughness}', inline=True)
                    embed.set_thumbnail(url=f'{scryfallURL}')
                    await ctx.send(embed=embed)
                elif "None" in str(name):
                    await ctx.send("The card does not have a picture. Use command $text for the card")
                else:
                    embed = discord.Embed(
                        title=f'{name}          {emoji_cost}',
                    )
                    embed.add_field(name='Type', value=f'{type}', inline=False)
                    embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                    embed.add_field(name="Stats", value=f'{power}/{toughness}', inline=True)
                    embed.set_thumbnail(url=f'{scryfallURL}')
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f'{name}          {emoji_cost }',
                )
                embed.add_field(name='Type', value=f'{type}', inline=False)
                embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                embed.add_field(name="Loyalty", value=f'{loyalty}', inline=True)
                embed.set_thumbnail(url=f'{scryfallURL}')
                await ctx.send(embed=embed)
        mycursor.close()

async def setup(client):
    await client.add_cog(scry(client))

