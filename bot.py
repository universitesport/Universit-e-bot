#Author : CUNY Félicien
#Language : FR - French
#Date : 01/12/2020
#Copyright : This code can be use for every member working on 'Universit'E-Bot' discord bot only. If you want to work on it, please contact me : felicien.cuny@outlook.fr

import discord #importation des modules discord
import random  #importation du random
import os #pour les cogs
from discord.ext import commands #importation des fonctions pour discord bot

universitebot = commands.Bot(command_prefix = '$') #prefixe à utiliser pour intéragir avec le bot

@universitebot.event #Déclarer à chaque fois que l'on veut une action du bot
async def on_ready(): #lancement du bot en ligne
    print('Le bot est pret') #indique que le bot est lancé.

@universitebot.command() #Déclarer à chaque fois que l'on veut utiliser le bot
async def ping(ctx): #ping = nom de la commande; exemple $ping pourra être utiliser sur discord pour trigger le bot
    await ctx.send("Pong !")

@universitebot.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@universitebot.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        universitebot.load_extension(f'cogs.{filename[:-3]}')

universitebot.run('Token')
