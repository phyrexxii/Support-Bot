import discord
import time
import datetime
import asyncio
import random

from discord.ext import commands
from random import randint

class Games():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def choose(self, *choices : str):
        """Chooses Between Multiple Choices!"""
        await self.bot.say(random.choice(choices))

def setup(bot):
    bot.add_cog(Games(bot))
