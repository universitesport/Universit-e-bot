#Author : CUNY Félicien
#Language : FR - French
#Date : 01/12/2020
#Copyright : This code can be use for every member working on 'Universit'E-Bot' discord bot only. If you want to work on it, please contact me : felicien.cuny@outlook.fr

import discord
from discord.ext import commands

class Admin(commands.Cog): #création de la classe pour le cog

    def __init__(self, universitebot): #connexion avec le bot
        self.universitebot = universitebot

    @commands.Cog.listener() #Event dans un cog (obligatoire)
    async def on_ready(self): #lancement du bot en ligne
        print('Le bot est pret') #indique que le bot est lancé.

    @commands.command() #Command dans un cog
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command() #Command dans un cog
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
                return


def setup(universitebot):
    universitebot.add_cog(Admin(universitebot))
