import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import errorcode
from sqlalchemy import create_engine
from functions import updatecarddatabase

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')

db_info={
    "host": MAGIC_INVENTORY_HOST,
    "user": MAGIC_INVENTORY_USER,
    "passwd":MAGIC_INVENTORY_PASSWORD,
    "database":MAGIC_INVENTORY_DATABASE
}

# Create tables to import users, and cards
db = mysql.connector.connect(
    host=MAGIC_INVENTORY_HOST,
    user=MAGIC_INVENTORY_USER,
    passwd=MAGIC_INVENTORY_PASSWORD,
    database=MAGIC_INVENTORY_DATABASE
)

mycursor = db.cursor()

url = f'mysql+pymysql://{MAGIC_INVENTORY_USER}:{MAGIC_INVENTORY_PASSWORD}@{MAGIC_INVENTORY_HOST}/{MAGIC_INVENTORY_DATABASE}'
engine = create_engine(url)


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

TABLES['inventory'] = (
"CREATE TABLE `inventory` ("
  "`id` int NOT NULL AUTO_INCREMENT,"
  "`count` int DEFAULT NULL,"
  "`name` varchar(255) NOT NULL,"
  "`edition` varchar(255) NOT NULL,"
  "`cardnumber` int NOT NULL,"
  "`foil` varchar(4) DEFAULT NULL,"
  "`discordid` varchar(255) DEFAULT NULL,"
  "PRIMARY KEY (`id`),"
  "KEY `discordid_idx` (`discordid`),"
  "CONSTRAINT `discordid` FOREIGN KEY (`discordid`) REFERENCES `discorduser` (`discordid`)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
)

TABLES['user'] = (
"CREATE TABLE `user` ("
  "`id` int NOT NULL AUTO_INCREMENT,"
  "`email` varchar(150) DEFAULT NULL,"
  "`password` varchar(150) DEFAULT NULL,"
  "`first_name` varchar(150) DEFAULT NULL,"
  "`discordid` varchar(255) DEFAULT NULL,"
  "PRIMARY KEY (`id`),"
  "UNIQUE KEY `email` (`email`),"
  "UNIQUE KEY `discordid` (`discordid`)"
") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"
)


def create_database(mycursor):
    try:
        mycursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MAGIC_INVENTORY_DATABASE))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

async def start_database():
    db = mysql.connector.connect(
        host=MAGIC_INVENTORY_HOST,
        user=MAGIC_INVENTORY_USER,
        passwd=MAGIC_INVENTORY_PASSWORD,
        database=MAGIC_INVENTORY_DATABASE
    )

    mycursor = db.cursor()
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
    db.close()

async def prompt_user_updatecards():
    while True:
        user_input = input("Do you want to execute this command? (Y/N): ")

        if user_input.lower() == "y":
            await updatecarddatabase()
            break
        elif user_input.lower() == "n":
            print("Command not executed.")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")