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

db = mysql.connector.connect(
        host=MAGIC_INVENTORY_HOST,
        user=MAGIC_INVENTORY_USER,
        passwd=MAGIC_INVENTORY_PASSWORD,
        database=MAGIC_INVENTORY_DATABASE
    )
mycursor = db.cursor()

class events(commands.Cog):

    def __init__(self,client):
        self.client = client

    ## The events below will update the database when a user joins and if they leave set active to 0
    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = mysql.connector.connect(
            host=MAGIC_INVENTORY_HOST,
            user=MAGIC_INVENTORY_USER,
            passwd=MAGIC_INVENTORY_PASSWORD,
            database=MAGIC_INVENTORY_DATABASE
        )
        mycursor = db.cursor()
        authname = str(member)
        authorid = str(member.id)
        authserverid = str(member.guild.id)
        mycursor.execute(
            f'SELECT u.discordid, s.serverid, s.active FROM discorduser u LEFT JOIN discordserver s ON u.discordid = s.discordid WHERE s.serverid = "{authserverid}" AND u.discordid = "{authorid}" AND s.active = 0')
        result = mycursor.fetchall()
        if authorid in str(result):
            mycursor.execute(f'UPDATE discorduser SET name = "{authname}" WHERE discordid = "{authorid}"')
            db.commit()
            mycursor.execute(
                f'UPDATE discordserver SET active = 1 WHERE serverid = "{authserverid}" AND discordid = "{authorid}"')
            db.commit()
            print(f'{member} has been set to active')
        else:
            mycursor.execute(f'INSERT IGNORE INTO discorduser (discordid, name) VALUES("{authorid}","{authname}")')
            db.commit()
            mycursor.execute(
                f'INSERT INTO discordserver (discordid, serverid, active) VALUES ("{authorid}","{authserverid}",1)')
            db.commit()
            print(f'{member} has been inserted')
        mycursor.close()

    ##event that when a user changers their discord name it will update the database
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        db = mysql.connector.connect(
            host=MAGIC_INVENTORY_HOST,
            user=MAGIC_INVENTORY_USER,
            passwd=MAGIC_INVENTORY_PASSWORD,
            database=MAGIC_INVENTORY_DATABASE
        )
        mycursor = db.cursor()
        beforeusername = str(before.name)
        afterusernanme = str(after.name)
        afterdiscriminator = str(after.discriminator)
        ID = str(before.id)
        if beforeusername != afterusernanme:
            mycursor.execute(
                f'UPDATE discorduser SET name = "{afterusernanme + "#" + afterdiscriminator}" WHERE discordid = {ID}')
            db.commit()
            mycursor.close()
            print("Users name was updated in the database!")
        else:
            print("User name was not change")

    ##event where when a member leaves the server it sets them to inactive which will stop the system from sending out thier card inventory
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = mysql.connector.connect(
            host=MAGIC_INVENTORY_HOST,
            user=MAGIC_INVENTORY_USER,
            passwd=MAGIC_INVENTORY_PASSWORD,
            database=MAGIC_INVENTORY_DATABASE
        )
        mycursor = db.cursor()
        authorid = str(member.id)
        authserverid = str(member.guild.id)
        mycursor.execute(
            f'SELECT u.discordid, s.serverid, s.active FROM discorduser u LEFT JOIN discordserver s ON u.discordid = s.discordid WHERE s.serverid = "{authserverid}" AND u.discordid = "{authorid}" AND s.active = 1')
        result = mycursor.fetchall()
        if authorid in str(result):
            mycursor.execute(
                f'UPDATE discordserver SET active = 0 WHERE serverid = "{authserverid}" AND discordid = "{authorid}"')
            db.commit()
            print(f'{member} has been set to inactive')
        else:
            print(f'{member} has lefted and was not part of the database')
        mycursor.close()

    ##an event to pull all user information when joining the server
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async for member in guild.fetch_members(limit=None):
            discordmembers = ('("{}","{}"),'.format(member, member.id))
            serverinfo = (
                f'INSERT INTO discordserver (discordid, serverid, active) SELECT * FROM (SELECT {member.id} AS discordid, {member.guild.id} AS serverid, 1 AS active ) AS TEMP WHERE NOT EXISTS ( SELECT discordid, serverid FROM discordserver WHERE discordid = {member.id} AND serverid = {member.guild.id}) limit 1;')
            formemberquery = discordmembers[:-1]
            db = mysql.connector.connect(
                host=MAGIC_INVENTORY_HOST,
                user=MAGIC_INVENTORY_USER,
                passwd=MAGIC_INVENTORY_PASSWORD,
                database=MAGIC_INVENTORY_DATABASE
            )
            mycursor = db.cursor()
            mycursor.execute(f'INSERT IGNORE INTO discorduser (name,discordid) VALUES {formemberquery}')
            db.commit()
            mycursor.execute(serverinfo)
            db.commit()
        mycursor.close()
        print(f'Users have been imported!{guild.name}')

async def setup(client):
    await client.add_cog(events(client))