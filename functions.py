import mysql.connector
import zipfile
import requests
import pandas as pd
import discord



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

async def send_card_embed(ctx,query):
    from database import db_info
    db = mysql.connector.connect(**db_info)
    mycursor = db.cursor()

    mycursor.execute(query)
    for (name, manaCost, type, text, power, toughness, scryfallId, loyalty, side) in mycursor:
        if "b" in str(side):
            cardsideurl = "back"
        else:
            cardsideurl = "front"
        if "None" in str(manaCost):
            emoji_text = emojimana(ctx, text)
        else:
            emoji_cost = emojimana(ctx, manaCost)
            emoji_text = emojimana(ctx, text)
        firstletterforurl = scryfallId[0]
        secondletterforurl = scryfallId[1]
        scryfallURL = f'https://c1.scryfall.com/file/scryfall-cards/large/{cardsideurl}/{firstletterforurl}/{secondletterforurl}/{scryfallId}.jpg'
        if "None" in str(loyalty):
            if "None" in str(manaCost) and "None" in str(power):
                embed = discord.Embed(
                    title=f'{name}',
                )
                embed.add_field(name='Type', value=f'{type}', inline=False)
                embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                embed.set_thumbnail(url=f'{scryfallURL}')
                return(ctx.send(embed=embed))
            elif "None" in str(power):
                embed = discord.Embed(
                    title=f'{name}          {emoji_cost }',
                )
                embed.add_field(name='Type', value=f'{type}', inline=False)
                embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                embed.set_thumbnail(url=f'{scryfallURL}')
                return(ctx.send(embed=embed))
            elif "None" in str(manaCost):
                embed = discord.Embed(
                    title=f'{name}',
                )
                embed.add_field(name='Type', value=f'{type}', inline=False)
                embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                embed.add_field(name="Stats", value=f'{power}/{toughness}', inline=True)
                embed.set_thumbnail(url=f'{scryfallURL}')
                return(ctx.send(embed=embed))
            elif "None" in str(name):
                return (ctx.send("The card does not have a picture. Use command $text for the card"))
            else:
                embed = discord.Embed(
                    title=f'{name}          {emoji_cost}',
                )
                embed.add_field(name='Type', value=f'{type}', inline=False)
                embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
                embed.add_field(name="Stats", value=f'{power}/{toughness}', inline=True)
                embed.set_thumbnail(url=f'{scryfallURL}')
                return(ctx.send(embed=embed))
        else:
            embed = discord.Embed(
                title=f'{name}          {emoji_cost }',
            )
            embed.add_field(name='Type', value=f'{type}', inline=False)
            embed.add_field(name="Text", value=f'{emoji_text}', inline=False)
            embed.add_field(name="Loyalty", value=f'{loyalty}', inline=True)
            embed.set_thumbnail(url=f'{scryfallURL}')
            return(ctx.send(embed=embed))
    mycursor.close()
    db.close()

async def wantcardsuser (card):
    from database import db_info
    db = mysql.connector.connect(**db_info)
    mycursor = db.cursor()

    newwantquery = (f'SELECT i.discordid AS usid, SUM(i.count) AS count, i.name AS magicname, d.name AS uname FROM inventory i JOIN discorduser d ON i.discordid = d.discordid WHERE i.name="{card}" GROUP BY i.discordid, i.name, d.name')
    mycursor.execute(newwantquery)
    for (usid,count,magicname, uname) in mycursor:
        return ("<@!{}> has {} {}".format(usid, count, magicname))
    mycursor.close()
    db.close()

async def cardnamechecker (card):
    from database import db_info
    db = mysql.connector.connect(**db_info)
    mycursor = db.cursor()

    checkerquery = (f'SELECT name,uuid FROM cards WHERE name="{card}" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    checkerquerydoublefacefront = (f'SELECT name, uuid FROM cards WHERE name LIKE "{card} //%" AND side= "a" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    checkerquerydoublefaceback = (f'SELECT name, uuid FROM cards WHERE name LIKE "%// {card}" AND side= "b" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
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
    db.close()

async def cardnamecheckername(card):
    from database import db_info
    db = mysql.connector.connect(**db_info)
    mycursor = db.cursor()

    checkerquery = (
        f'SELECT name,uuid FROM cards WHERE name="{card}" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    checkerquerydoublefacefront = (
        f'SELECT name, uuid FROM cards WHERE name LIKE "{card} //%" AND side= "a" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
    checkerquerydoublefaceback = (
        f'SELECT name, uuid FROM cards WHERE name LIKE "%// {card}" AND side= "b" AND type != "Vanguard" ORDER BY RAND() LIMIT 1')
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
    db.close()

##This def will pull out Card Name, Manacost, Type, Text, And power and toughness.
##If no Manacost it will leave that out in the return
##If no power it will leave that out in the return
##if both power and manacost are not there then it will not return either
async def cardinfo (card):
    from database import db_info
    db = mysql.connector.connect(**db_info)
    mycursor = db.cursor()

    infoquery = (f'SELECT distinct name,manaCost,type,text,power,toughness,loyalty FROM cards WHERE uuid="{card}"')
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
    db.close()

async def updatecarddatabase():
    from database import engine
    # Will download the CSV from mtgjson to import cards that are missing
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