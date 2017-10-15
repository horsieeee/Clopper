import discord
from discord.ext import commands
from utils import perms
from utils.dataIO import dataIO, fileIO

from random import randint
import os
import time

client = discord.Client()


class Levels:
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = 60
        self.leader_board = dataIO.load_json("data/levels/leader_board.json")
        self.gettingxp = {}
        self.xp_gaining_channels = []

    @commands.group(name="rank", pass_context=True)
    async def _rank(self, ctx):
        """Rank operations"""
        if ctx.invoked_subcommand is None:
            await self.bot.say('Check c!help for help on this rank.')

    @_rank.command(pass_context=True, no_pm=True)
    async def join(self, ctx, user: discord.Member = None):
        """Join the system yourself. When you join, you'll be greeted with your own rank and EXP. The more active
        you are, the more rank you get."""
        if not user:
            user = ctx.message.author
            if user.id not in self.leader_board:
                self.leader_board[user.id] = {"name": user.name, "rank": 0, "XP": 0}
                dataIO.save_json("data/levels/leader_board.json", self.leader_board)
                embed = discord.Embed(title='Rank', description="{} has joined the clopperboard!".format(user.mention))
                await self.bot.say(embed=discord.Embed)
            else:
                embed = discord.Embed(title='Rank', description="{} has already joined and is rank {}".format(user.mention, str(self.get_rank(user.id))))
                await self.bot.say(
                    embed=embed)
        else:
            await self.bot.say(
                ":x: Thanks to idiots overusing the ability to `rank join` others, this part of the command cannot be used! \nPlease get a Moderator or Admin to use `rank joino`!\nIf you're trying to `rank join` yourself...then please do `rank join` without a mention!")

    @_rank.command(name="joino", pass_context=True, no_pm=True)
    @perms.admin_or_permissions(manage_server=True)
    async def joino(self, ctx, user: discord.Member):
        """Forces another person to join the ranking system."""
        if not user:
            if user.id not in self.leader_board:
                self.leader_board[user.id] = {"name": user.name, "rank": 0, "XP": 0}
                dataIO.save_json("data/levels/leader_board.json", self.leader_board)
                embed = discord.Embed(title='Rank', description="{} has joined the clopperboard!".format(user.mention))
                await self.bot.say(embed=embed)
            else:
                embed = discord.Embed(title='Rank',
                                      description="{} has already joined and is rank {}".format(user.mention, str(
                                          self.get_rank(user.id))))
                await self.bot.say(
                    embed=embed)
        else:
            if user.id not in self.leader_board:
                self.leader_board[user.id] = {"name": user.name, "rank": 0, "XP": 0}
                dataIO.save_json("data/levels/leader_board.json", self.leader_board)
                embed = discord.Embed(title='Rank', description="{} has joined the clopperboard!".format(user.mention))
                await self.bot.say(embed=embed)
            else:
                embed = discord.Embed(title='Rank',
                                      description="{} has already joined and is rank {}".format(user.mention, str(
                                          self.get_rank(user.id))))
                await self.bot.say(
                    embed=embed)

    @_rank.command(name="set", pass_context=True, no_pm=True)
    @perms.admin_or_permissions(manage_server=True)
    async def _set(self, ctx, user: discord.Member, rank: int, xp: int):
        """Set rank and EXP of particular user."""
        if user.id in self.leader_board:
            self.leader_board[user.id] = {"name": user.name, "rank": rank, "XP": xp}
            dataIO.save_json("data/levels/leader_board.json", self.leader_board)
            await self.bot.say(
                "{}'s current stats are now: **Rank: {} XP {}/{}**".format(user.mention, self.get_rank(user.id),
                                                                           self.get_xp(user.id),
                                                                           self.get_level_xp(int(
                                                                               self.leader_board[user.id]["rank"]))))
        else:
            await self.bot.say(
                "{} is not in the clopperboard. Please make {} do `{}rank join` so their XP and Rank can be set!".format(
                    user.mention, user.mention, ctx.prefix))

    @_rank.command(pass_context=True, no_pm=True)
    async def leave(self, ctx, user: discord.Member = None):
        """Leave the ranking system. This will erase your progress."""
        user = ctx.message.author
        if user.id in self.leader_board:
            del self.leader_board[user.id]
            dataIO.save_json("data/levels/leader_board.json", self.leader_board)
            await self.bot.say(embed=discord.Embed(title='Rank', description="{} has left in the clopperboard!".format(user.mention)))
        else:
            await self.bot.say(
                embed=discord.Embed(title='Rank', description="{} has not yet joined in the clopperboard! Do `{}rank join`!".format(user.mention, ctx.prefix)))

    @_rank.command(name="show", pass_context=True)
    async def _show(self, ctx, user: discord.Member = None):
        """Show rank and XP of users.
        Defaults to yours."""
        if not user:
            user = ctx.message.author  # LEVEL 13 | XP 1438/1595 | TOTAL XP 9888 | Rank 5/829
            if self.check_joined(user.id):
                await self.bot.say(embed=discord.Embed(title='Rank',
                                                       description="{} **LEVEL {} | XP {}/{} **".format(user.name, self.get_rank(user.id),
                                                                        self.get_xp(user.id),
                                                                        self.get_level_xp(
                                                                            int(self.leader_board[user.id]["rank"])))))
            else:
                await self.bot.say(
                    embed=discord.Embed(title='Rank', description="You are not in the ranking system. Type `{}rank join` to join".format(user.mention, ctx.prefix)))
        else:
            if self.check_joined(user.id):
                rank = self.get_rank(user.id)
                xp = self.get_xp(user.id)
                await self.bot.say(embed=discord.Embed(title='Rank',
                                                       description="{} **LEVEL {} | XP {}/{} **".format(user.name,
                                                                                                        self.get_rank(
                                                                                                            user.id),
                                                                                                        self.get_xp(
                                                                                                            user.id),
                                                                                                        self.get_level_xp(
                                                                                                            int(
                                                                                                                self.leader_board[
                                                                                                                    user.id][
                                                                                                                    "rank"])))))
            else:
                await self.bot.say(embed=discord.Embed(title='Rank', description="This user has not joined the rank system"))

    @_rank.command(pass_context=True)
    async def levelup(self, ctx):
        """level up. Mainly used in case Auto-Leveling doesn't work!"""
        user = ctx.message.author
        if self.leader_board[user.id]["XP"] >= self.get_level_xp(self.leader_board[user.id]["rank"]):
            self.leader_board[user.id]["rank"] += 1
            self.leader_board[user.id]["XP"] -= self.get_level_xp(self.leader_board[user.id]["rank"])
            embed = discord.Embed(
                title='Rank',
                description="{}: Level Up! You are now level {}".format(user.mention,
                                                                           self.leader_board[user.id]["rank"])
            )
            await self.bot.say(embed=embed)
        else:
            await self.bot.say(embed=discord.Embed(title='Rank', description='You are not ready.'))

    @_rank.command()
    async def clopperboard(self, top: int = 10):
        """Prints out the rank leaderboard.
        Defaults to top 10, unless 10 haven't joined the ranking system."""
        if top < 1:
            top = 10
        if top > 20:
            top = 20
        leader_board_sorted = sorted(self.leader_board.items(), key=lambda x: x[1]["rank"], reverse=True)
        if len(leader_board_sorted) < top:
            top = len(leader_board_sorted)
        topten = leader_board_sorted[:top]
        highscore = ""
        place = 1
        for id in topten:
            highscore += str(place).ljust(len(str(top)) + 1)
            highscore += (id[1]["name"] + " ").ljust(23 - len(str(id[1]["rank"])))
            highscore += str(id[1]["rank"]) + "\n"
            place += 1
        if highscore:
            if len(highscore) < 1985:
                await self.bot.say("```py\n" + highscore + "```")
            else:
                await self.bot.say(":x: The leaderboard is too big to be displayed. Try with a lower <top> parameter.")
        else:
            await self.bot.say(":x: No one has joined the rank system.")

    async def gain_xp(self, message):
        user = message.author
        id = user.id
        if self.check_joined(id):
            if id in self.gettingxp:
                seconds = abs(self.gettingxp[id] - int(time.perf_counter()))
                if seconds >= self.cooldown:
                    self.add_xp(id)
                    self.gettingxp[id] = int(time.perf_counter())
                    fileIO("data/levels/leader_board.json", "save", self.leader_board)
                if self.leader_board[user.id]["XP"] >= self.get_level_xp(self.leader_board[user.id]["rank"]):
                    self.leader_board[user.id]["rank"] += 1
                    self.leader_board[user.id]["XP"] = 0
                    msg = discord.Embed(
                        title='Rank',
                        description='{} **has leveled up and is now level {}!**'
                    )
                    msg = msg.description.format(message.author.display_name, self.leader_board[user.id]["rank"])
                    await self.bot.send_message(message.channel, msg)
                    fileIO("data/levels/leader_board.json", "save", self.leader_board)
            else:
                self.add_xp(id)
                self.gettingxp[id] = int(time.perf_counter())
                fileIO("data/levels/leader_board.json", "save", self.leader_board)

    def add_xp(self, id):
        if self.check_joined(id):
            self.leader_board[id]["XP"] += int(randint(20, 30))

    def mention_from_id(self, id):
        return "@" + str(self.leader_board[id]["name"]) + "#" + str(id)

    def get_level_xp(self, level):
        xp = 5 * (int(level) ** 2) + 50 * int(level) + 100
        return xp

    def check_joined(self, id):
        if id in self.leader_board:
            return True
        else:
            return False

    def get_rank(self, id):
        if self.check_joined(id):
            return self.leader_board[id]["rank"]

    def get_xp(self, id):
        if self.check_joined(id):
            return self.leader_board[id]["XP"]

    def display_time(self, seconds, granularity=2):  # What would I ever do without stackoverflow?
        intervals = (  # Source: http://stackoverflow.com/a/24542445
            ('weeks', 604800),  # 60 * 60 * 24 * 7
            ('days', 86400),  # 60 * 60 * 24
            ('hours', 3600),  # 60 * 60
            ('minutes', 60),
            ('seconds', 1),
        )

        result = []

        for name, count in intervals:
            value = seconds // count
            if value:
                seconds -= value * count
                if value == 1:
                    name = name.rstrip('s')
                result.append("{} {}".format(value, name))
        return ', '.join(result[:granularity])


def check_folders():
    if not os.path.exists("data/levels"):
        print("Creating data/levels folder...")
        os.mkdir("data/levels")


def check_files():
    fp = "data/levels/leader_board.json"
    if not dataIO.is_valid_json(fp):
        print("Creating leader_board.json...")
        dataIO.save_json(fp, {})


def setup(bot):
    check_folders()
    check_files()
    n = Levels(bot)
    bot.add_listener(n.gain_xp, "on_message")
    bot.add_cog(n)