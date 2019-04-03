import discord
from discord import Game
from discord.ext.commands import Bot
import asyncio
import os

BOT_PREFIX = "e!"
BOT_TOKEN = os.environ.get('EMBA-BOT_TOKEN')

current_announcement = {} # current announcement sent | Key: server id, Value: embedded object
announcement_channel = {} # channel to send announcements to | Key: server id, Value: channel

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

@client.event
async def on_ready():
    """This function runs when the bot is started"""
    await client.change_presence(game = Game(name = '<))'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command(name='set', pass_context=True)
async def set_announcement_channel(ctx):
    """The bot sets the announcement channel specified by the user for the current server
    
    Args:
        - ctx: context of the command
    """
    # gets the channel id from form: <#0000000000> to 00000000000
    channel_id = ctx.message.content[7:].replace(" ", "").replace("<", "").replace("#", "").replace(">", "")

    # get the selected channel
    channel = client.get_channel(channel_id)
    if channel is None:
        await client.send_message(ctx.message.channel, embed=discord.Embed(description="Invalid channel", color=discord.Color.red()))
    else:
        #set announcement channel for current server
        announcement_channel[ctx.message.server.id] = channel
        await client.send_message(ctx.message.channel, embed=discord.Embed(description="Set announcements channel as" + channel.mention, color=discord.Color.green()))

@client.command(name='preview', pass_context=True)
async def preview(ctx):
    """The bot outputs a preview of the embedded announcement
    
    Args:
        - ctx: context of the command (used for getting the server id) 
    """
    # get the servers announcement
    announcement = current_announcement.get(ctx.message.server.id)
    if announcement is None:
        await client.send_message(ctx.message.channel, embed=discord.Embed(description="No announcement message set!", color=discord.Color.red()))
    else:
        await client.send_message(ctx.message.channel, embed=announcement)

@client.command(name='post', pass_context=True)
async def post(ctx):
    """The bot posts the servers announcement to the specified announcement channel

    Args:
        - ctx: context of the command (used for getting the server id) 
    """
    # get server announcement
    announcement = current_announcement.get(ctx.message.server.id)
    if announcement is None: # if no announcement set
        await client.send_message(ctx.message.channel, embed=discord.Embed(description="No announcement message set!", color=discord.Color.red()))
        return
    # get announcement channel
    channel = announcement_channel.get(ctx.message.server.id)
    if channel is None: # if no announcement channel set
        await client.send_message(ctx.message.channel, embed=discord.Embed(description="No announcement channel set!", color=discord.Color.red()))
    else:
        await client.send_message(channel, embed=announcement)

client.run(BOT_TOKEN)
