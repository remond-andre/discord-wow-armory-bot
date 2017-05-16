#!/usr/bin/python3
# -*- coding: utf-8 -*-
import discord
import os
import re
from wow import *


DISCORD_BOT_TOKEN = str(os.environ.get('DISCORD_BOT_TOKEN'))
client = discord.Client()


@client.event
async def on_message(message):
    """Listens for specific user messages."""

    # If the author is the bot do nothing.
    if message.author == client.user:
        return

    # If it's not the bot and the message starts with '!armory' process it.
    if message.content.startswith('!armory'):
        # Splits up the message, requires the user to type their message as '!wow Jimo burning-legion'.
        # Sends the second word (name) and third word (realm) to the characterInfo function to build a character sheet.
        split = message.content.split(" ")
        info = characterInfo(split[1], split[2])

        # If the returned data is an empty string send a message saying the player/realm couldn't be found.
        if info == '':
            msg = 'Could not find a player with that name/realm combination.'.format(message)
            await client.send_message(message.channel, msg)
        # Otherwise respond with an incredibly long string of data holding all of the info.
        else:
            colour_code = classColour(info['class_type'])
            msg = discord.Embed(title="%s" % (info['name']), colour=discord.Colour(colour_code), url="%s" % (info['armory']), description="%s" % (info['realm']))

            msg.set_thumbnail(url="https://render-%s.worldofwarcraft.com/character/%s" % (WOW_REGION, info['thumb']))
            msg.set_footer(text="Generated by WoW Armory Bot - https://jamesiv.es", icon_url="https://github.com/JamesIves/discord-wow-armory-bot/blob/master/assets/icon.jpg?raw=true")

            msg.add_field(name="Character", value="**Character** %s\n**Realm** %s\n**Item Level** %s" % (info['name'], info['realm'], info['ilvl']), inline=True)


            await client.send_message(message.channel, embed=msg)


client.run(DISCORD_BOT_TOKEN)
