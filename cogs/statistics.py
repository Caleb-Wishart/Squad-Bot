# general_commands.py

### IMPORTS ###
import discord
from discord.ext import tasks, commands

import os
from sys import path
path.append("..") # Adds higher directory to python modules path.
from roles import admin_roles, elevated_roles
import re
import logging


channel_id = 910694743728619540
save_file = "./statistics.sav"

class ScreamLog:
    def __init__(self, aid, number = 0, days = 0, bestDays = 0) -> None:
        self.aid = aid
        self.total = number
        self.days = days
        self.bestDays = bestDays

    def addDay(self):
        self.days += 1
        if self.days > self.bestDays:
            self.bestDays = self.days

    def __repr__(self) -> str:
        return f"""Total number of screams: {self.total}
    Number of consecutive days: {self.days}
    Best streak: {self.bestDays}"""

    def encode(self) -> str:
        return f"{self.aid},{self.total},{self.days},{self.bestDays}\n"

class statistics_commands(commands.Cog):
    regexp = re.compile(r'[ \t]?[aA]+[hH]*(?![^\s])')

    def __init__(self,client):
        self.client = client
        self.log = {}
        self.screamsToday = []
        if os.path.exists(save_file):
            with open(save_file,'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.split(',')
                    if len(parts) == 4:
                        self.log[parts[0]] = ScreamLog(parts[0],parts[1],parts[2],parts[3])

    def generateStatistics(self, aid):
        return self.log[aid]


    ### Tasls ###
    @tasks.loop(hours=24)
    async def newDay(self):
        self.screamsToday = []
        with open(save_file, 'w') as f:
            f.writelines([value.encode() for value in self.log.values()])


    ### Listener ###
    @commands.Cog.listener()
    async def on_message(self, message):
        # don't respond to bots
        if message.author.bot:
            return
        if message.channel.id == channel_id:
            msg = message.content
            aid = message.author.id
            if self.regexp.search(msg):
                if aid not in self.log:
                    self.log[aid] = ScreamLog(aid)
                self.log[aid].total += 1
                if aid not in self.screamsToday:
                    self.screamsToday.append(aid)
                    self.log[aid].addDay()
                    await message.channel.send(f'Congrats <@{aid}> on your first scream of the day.\nYour current streak is: {self.log[aid].days}.\nFor more information see the ".cs help stats" command.')

    ### COMMANDS ###
    @commands.command(aliases=['stats'],
        brief='Statistics of screams into the void',
        description='Gives details on the number of times people have screemed into the void'
        )
    async def statistics(self, ctx):
        logging.info(f"<@{ctx.author.id}> called statistics")
        if ctx.author.id in self.log:
            await ctx.send(f'<@{ctx.author.id}>, here are your statistics\n{self.generateStatistics(ctx.author.id)}')
        else:
            await ctx.send(f"<@{ctx.author.id}>, you have not down any screaming yet.")

    @commands.command(aliases=['screamtop'],
        brief='Statistics of best screamers into the void',
        description='Gives details on the number of times people have screemed into the void'
        )
    async def leaderboard(self, ctx):
        logging.info(f"<@{ctx.author.id}> called leaderboard")
        logs = list(self.log.values())

        top = 3

        bestTotal = sorted(logs,key= lambda l: l.total, reverse=True)[:top]
        bestStreak = sorted(logs,key= lambda l: l.days, reverse=True)[:top]
        bestStreakHistorical = sorted(logs,key= lambda l: l.bestDays, reverse=True)[:top]
        message = " ---{ LEADERBOARD }---\n"
        message += "-> Total Number of times screamed\n"

        for i in range(len(bestTotal)):
            username = await self.client.fetch_user(bestTotal[i].aid)
            username = "[Unknown]" if username == None else username
            message += f"---> {i+1}: {username} with {bestTotal[i].total} screams.\n"
        for i in range(len(bestTotal),top):
            message += f"---> {i+1}: This could be you!\n"

        message += "-> Best active daily streak\n"
        for i in range(len(bestStreak)):
            username = await self.client.fetch_user(bestTotal[i].aid)
            username = "[Unknown]" if username == None else username
            message += f"---> {i+1}: {username} with {bestStreak[i].days} days.\n"
        for i in range(len(bestStreak),top):
            message += f"---> {i+1}: This could be you!\n"

        message += "-> Best historical daily streak\n"
        for i in range(len(bestStreakHistorical)):
            username = await self.client.fetch_user(bestTotal[i].aid)
            username = "[Unknown]" if username == None else username
            message += f"---> {i+1}: {username} with {bestStreakHistorical[i].bestDays} days.\n"
        for i in range(len(bestStreakHistorical),top):
            message += f"---> {i+1}: This could be you!\n"

        await ctx.send(message)

    @commands.command(
        brief='Resets the scream statistics',
        description='Clears the scream statistics\nRequires an elevated role.'
        )
    @commands.has_any_role(*elevated_roles)
    async def clearStats(self, ctx, amount=5):
        logging.warning(f"<@{ctx.author.id}> called clearStats")
        self.log = {}
        self.screamsToday = []
        if os.path.exists(save_file):
            os.remove(save_file)
            logging.info("Save file deleted")
    @commands.command(
        brief='Force saves stats to a file',
        description='See brief\nRequires an elevated role.'
        )
    @commands.has_any_role(*elevated_roles)
    async def saveStats(self, ctx):
        logging.warning(f"<@{ctx.author.id}> called saveStats")
        with open(save_file, 'w') as f:
            f.writelines([value.encode() for value in self.log.values()])



def setup(client):
    client.add_cog(statistics_commands(client))

def teardown(client):
    pass