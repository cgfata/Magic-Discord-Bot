import mysql.connector
import discord
import os
import time
import re
from discord.ext import commands
from dotenv import load_dotenv
from functions import wantcardsuser, cardnamechecker, cardnamecheckername,cardinfo

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')


class want(commands.Cog):

    def __init__(self,client):
        self.client = client

    #commands
    @commands.command(brief='Will @ People who have the card and how many')
    async def want(self, ctx, *, cardwanted):
        await ctx.send(f'looking up the users who have {cardwanted}......')
        if "}" in str(f'{cardwanted}') or "{" in str(f'{cardwanted}'):
            await ctx.send('Hey now. You stop that!')
        elif "None" in str(cardnamechecker(f'{cardwanted}')):
            await ctx.send('The card name is incorrect')
        elif "None" in str(wantcardsuser(f'{cardwanted}')):
            await ctx.send('No one has the card')
        else:
            db = mysql.connector.connect(
                host=MAGIC_INVENTORY_HOST,
                user=MAGIC_INVENTORY_USER,
                passwd=MAGIC_INVENTORY_PASSWORD,
                database=MAGIC_INVENTORY_DATABASE
            )
            mycursor = db.cursor()
            atcard = ""
            noatcard = ""
            guild = str(ctx.guild.id)
            cardoutputname = cardnamecheckername(f'{cardwanted}')
            mycursor.execute(
                f'SELECT i.discordid AS usid, SUM(i.count) AS count, i.name AS magicname FROM inventory i JOIN discorduser d ON i.discordid = d.discordid LEFT JOIN discordserver s ON i.discordid = s.discordid Where i.name = "{cardoutputname}" AND serverid = {guild} AND active = 1 AND at = 1 GROUP BY i.discordid')
            rows = mycursor.fetchall()
            for (usid, count, magicname) in rows:
                atcard += ("<@!{}> has {} {}\n".format(usid, count, magicname))
            mycursor.execute(
                f'SELECT d.name AS uname, SUM(i.count) AS count, i.name AS magicname FROM inventory i JOIN discorduser d ON i.discordid = d.discordid LEFT JOIN discordserver s ON i.discordid = s.discordid Where i.name = "{cardoutputname}" AND serverid = {guild} AND active = 1 AND at = 0 GROUP BY i.discordid')
            rows = mycursor.fetchall()
            for (uname, count, magicname) in rows:
                noatcard += ("{} has {} {}\n".format(uname, count, magicname))
            await ctx.send(
                f'<@!{ctx.author.id}> here are the users who have the card {cardwanted}:\n\n{atcard + noatcard}')
            mycursor.close()

    @commands.command(brief='Wll look up a mass import of who has the cards. ')
    async def masswant(self, ctx, *, cardwanted):
        cardsplit = (re.split("\n+", cardwanted))
        timeofsend = int(time.time())
        nonumber = ""
        lessthan10 = ""
        greaterthan10 = ""
        numbercheck = list(range(10))
        cardwantedlist = []
        if "}" in str(f'{cardwanted}') or "{" in str(f'{cardwanted}'):
            await ctx.send('Please remove { or } from your list!')
        else:
            await ctx.send('looking up the users who have cards from the list......')
            for x in cardsplit:
                if x[0] not in str(numbercheck):
                    nonumber += ('i.name = "{}" OR '.format(x))
                    cardwantedlist.append('{}'.format(x))
                elif x[0] == " ":
                    nonumber += ('i.name = "{}" OR '.format(x))
                    cardwantedlist.append('{}'.format(x))
                elif int(x[0] + x[1]) < 10:
                    lessthan10 += ('i.name = "{}" OR '.format(x[2:]))
                    cardwantedlist.append('{}'.format(x[2:]))
                else:
                    greaterthan10 += ('i.name = "{}" OR '.format(x[3:]))
                    cardwantedlist.append('{}'.format(x[3:]))
                whereintoquery = (nonumber + greaterthan10 + lessthan10)[:-3]
                db = mysql.connector.connect(
                    host=MAGIC_INVENTORY_HOST,
                    user=MAGIC_INVENTORY_USER,
                    passwd=MAGIC_INVENTORY_PASSWORD,
                    database=MAGIC_INVENTORY_DATABASE
                )
                mycursor = db.cursor()
                atcard = ""
                noatcard = ""
                currentuser = ""
                userlist = []
                cardlist = []
                guild = str(ctx.guild.id)
                mycursor.execute(
                    f'SELECT i.discordid AS usid, SUM(i.count) AS count, i.name AS magicname FROM inventory i JOIN discorduser d ON i.discordid = d.discordid LEFT JOIN discordserver s ON i.discordid = s.discordid WHERE ({whereintoquery}) AND serverid = {guild} AND active = 1 AND at = 1 GROUP BY i.discordid, i.name ORDER BY i.name')
                rows = mycursor.fetchall()
                for (usid, count, magicname) in rows:
                    if currentuser == "" or currentuser != usid:
                        currentuser = usid
                        userlist.append(currentuser)
                userlist = list(set(userlist))
                for user in userlist:
                    atcard += "<@!{}> ".format(user)
                mycursor.execute(
                    f'SELECT d.name AS uname, SUM(i.count) AS count, i.name AS magicname FROM inventory i JOIN discorduser d ON i.discordid = d.discordid LEFT JOIN discordserver s ON i.discordid = s.discordid WHERE ({whereintoquery}) AND serverid = {guild} AND active = 1 GROUP BY i.discordid, i.name ORDER BY i.name')
                rows = mycursor.fetchall()
                currentcard = ""
                for (uname, count, magicname) in rows:
                    if currentcard == "" or currentcard != magicname:
                        currentcard = magicname
                        cardlist.append(magicname)
                        noatcard += "\n{}: \n".format(currentcard)
                    noatcard += ("{} has {} {}\n".format(uname, count, magicname))
                cardlist = list(set(cardlist))
                cardsnonehas = list(set(cardwantedlist).difference(cardlist))
                cardsnonehaswrite = ""
                for x in cardsnonehas:
                    cardsnonehaswrite += ('\n{}:\nNo one has this card or the card name was missed spelled\n'.format(x))
                filename = f'{timeofsend}{ctx.author.id}.txt'
                savepath = 'F:/Documents/Python Projects/MagicBot/Massexports'
                filepath = os.path.join(savepath, filename)
                with open(filepath, "w") as f:
                    f.write(F'{noatcard}\n{60 * "-"}\n{cardsnonehaswrite}')
                file = discord.File(filepath)
                flushdir(savepath)
        await ctx.send(file=file,
                       content=f'<@!{ctx.author.id}> we have found your cards!\n\nHere are users for quick whisper: {atcard}\n\nHere is the users who have cards on your list:')
        mycursor.close()

##removes files that are a minute old to keel the massexports folder from filling up
def flushdir(dir):
    now = time.time()
    for f in os.listdir(dir):
        fullpath = os.path.join(dir, f)
        if os.stat(fullpath).st_mtime < (now - 60):
            if os.path.isfile(fullpath):
                os.remove(fullpath)
            elif os.path.isdir(fullpath):
                flushdir(fullpath)

async def setup(client):
    await client.add_cog(want(client))