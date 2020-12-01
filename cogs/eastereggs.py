#Author : CUNY Félicien
#Language : FR - French
#Date : 01/12/2020
#Copyright : This code can be use for every member working on 'Universit'E-Bot' discord bot only. If you want to work on it, please contact me : felicien.cuny@outlook.fr

import discord
import random
from discord.ext import commands

class EasterEggs(commands.Cog): #création de la classe pour le cog

    def __init__(self, universitebot): #connexion avec le bot 
        self.universitebot = universitebot

    @commands.Cog.listener() #Event dans un cog (obligatoire)
    async def on_ready(self): #lancement du bot en ligne
        print('Le bot est pret') #indique que le bot est lancé.

    @commands.command() #Command dans un cog
    async def sardoche(self, ctx): #$sardoche envoie random une citation de sardoche
        reponses = ["Mais c'était sûr en fait !",
                     "Il est mort, le noir est mort",
                     "POURQUOI ? POURQUOI ? POURQUOI ?"]
        await ctx.send(f'{random.choice(reponses)}') #envoie la réponse

def setup(universitebot):
    universitebot.add_cog(EasterEggs(universitebot))
