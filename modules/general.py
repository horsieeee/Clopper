import discord
from discord.ext import commands
import asyncio
import os
import time
from utils.dataIO import dataIO, fileIO


class General:
    """General cogs for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.reminders = fileIO("data/general/reminders.json", "load")
        self.units = {"minute": 60, "hour": 3600, "day": 86400, "week": 604800, "month": 2592000}

    @commands.command(pass_context=True)
    async def reminder(self, ctx, quantity: int, time_unit: str, *, text: str):
        """Gives you a reminder."""
        time_unit = time_unit.lower()
        author = ctx.message.author
        s = ""
        if time_unit.endswith("s"):
            time_unit = time_unit[:-1]
            s = "s"
        if not time_unit in self.units:
            await self.bot.say(":x: Invalid time unit. You must choose: minute/hour/day/week/month")
            return
        if quantity < 1:
            await self.bot.say(":x: Quantity must not be 0 or negative.")
            return
        if len(text) > 1960:
            await self.bot.say(":x: Text is too long. Shorten your text.")
            return
        seconds = self.units[time_unit] * quantity
        future = int(time.time() + seconds)
        self.reminders.append({"ID": author.id, "FUTURE": future, "TEXT": text})
        await self.bot.say(":clock: I will remind you in {} {}.".format(str(quantity), time_unit + s))
        fileIO("data/general/reminders.json", "save", self.reminders)

    async def check_reminders(self):
        while self is self.bot.get_cog("General"):
            to_remove = []
            for reminder in self.reminders:
                if reminder["FUTURE"] <= int(time.time()):
                    try:
                        await self.bot.send_message(discord.User(id=reminder["ID"]),
                                                    "You asked me to remind you this:\n{}".format(reminder["TEXT"]))
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(reminder)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(reminder)
            for reminder in to_remove:
                self.reminders.remove(reminder)
            if to_remove:
                fileIO("data/general/reminders.json", "save", self.reminders)
            await asyncio.sleep(5)


def setup(bot):
    n = General(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.check_reminders())
    bot.add_cog(n)
