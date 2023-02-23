import mysql.connector
import os
import discord
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')

def emojimana(ctx, text):
    mana0 = discord.utils.get(ctx.bot.emojis, name="mana0")
    mana1 = discord.utils.get(ctx.bot.emojis, name="mana1")
    mana10 = discord.utils.get(ctx.bot.emojis, name="mana10")
    mana11 = discord.utils.get(ctx.bot.emojis, name="mana11")
    mana12 = discord.utils.get(ctx.bot.emojis, name="mana12")
    mana13 = discord.utils.get(ctx.bot.emojis, name="mana13")
    mana14 = discord.utils.get(ctx.bot.emojis, name="mana14")
    mana15 = discord.utils.get(ctx.bot.emojis, name="mana15")
    mana16 = discord.utils.get(ctx.bot.emojis, name="mana16")
    mana2 = discord.utils.get(ctx.bot.emojis, name="mana2")
    mana20 = discord.utils.get(ctx.bot.emojis, name="mana20")
    mana2b = discord.utils.get(ctx.bot.emojis, name="mana2b")
    mana2g = discord.utils.get(ctx.bot.emojis, name="mana2g")
    mana2r = discord.utils.get(ctx.bot.emojis, name="mana2r")
    mana2u = discord.utils.get(ctx.bot.emojis, name="mana2u")
    mana2w = discord.utils.get(ctx.bot.emojis, name="mana2w")
    mana3 = discord.utils.get(ctx.bot.emojis, name="mana3")
    mana4 = discord.utils.get(ctx.bot.emojis, name="mana4")
    mana5 = discord.utils.get(ctx.bot.emojis, name="mana5")
    mana6 = discord.utils.get(ctx.bot.emojis, name="mana6")
    mana7 = discord.utils.get(ctx.bot.emojis, name="mana7")
    mana8 = discord.utils.get(ctx.bot.emojis, name="mana8")
    mana9 = discord.utils.get(ctx.bot.emojis, name="mana9")
    manaa = discord.utils.get(ctx.bot.emojis, name="manaa")
    manab = discord.utils.get(ctx.bot.emojis, name="manab")
    manabg = discord.utils.get(ctx.bot.emojis, name="manabg")
    manabgp = discord.utils.get(ctx.bot.emojis, name="manabgp")
    manabp = discord.utils.get(ctx.bot.emojis, name="manabp")
    manabr = discord.utils.get(ctx.bot.emojis, name="manabr")
    manabrp = discord.utils.get(ctx.bot.emojis, name="manabrp")
    manac = discord.utils.get(ctx.bot.emojis, name="manac")
    manachaos = discord.utils.get(ctx.bot.emojis, name="manachaos")
    manae = discord.utils.get(ctx.bot.emojis, name="manae")
    manag = discord.utils.get(ctx.bot.emojis, name="manag")
    managp = discord.utils.get(ctx.bot.emojis, name="managp")
    managu = discord.utils.get(ctx.bot.emojis, name="managu")
    managup = discord.utils.get(ctx.bot.emojis, name="managup")
    managw = discord.utils.get(ctx.bot.emojis, name="managw")
    managwp = discord.utils.get(ctx.bot.emojis, name="managwp")
    manapw = discord.utils.get(ctx.bot.emojis, name="manapw")
    manaq = discord.utils.get(ctx.bot.emojis, name="manaq")
    manar = discord.utils.get(ctx.bot.emojis, name="manar")
    manarg = discord.utils.get(ctx.bot.emojis, name="manarg")
    manargp = discord.utils.get(ctx.bot.emojis, name="manargp")
    manarp = discord.utils.get(ctx.bot.emojis, name="manarp")
    manarw = discord.utils.get(ctx.bot.emojis, name="manarw")
    manarwp = discord.utils.get(ctx.bot.emojis, name="manarwp")
    manas = discord.utils.get(ctx.bot.emojis, name="manas")
    manat = discord.utils.get(ctx.bot.emojis, name="manat")
    manau = discord.utils.get(ctx.bot.emojis, name="manau")
    manaub = discord.utils.get(ctx.bot.emojis, name="manaub")
    manaubp = discord.utils.get(ctx.bot.emojis, name="manaubp")
    manaup = discord.utils.get(ctx.bot.emojis, name="manaup")
    manaur = discord.utils.get(ctx.bot.emojis, name="manaur")
    manaurp = discord.utils.get(ctx.bot.emojis, name="manaurp")
    manaw = discord.utils.get(ctx.bot.emojis, name="manaw")
    manawb = discord.utils.get(ctx.bot.emojis, name="manawb")
    manawbp = discord.utils.get(ctx.bot.emojis, name="manawbp")
    manawp = discord.utils.get(ctx.bot.emojis, name="manawp")
    manawu = discord.utils.get(ctx.bot.emojis, name="manawu")
    manawup = discord.utils.get(ctx.bot.emojis, name="manawup")
    manax = discord.utils.get(ctx.bot.emojis, name="manax")
    emoji_map = {
        "{0}": mana0,
        "{1}": mana1,
        "{10}": mana10,
        "{11}": mana11,
        "{12}": mana12,
        "{13}": mana13,
        "{14}": mana14,
        "{15}": mana15,
        "{16}": mana16,
        "{2}": mana2,
        "{20}": mana20,
        "{2/B}": mana2b,
        "{2/G}": mana2g,
        "{2/R}": mana2r,
        "{2/U}": mana2u,
        "{2/W}": mana2w,
        "{3}": mana3,
        "{4}": mana4,
        "{5}": mana5,
        "{6}": mana6,
        "{7}": mana7,
        "{8}": mana8,
        "{9}": mana9,
        "{A}": manaa,
        "{B}": manab,
        "{B/G}": manabg,
        "{B/G/P}": manabgp,
        "{B/P}": manabp,
        "{B/R}": manabr,
        "{B/R/P}": manabrp,
        "{C}": manac,
        "{CHAOS}": manachaos,
        "{E}": manae,
        "{G}": manag,
        "{G/P}": managp,
        "{G/U}": managu,
        "{G/U/P}": managup,
        "{G/W}": managw,
        "{G/W/P}": managwp,
        "{PW}": manapw,
        "{Q}": manaq,
        "{R}": manar,
        "{R/G}": manarg,
        "{R/G/P}": manargp,
        "{R/P}": manarp,
        "{R/W}": manarw,
        "{R/W/P}": manarwp,
        "{S}": manas,
        "{T}": manat,
        "{U}": manau,
        "{U/B}": manaub,
        "{U/B/P}": manaubp,
        "{U/P}": manaup,
        "{U/R}": manaur,
        "{U/R/P}": manaurp,
        "{W}": manaw,
        "{W/B}": manawb,
        "{W/B/P}": manawbp,
        "{W/P}": manawp,
        "{W/U}": manawu,
        "{W/U/P}": manawup,
        "{X}": manax,
    }
    for placeholder, emoji in emoji_map.items():
        text = text.replace(placeholder, str(emoji))
    return text


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