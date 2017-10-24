# `Clopper`
Clopper is a multipurpose discord bot written in Python. It utilizes the discord.py library, allowing it to make use of a command registering system. Clopper has a built-in level and profile system, audio, a moderation extension, and a fun extension, including 8ball and urban dictionary.
## How to Install
If you want to self host (which is not recommended) you'll first need these libraries:
- urbandictionary
- discord.py[voice] (On Linux, you'll need the `libffi-dev` package.)
- bs4
- requests
- google

Next, open up [Discord's app page](https://discordapp.com/developers/applications/me "App page") and select "New App." There, you'll be able to customize your bot's name and add an avatar. When you're done, save. You'll notice a button that says "Create a Bot User" and that's what you want to click. Once you click it, you should see a text saying "Click to reveal token." Copy it, or place it in a text file for later reference.

You'll now want to go into the folder containing Clopper, and edit bot.py. You'll want to replace "token" in clopper.run(token) with your token.

Once you've done that, double check you have every library needed installed, and run the bot!
## Custom Modules / Cogs
I'll be posting a custom cog tutorial on the Wiki very soon. ;)
