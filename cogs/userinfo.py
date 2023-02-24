import mysql.connector
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')



class userinfo(commands.Cog):

    def __init__(self,client):
        self.client = client

    # commands
    @commands.command(brief='Will update your discord ID and Discord Name')
    async def userupdate(self, ctx):
        db = mysql.connector.connect(
            host=MAGIC_INVENTORY_HOST,
            user=MAGIC_INVENTORY_USER,
            passwd=MAGIC_INVENTORY_PASSWORD,
            database=MAGIC_INVENTORY_DATABASE
        )
        mycursor = db.cursor()
        authorid = str(ctx.author.id)
        authname = str(ctx.author)
        serverid = str(ctx.guild.id)
        mycursor.execute(
            f'SELECT u.discordid, s.serverid FROM discorduser u LEFT JOIN discordserver s ON u.discordid = s.discordid WHERE s.serverid = "{serverid}" AND u.discordid = "{authorid}"')
        result = mycursor.fetchall()
        if authorid in str(result):
            mycursor.execute(f'UPDATE discorduser SET name = "{authname}" WHERE discordid = {authorid}')
            db.commit()
            await ctx.send("Your user name has been updated into the magic database")
        else:
            mycursor.execute(f'INSERT IGNORE INTO discorduser (discordid, name) VALUES("{authorid}","{authname}")')
            db.commit()
            mycursor.execute(
                f'INSERT INTO discordserver (discordid, serverid, active) VALUES ("{authorid}","{serverid}",1)')
            db.commit()
            await ctx.send("Welcome! Your discord information has been uploaded to the magic database")
        mycursor.close()

    ##command to turn on or off the @ when someone types want card command
    @commands.command(brief='Type on or off after the command to be @ when someone does the want command')
    async def updateat(self, ctx, *, at):
        if "}" in str(at) or "{" in str(at):
            await ctx.send("Hey stop that!")
        elif "on" in str.lower(at):
            db = mysql.connector.connect(
                host=MAGIC_INVENTORY_HOST,
                user=MAGIC_INVENTORY_USER,
                passwd=MAGIC_INVENTORY_PASSWORD,
                database=MAGIC_INVENTORY_DATABASE
            )
            mycursor = db.cursor()
            mycursor.execute(
                f'Update discordserver set at=1 WHERE discordid = {ctx.author.id} AND serverid = {ctx.guild.id}')
            db.commit()
            await ctx.send('You will now be @ when people are looking for cards')
        elif "off" in str.lower(at):
            db = mysql.connector.connect(
                host=MAGIC_INVENTORY_HOST,
                user=MAGIC_INVENTORY_USER,
                passwd=MAGIC_INVENTORY_PASSWORD,
                database=MAGIC_INVENTORY_DATABASE
            )
            mycursor = db.cursor()
            mycursor.execute(
                f'Update discordserver set at=0 WHERE discordid = {ctx.author.id} AND serverid = {ctx.guild.id}')
            db.commit()
            await ctx.send('You will be no longer @ when people are looking for cards')
        else:
            await ctx.send(
                "Ops. It seems you missed typing on or off. Please type on to turn on @ and off to turn it off")

async def setup(client):
    await client.add_cog(userinfo(client))