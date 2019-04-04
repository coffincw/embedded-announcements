import discord
from discord import Game
from discord.ext.commands import Bot
import asyncio
import os

BOT_PREFIX = "e!"
BOT_TOKEN = os.environ.get('EMBA_BOT_TOKEN')

current_announcement = {} # current announcement sent | Key: server id, Value: embedded object
announcement_channel = {} # channel to send announcements to | Key: server id, Value: channel

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

@client.event
async def on_ready():
    """This function runs when the bot is started"""
    await client.change_presence(game = Game(name = 'the trumpet'))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.command(name='help', pass_context=True)
async def help(ctx):
    """help command"""
    # Only allowed to use commands if they have administrative permissions
    if ctx.message.author.server_permissions.administrator:
        # obtain the argument (remove the command and the leading and trailing whitespaces)
        argument = ctx.message.content[7:].strip()

        #check if user specified create module
        if argument == 'create':
            await helpcreate(ctx)
            return
        embed = discord.Embed(color = discord.Color.orange())
        embed.set_author(name='Help', icon_url='https://cdn.discordapp.com/attachments/561393414571294752/563071668533067901/announcement_icon.jpg')
        embed.add_field(
            name='Commands', 
            value='*e!create [text]* - Creates an an embedded post, to learn more about create try e!help create\n*e!preview* - Sends a preview of the announcement to the requesting channel\n*e!channel [#channel]* - Sets the announcement channel\n*e!post* - post the announcement to the set channel', 
            inline=True
        )
        await client.say(embed=embed)

async def helpcreate(ctx):
    embed = discord.Embed(color=discord.Color.orange())
    embed.set_author(name='Help | Create', icon_url='https://cdn.discordapp.com/attachments/561393414571294752/563071668533067901/announcement_icon.jpg')
    embed.add_field(
        name='Title',
        value='The first part of your input is the title of the announcement, | should be put at the end of the title and any field.\nIn the input: `e!create Contest | Details<This is a test` The title is `Contest`',
        inline=True
    )
    embed.add_field(
        name='Sections',
        value='Separate sections with |',
        inline=True
    )
    embed.add_field(
        name='Section Headers',
        value='^This is a section header, section headers are the first few words after a | before a < in inputed\nIn the input: `e!create Contest | Other Details<The event will take place...` Other Details would be the header',
        inline=True
    )
    await client.send_message(ctx.message.channel, embed=embed)

@client.command(name='create', pass_context=True)
async def create(ctx):
    """The bot creates an announcement and saves it for the server.  The user can then preview or post the announcement
    
    Args:
        - ctx: context of the command
    """
    # Only allowed to use commands if they have administrative permissions
    if ctx.message.author.server_permissions.administrator:
        # get the input (strip the command syntax)
        message = ctx.message.content[9:]

        # split message based on '|'
        input = message.split('|')
        
        if len(input) is 0:
            await client.send_message(ctx.message.channel, embed=discord.Embed(description='No contents specified!', color=discord.Color.red()))
            return

        # create embed with teal color
        announcement = discord.Embed(color=discord.Color.teal())
        
        # set author based on the first part of the users message 
        announcement.set_author(name=input[0], icon_url='https://cdn.discordapp.com/attachments/561393414571294752/563071668533067901/announcement_icon.jpg')
        input = input[1:]
        for segment in input:
            # use the first word as the field name
            field_name = segment.split('<', 1)[0]

            # use the rest as the value
            field_text = segment.split('<', 1)[1]

            #add the field
            announcement.add_field(
                name=field_name,
                value=field_text,
                inline=True
            )
        # set announcement
        current_announcement[ctx.message.server.id] = announcement
        await client.send_message(ctx.message.channel, embed=discord.Embed(description='Announcement set! Preview with with e!preview', color=discord.Color.green()))



@client.command(name='channel', pass_context=True)
async def set_announcement_channel(ctx):
    """The bot sets the announcement channel specified by the user for the current server
    
    Args:
        - ctx: context of the command
    """
    # Only allowed to use commands if they have administrative permissions
    if ctx.message.author.server_permissions.administrator:
        # gets the channel id from form: <#0000000000> to 00000000000
        channel_id = ctx.message.content[10:].replace(" ", "").replace("<", "").replace("#", "").replace(">", "")

        # get the selected channel
        channel = client.get_channel(channel_id)
        if channel is None:
            await client.send_message(ctx.message.channel, embed=discord.Embed(description="Invalid channel", color=discord.Color.red()))
        else:
            #set announcement channel for current server
            announcement_channel[ctx.message.server.id] = channel
            await client.send_message(ctx.message.channel, embed=discord.Embed(description="Set announcements channel as " + channel.mention, color=discord.Color.green()))

@client.command(name='preview', pass_context=True)
async def preview(ctx):
    """The bot outputs a preview of the embedded announcement
    
    Args:
        - ctx: context of the command (used for getting the server id) 
    """
    # Only allowed to use commands if they have administrative permissions
    if ctx.message.author.server_permissions.administrator:
        # get the servers announcement
        announcement = current_announcement.get(ctx.message.server.id)
        if announcement is None:
            await client.send_message(ctx.message.channel, embed=discord.Embed(description="No announcement message set! Set an announcement with e!create", color=discord.Color.red()))
        else:
            await client.send_message(ctx.message.channel, embed=announcement)

@client.command(name='post', pass_context=True)
async def post(ctx):
    """The bot posts the servers announcement to the specified announcement channel

    Args:
        - ctx: context of the command (used for getting the server id) 
    """
    # Only allowed to use commands if they have administrative permissions
    if ctx.message.author.server_permissions.administrator:
        # get server announcement
        announcement = current_announcement.get(ctx.message.server.id)
        if announcement is None: # if no announcement set
            await client.send_message(ctx.message.channel, embed=discord.Embed(description="No announcement message set! Set an announcement with e!create", color=discord.Color.red()))
            return
        # get announcement channel
        channel = announcement_channel.get(ctx.message.server.id)
        if channel is None: # if no announcement channel set
            await client.send_message(ctx.message.channel, embed=discord.Embed(description="No announcement channel set! Set an announcement channel with e!channel", color=discord.Color.red()))
        else:
            everyone = ctx.message.server.roles[0]
            await client.send_message(channel, everyone)
            await client.send_message(channel, embed=announcement)

client.run(BOT_TOKEN)
