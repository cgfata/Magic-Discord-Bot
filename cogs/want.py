import mysql.connector
import discord
import time
import re
import os
from discord.ext import commands
from functions import wantcardsuser, cardnamechecker, cardnamecheckername



class want(commands.Cog):

    def __init__(self,client):
        self.client = client

    #commands
    @commands.command(brief='Will @ People who have the card and how many')
    async def want(self, ctx, *, card):
        await ctx.send(f'looking up the users who have {card}......')
        if "}" in str(f'{card}') or "{" in str(f'{card}'):
            await ctx.send('Hey now. You stop that!')
        elif "None" in str(await cardnamechecker(f'{card}')):
            await ctx.send('The card name is incorrect')
        elif "None" in str(await wantcardsuser(f'{card}')):
            await ctx.send('No one has the card')
        else:
            from database import db_info
            db = mysql.connector.connect(**db_info)
            mycursor = db.cursor()
            atcard = ""
            noatcard = ""
            guild = str(ctx.guild.id)
            cardoutputname = await cardnamecheckername(f'{card}')
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
                f'<@!{ctx.author.id}> here are the users who have the card {card}:\n\n{atcard + noatcard}')
        mycursor.close()
        db.close()

    @commands.command(brief='Wll look up a mass import of who has the cards. ')
    async def masswant(self, ctx, *, card):
        cardsplit = (re.split("\n+", card))
        timeofsend = int(time.time())
        nonumber = ""
        lessthan10 = ""
        greaterthan10 = ""
        numbercheck = list(range(10))
        cardwantedlist = []
        if "}" in str(f'{card}') or "{" in str(f'{card}'):
            await ctx.send('Please remove { or } from your list!')
        else:
            await ctx.send('looking up the users who have cards from the list......')
            for card in cardsplit:
                if card[0] not in str(numbercheck):
                    nonumber += ('i.name = "{}" OR '.format(card))
                    cardwantedlist.append('{}'.format(card))
                elif card[0] == " ":
                    nonumber += ('i.name = "{}" OR '.format(card))
                    cardwantedlist.append('{}'.format(card))
                elif int(card[0] + card[1]) < 10:
                    lessthan10 += ('i.name = "{}" OR '.format(card[2:]))
                    cardwantedlist.append('{}'.format(card[2:]))
                else:
                    greaterthan10 += ('i.name = "{}" OR '.format(card[3:]))
                    cardwantedlist.append('{}'.format(card[3:]))
                whereintoquery = (nonumber + greaterthan10 + lessthan10)[:-3]
                from database import db_info
                db = mysql.connector.connect(**db_info)
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
                cardlist_lower = [card.lower() for card in cardlist]
                cardwantedlist_lower = [card.lower() for card in cardwantedlist]
                cardsnonehas = list(set(cardwantedlist_lower).difference(cardlist_lower))
                cardsnonehasmessege = ""
                for card in cardsnonehas:
                    cardsnonehasmessege += ('\n{}:\nNo one has this card or the card name was missed spelled\n'.format(card))
                filename = f'{timeofsend}{ctx.author.id}.txt'
                savepath = 'F:/Documents/Python Projects/MagicBot/Massexports'
                filepath = os.path.join(savepath, filename)
                with open(filepath, "w") as f:
                    f.write(F'{noatcard}\n{60 * "-"}\n{cardsnonehasmessege}')
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