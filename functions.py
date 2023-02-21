import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')

def wantcardsuser (cardinventoryuser):
    db = mysql.connector.connect(
        host=MAGIC_INVENTORY_HOST,
        user=MAGIC_INVENTORY_USER,
        passwd=MAGIC_INVENTORY_PASSWORD,
        database=MAGIC_INVENTORY_DATABASE
    )
    mycursor = db.cursor()

    cardoutputname = cardnamecheckername(f'{cardinventoryuser}')
    newwantquery = (f'SELECT i.discordid AS usid, SUM(i.count) AS count, i.name AS magicname, d.name AS uname FROM inventory i JOIN discorduser d ON i.discordid = d.discordid WHERE i.name="{cardoutputname}" GROUP BY i.discordid, i.name, d.name')
    mycursor.execute(newwantquery)
    for (usid,count,magicname, uname) in mycursor:
        return ("<@!{}> has {} {}".format(usid, count, magicname))
    mycursor.close()


def cardnamechecker (cardbeingchecked):
    db = mysql.connector.connect(
        host=MAGIC_INVENTORY_HOST,
        user=MAGIC_INVENTORY_USER,
        passwd=MAGIC_INVENTORY_PASSWORD,
        database=MAGIC_INVENTORY_DATABASE
    )
    mycursor = db.cursor()

    checkerquery = (f'SELECT name,uuid FROM cards WHERE name="{cardbeingchecked}" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    checkerquerydoublefacefront = (f'SELECT name, uuid FROM cards WHERE name LIKE "{cardbeingchecked} //%" AND side= "a" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    checkerquerydoublefaceback = (f'SELECT name, uuid FROM cards WHERE name LIKE "%// {cardbeingchecked}" AND side= "b" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    mycursor.execute(checkerquery)
    for (name,uuid) in mycursor:
        return (str(uuid))
    mycursor.execute(checkerquerydoublefacefront)
    for (name,uuid) in mycursor:
        return (str(uuid))
    mycursor.execute(checkerquerydoublefaceback)
    for (name,uuid) in mycursor:
        return (str(uuid))
    mycursor.close()

def cardnamecheckername(cardbeingchecked):
    db = mysql.connector.connect(
        host=MAGIC_INVENTORY_HOST,
        user=MAGIC_INVENTORY_USER,
        passwd=MAGIC_INVENTORY_PASSWORD,
        database=MAGIC_INVENTORY_DATABASE
    )
    mycursor = db.cursor()

    checkerquery = (
        f'SELECT name,uuid FROM cards WHERE name="{cardbeingchecked}" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    checkerquerydoublefacefront = (
        f'SELECT name, uuid FROM cards WHERE name LIKE "{cardbeingchecked} //%" AND side= "a" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    checkerquerydoublefaceback = (
        f'SELECT name, uuid FROM cards WHERE name LIKE "%// {cardbeingchecked}" AND side= "b" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    mycursor.execute(checkerquery)
    for (name, uuid) in mycursor:
        return (str(name))
    mycursor.execute(checkerquerydoublefacefront)
    for (name, uuid) in mycursor:
        return (str(name))
    mycursor.execute(checkerquerydoublefaceback)
    for (name, uuid) in mycursor:
        return (str(name))
    mycursor.close()


##This def will pull out Card Name, Manacost, Type, Text, And power and toughness.
##If no Manacost it will leave that out in the return
##If no power it will leave that out in the return
##if both power and manacost are not there then it will not return either
def cardinfo (info):
    db = mysql.connector.connect(
        host=MAGIC_INVENTORY_HOST,
        user=MAGIC_INVENTORY_USER,
        passwd=MAGIC_INVENTORY_PASSWORD,
        database=MAGIC_INVENTORY_DATABASE
    )
    mycursor = db.cursor()

    infoquery = (f'SELECT distinct name,manaCost,type,text,power,toughness,loyalty FROM cards WHERE uuid="{info}"')
    mycursor.execute(infoquery)
    for (name, manaCost, type, text,power,toughness,loyalty) in mycursor:
        if "None" in str(loyalty):
            if "None" in str (manaCost) and "None" in str (power):
                return ("{}\n\n{}\n\n{}".format(name,type,text,power,toughness))
            elif "None" in str (power):
                return ("{} {}\n\n{}\n\n{}".format(name, manaCost, type, text, power, toughness))
            elif "None" in str (manaCost):
                return ("{}\n\n{}\n\n{}\n\nstats: {}/{}".format(name, type, text, power, toughness))
            else:
                return ("{} {}\n\n{}\n\n{}\n\nStats: {}/{}".format(name,manaCost,type,text,power,toughness))
        else:
            return ("{} {}\n\n{}\n\n{}\n\nLoyalty: {}".format(name,manaCost,type,text,loyalty))
    mycursor.close()