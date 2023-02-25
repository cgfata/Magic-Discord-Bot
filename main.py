import mysql.connector
import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from database import start_database,prompt_user_updatecards

intents = discord.Intents.all()

client = commands.Bot(command_prefix='$', intents=intents)

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')

# Create tables to import users, and cards
db = mysql.connector.connect(
    host=MAGIC_INVENTORY_HOST,
    user=MAGIC_INVENTORY_USER,
    passwd=MAGIC_INVENTORY_PASSWORD,
    database=MAGIC_INVENTORY_DATABASE
)

mycursor = db.cursor()


def is_was_me_GIO(ctx):
    return ctx.author.id == 78717168631427072

def right_channel(ctx):
    return ctx.channel.id == 881395247236649071

@client.command()
@commands.check(is_was_me_GIO)
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')

@client.command()
@commands.check(is_was_me_GIO)
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')

@client.command()
@commands.check(is_was_me_GIO)
async def reload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded {extension}')


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    await load()
    await client.start(BOT_TOKEN)

##Prints in python bot is read, and imports users information when restarts.
@client.event
async def on_ready():
    await start_database()
    await prompt_user_updatecards()
    await client.change_presence(activity=discord.Game('Ready to Pull Magic Cards'))
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            discordmembers = ('("{}","{}"),'.format(member, member.id))
            serverinfo = (f'INSERT INTO discordserver (discordid, serverid, active) SELECT * FROM (SELECT {member.id} AS discordid, {member.guild.id} AS serverid, 1 AS active ) AS TEMP WHERE NOT EXISTS ( SELECT discordid, serverid FROM discordserver WHERE discordid = {member.id} AND serverid = {member.guild.id}) limit 1;')
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
        print(f'Users have been imported! {guild.name}')

    global ready
    print("Bot is ready!")


##Sends back messages for missed commands
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command does not exist. Please type $help for the list commands")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You forgot to put in the card name or forgot to type on or off for updating @")



asyncio.run(main())
