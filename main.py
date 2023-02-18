import mysql.connector
import discord
import os
import asyncio
import zipfile
import requests
import pandas as pd
from discord.ext import commands
from dotenv import load_dotenv
from mysql.connector import errorcode
from sqlalchemy import create_engine

intents = discord.Intents.all()

client = commands.Bot(command_prefix='$', intents=intents)

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')

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
    await client.change_presence(activity=discord.Game('Ready to Pull Magic Cards'))
    #Create tables to import users, and cards
    db = mysql.connector.connect(
        host=MAGIC_INVENTORY_HOST,
        user=MAGIC_INVENTORY_USER,
        passwd=MAGIC_INVENTORY_PASSWORD,
        database=MAGIC_INVENTORY_DATABASE
    )

    mycursor = db.cursor()

    TABLES = {}

    TABLES['discorduser'] = (
        "CREATE TABLE `discorduser` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `discordid` varchar(255) NOT NULL,"
        "  `name` varchar(255) NOT NULL,"
        "  PRIMARY KEY (`id`),"
        "  UNIQUE KEY `discordid_UNIQUE` (`discordid`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")

    TABLES['discordserver'] = (
        "CREATE TABLE `discordserver` ("
        "  `id` int NOT NULL AUTO_INCREMENT,"
        "  `discordid` varchar(255) NOT NULL,"
        "  `serverid` varchar(255) NOT NULL,"
        "  `active` int NOT NULL,"
        "  `at` int NOT NULL DEFAULT '0',"
        "  PRIMARY KEY (`id`),"
        "  KEY `usertoserver_idx` (`discordid`),"
        "  CONSTRAINT `usertoserver` FOREIGN KEY (`discordid`) REFERENCES `discorduser` (`discordid`)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")

    TABLES['cards'] = (
        "CREATE TABLE `cards` ("
        "  `index` bigint DEFAULT NULL,"
        "  `id` bigint DEFAULT NULL,"
        "  `artist` text,"
        "`asciiName` text,"
        "`attractionLights` double DEFAULT NULL,"
        "`availability` text,"
        "`boosterTypes` text,"
        "`borderColor` text,"
        "`cardKingdomEtchedId` double DEFAULT NULL,"
        "`cardKingdomFoilId` double DEFAULT NULL,"
        "`cardKingdomId` double DEFAULT NULL,"
        " `cardParts` text,"
        "`cardsphereId` double DEFAULT NULL,"
        "`colorIdentity` text,"
        "`colorIndicator` text,"
        "`colors` text,"
        "`convertedManaCost` double DEFAULT NULL,"
        "`duelDeck` text,"
        "`edhrecRank` double DEFAULT NULL,"
        "`edhrecSaltiness` double DEFAULT NULL,"
        "`faceConvertedManaCost` double DEFAULT NULL,"
        "`faceFlavorName` text,"
        "`faceManaValue` double DEFAULT NULL,"
        "`faceName` text,"
        "`finishes` text,"
        "`flavorName` text,"
        "`flavorText` text,"
        "`frameEffects` text,"
        "`frameVersion` text,"
        "`hand` double DEFAULT NULL,"
        "`hasAlternativeDeckLimit` bigint DEFAULT NULL,"
        "`hasContentWarning` bigint DEFAULT NULL,"
        "`hasFoil` bigint DEFAULT NULL,"
        "`hasNonFoil` bigint DEFAULT NULL,"
        "`isAlternative` bigint DEFAULT NULL,"
        "`isFullArt` bigint DEFAULT NULL,"
        "`isFunny` bigint DEFAULT NULL,"
        "`isOnlineOnly` bigint DEFAULT NULL,"
        "`isOversized` bigint DEFAULT NULL,"
        "`isPromo` bigint DEFAULT NULL,"
        "`isRebalanced` bigint DEFAULT NULL,"
        "`isReprint` bigint DEFAULT NULL,"
        "`isReserved` bigint DEFAULT NULL,"
        "`isStarter` bigint DEFAULT NULL,"
        "`isStorySpotlight` bigint DEFAULT NULL,"
        "`isTextless` bigint DEFAULT NULL,"
        "`isTimeshifted` bigint DEFAULT NULL,"
        "`keywords` text,"
        "`language` text,"
        "`layout` text,"
        "`leadershipSkills` text,"
        "`life` double DEFAULT NULL,"
        "`loyalty` text,"
        "`manaCost` text,"
        "`manaValue` double DEFAULT NULL,"
        "`mcmId` double DEFAULT NULL,"
        "`mcmMetaId` double DEFAULT NULL,"
        "`mtgArenaId` double DEFAULT NULL,"
        "`mtgjsonFoilVersionId` text,"
        "`mtgjsonNonFoilVersionId` text,"
        "`mtgjsonV4Id` text,"
        "`mtgoFoilId` double DEFAULT NULL,"
        "`mtgoId` double DEFAULT NULL,"
        "`multiverseId` double DEFAULT NULL,"
        "`name` text,"
        "`number` text,"
        "`originalPrintings` text,"
        "`originalReleaseDate` text,"
        "`originalText` text,"
        "`originalType` text,"
        "`otherFaceIds` text,"
        "`power` text,"
        "`printings` text,"
        "`promoTypes` text,"
        "`purchaseUrls` text,"
        "`rarity` text,"
        "`rebalancedPrintings` text,"
        "`relatedCards` text,"
        "`scryfallId` text,"
        "`scryfallIllustrationId` text,"
        "`scryfallOracleId` text,"
        "`securityStamp` text,"
        "`setCode` text,"
        "`side` text,"
        "`signature` text,"
        "`subsets` text,"
        "`subtypes` text,"
        "`supertypes` text,"
        "`tcgplayerEtchedProductId` double DEFAULT NULL,"
        "`tcgplayerProductId` double DEFAULT NULL,"
        "`text` text,"
        "`toughness` text,"
        "`type` text,"
        "`types` text,"
        "`uuid` text,"
        "`variations` text,"
        "`watermark` text"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4")

    def create_database(mycursor):
        try:
            mycursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MAGIC_INVENTORY_DATABASE))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    try:
        mycursor.execute("USE {}".format(MAGIC_INVENTORY_DATABASE))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(MAGIC_INVENTORY_DATABASE))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(mycursor)
            print("Database {} created successfully.".format(MAGIC_INVENTORY_DATABASE))
            db.database = MAGIC_INVENTORY_DATABASE
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            mycursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    mycursor.close()

    #Will download the CSV from mtgjson to import cards that are missing
    url = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD}@{MAGIC_INVENTORY_HOST}/{MAGIC_INVENTORY_DATABASE}'
    engine = create_engine(url)
    print('Script has started and starting to download the file')

    downloadurl = 'https://mtgjson.com/api/v5/csv/cards.csv.zip'

    req = requests.get(downloadurl)

    filename = req.url[downloadurl.rfind('/') + 1:]
    unzfilename = filename[:-4]

    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
        print("File has been Downloaded")

    with zipfile.ZipFile(filename, 'r') as filename:
        filename.extract(unzfilename)
        print("File has been unzipped")

    csvdf = pd.read_csv(unzfilename, header=0, index_col=False, low_memory=False, delimiter=',')

    with engine.begin() as connection:
        sqldf = pd.read_sql_table('cards', con=connection)
        dftoinsert = pd.concat([csvdf, sqldf]).drop_duplicates(subset=['id'], keep=False)
        print("Reading Database to check dublicates")
        dftoinsert.to_sql("cards", con=connection, if_exists='append', index=False)
        print("Inserted Cards")

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
