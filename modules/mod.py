import discord
from discord.ext import commands
import asyncio
from utils import perms
from modules.audio import emoji_list


class Moderation:
    """Moderation commands for Clopper."""
    def __init__(self, bot):
        self.bot = bot
        self.check = emoji_list['check']
        self.error = emoji_list['error']

    @commands.command(pass_context=True, no_pm=True)
    @perms.is_mod()
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        """Warn a user for x reason."""
        warn_embed = discord.Embed(
            title = 'You have been warned.',
            description = 'You were warned for: {}'.format(reason)
        )
        await self.bot.send_message(destination=user, embed=warn_embed)
        await self.bot.say(self.check + ' Warned the user!')

    @commands.command(pass_context=True, no_pm=True)
    @perms.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member):
        """Kicks a member."""
        author = ctx.message.author
        if author == user:
            await self.bot.say(emoji_list['error'] + ' You can\'t do that to yourself.')
            return
        try:
            await self.bot.kick(user)
            await self.bot.say(emoji_list['check'] + ' Kicked {}.'.format(user))
        except discord.errors.Forbidden:
            await self.bot.say(emoji_list['error'] + ' I do not have permission to do this.')

    @commands.command(pass_context=True, no_pm=True)
    @perms.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member):
        """Bans a member."""
        author = ctx.message.author
        if author == user:
            await self.bot.say(emoji_list['error'] + ' You can\'t do that to yourself.')
            return
        try:
            await self.bot.ban(user)
            await self.bot.say(emoji_list['check'] + ' Kicked {}.'.format(user))
        except discord.errors.Forbidden:
            await self.bot.say(emoji_list['error'] + ' I do not have permission to do this.')

    @commands.command(pass_context=True, no_pm=True)
    async def mute(self, ctx, user: discord.Member, *, minutes: int):
        """Mutes a member for an amount of time."""
        for channel in user.server.channels:
            perms = discord.PermissionOverwrite()
            perms.send_messages = False
            await self.bot.edit_channel_permissions(channel, user, perms)
        await self.bot.say(emoji_list['check'] + ' Muted.')
        await asyncio.sleep(minutes * 60)
        for channel in user.server.channels:
            perms = discord.PermissionOverwrite()
            perms.send_messages = None
            await self.bot.edit_channel_permissions(channel, user, perms)

    @commands.command(no_pm=True)
    async def nickname(self, user: discord.Member, *, name: str):
        """Nicknames a user.
        If no name is given, their nick will be reset.
        """
        try:
            if not name:
                self.bot.change_nickname(user, None)
            else:
                self.bot.change_nickname(user, name)
        except discord.errors.Forbidden:
            await self.bot.say(':x: I do not have the valid permissions to do that.')


def setup(bot): bot.add_cog(Moderation(bot))
