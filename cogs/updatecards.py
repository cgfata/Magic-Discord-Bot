import discord
import os
import zipfile
import csv
import requests
import pandas as pd
from sqlalchemy import create_engine
from pandas.io import sql
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import commands
from dotenv import load_dotenv
from functions import wantcardsuser, cardnamechecker, cardnamecheckername,cardinfo

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
MAGIC_INVENTORY_HOST = os.getenv('HOST')
MAGIC_INVENTORY_USER = os.getenv('USER')
MAGIC_INVENTORY_PASSWORD = os.getenv('PASSWORD')
MAGIC_INVENTORY_DATABASE = os.getenv('DATABASE')

class updatecards(commands.Cog):

    def __init__(self,client):
        self.client = client


    #commands
    @commands.command(brief='Will update the card database')
    async def updatecards(self, ctx):
        await ctx.send("Downloading the most recent cards from MTGjson and updating the database")
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
        await ctx.send("Updated the card database!")

async def setup(client):
    await client.add_cog(updatecards(client))