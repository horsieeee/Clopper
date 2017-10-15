import discord
from discord.ext import commands
import asyncio
from html.parser import HTMLParser
import random
import urllib.request, urllib.error
import aiohttp
import re
import urllib.parse
import urbandictionary as ud
import google


class RedditHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            if attrs[0][1].startswith('//b.thumbs.redditmedia.com'):
                self.links.append(attrs[0][1])


class ParserException(Exception):
    pass


class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.eight_ball_messages = [
            'Definitely not.', 'Pizza', 'Yes.', 'My sources say yes.', 'My sources say no.',
            'Maybe.', 'Don\'t count on it.'
        ]

    @commands.command(no_pm=True)
    async def meme(self):
        """Pulls up a meme from reddit."""
        try:
            request = urllib.request.Request('http://www.reddit.com/r/dankmemes/')
            data = urllib.request.urlopen(request)
            htmlparser = RedditHTMLParser()
            htmlparser.feed(data.read().decode())
            meme = random.choice(htmlparser.links)
            await self.bot.say('http:' + meme + ' Here\'s your meme :ok_hand:')
        except urllib.error.HTTPError:
            await self.bot.say(':x: An error occured. Please try later.')

    @commands.command(no_pm=True)
    async def urban(self, text):
        """Does a simple urban dictionary definition."""
        definition = ud.define(text)[0]
        embed = discord.Embed(
            title="Definition for " + text,
            description=str(definition.definition)
        )
        if definition.example:
            embed.add_field(name="Example", value=definition.example, inline=False)
        embed.add_field(name="Upvotes", value=str(definition.upvotes), inline=False)
        embed.add_field(name="Downvotes", value=str(definition.downvotes), inline=False)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, name="8ball")
    async def eight_ball(self, ctx, *, q: str):
        """The eight ball has spoken!"""
        await self.bot.say(':8ball: ' + random.choice(self.eight_ball_messages))


def setup(bot): bot.add_cog(Fun(bot))
