import discord
import time
import datetime
import asyncio
import random
import os

from discord.ext import commands
from discord.ext.commands import Bot
from random import randint

bot = commands.Bot(command_prefix = commands.when_mentioned_or("s-"))
tu = datetime.datetime.now()
version = "Support Bot v0.1"
startup_extensions = ["cogs.games"]
bot_request = "398983251101745182"
verif = discord.Object("398961598145888266")

@bot.event
async def on_ready():
    print("===================================")
    print("Logged in as: %s"%bot.user.name)
    print("ID: %s"%bot.user.id)
    print('Server count:', str(len(bot.servers)))
    print('User Count:',len(set(bot.get_all_members())))
    print("Py Lib Version: %s"%discord.__version__)
    print("===================================")
    while 1==1:
        await bot.change_presence(game=discord.Game(name='My Developer'))
        await asyncio.sleep(60)
        await bot.change_presence(game=discord.Game(name='Counter Strike: Global Offensive'))
        await asyncio.sleep(60)                         
        await bot.change_presence(game=discord.Game(name='Getting Over It With Bennett Foddy'))
        await asyncio.sleep(60)
        await bot.change_presence(game=discord.Game(name='Import discord'))
        await asyncio.sleep(60)

@bot.command(pass_context=True)
async def ping(ctx):
    """Check The Bots Response Time"""
    t1 = time.perf_counter()
    await bot.send_typing(ctx.message.channel)
    t2 = time.perf_counter()
    thedata = (":ping_pong: **Pong.**\nTime: " + str(round((t2 - t1) * 1000)) + "ms")
    color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
    color = int(color, 16)
    data = discord.Embed(description = thedata, colour=discord.Colour(value = color))
    data.set_footer(text="{} | Requested by: {}".format(version, ctx.message.author))
    await bot.say(embed = data)

@bot.command(pass_context = True)
async def uptime(ctx):
    """Check bot uptime."""
    global tu
    colour = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
    colour = int(colour, 16)
    embed = discord.Embed(colour = discord.Colour(value = colour), timestamp = datetime.datetime.utcnow())
    embed.add_field(name = "__**My Current Uptime :**__",value = (timedelta_str(datetime.datetime.now() - tu)))
    embed.set_footer(text= "{} | Requested by: {}".format(version, ctx.message.author))
    await bot.say(embed = embed)

#Convert uptime to a string.
def timedelta_str(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec)

@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("`{}` loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("`{}` unloaded.".format(extension_name))

@bot.command(pass_context = True)
async def iamrewrite(ctx):
    """Give a user the role Discord.py Rewrite"""
    role = discord.utils.get(ctx.message.server.roles, name="Discord.py Rewrite")
    if "Discord.py Rewrite" in [role.name for role in ctx.message.author.roles]:
        await bot.remove_roles(ctx.message.author, role)
        await bot.say(":x:  | You already had the `Discord.py Rewrite` role added, so I removed it")
    else:
        await bot.add_roles(ctx.message.author, role)
        await bot.say(":white_check_mark: | I've Given You The `Discord.py Rewrite` Role")

@bot.command(pass_context = True)
async def iamasync(ctx):
    """Give a user the role Discord.py Async"""
    role = discord.utils.get(ctx.message.server.roles, name="Discord.py Async")
    if "Discord.py Async" in [role.name for role in ctx.message.author.roles]:
        await bot.remove_roles(ctx.message.author, role)
        await bot.say(":x:  | You already had the `Discord.py Async` role added, so I removed it")
    else:
        await bot.add_roles(ctx.message.author, role)
        await bot.say(":white_check_mark: | I've Given You The `Discord.py Async` Role")

@bot.command(pass_context = True)
async def verify(ctx, member : discord.Member = None):
    """Verify a members Bot"""
    user_roles = [r.name.lower() for r in ctx.message.author.roles]
    

    if "admin" in user_roles:
        if member is None:
            await bot.say(":x: | Please `Tag` A `Bot` To `Verify`!")
        
        else:
            try:
                oldrole = discord.utils.get(member.server.roles, name = "Not Yet Verified")
                newrole = discord.utils.get(member.server.roles, name = "Verified Bot")
                await bot.add_roles(member, newrole)
                await asyncio.sleep(1)
                await bot.remove_roles(member, oldrole)
                await bot.add_reaction(ctx.message, "\U00002705")
                chan = discord.Object('402963004183805962')
                em = discord.Embed(title="Bot verified", description="{0} was verified by {1}".format(member.mention, ctx.message.author.mention))
                await bot.send_message(chan, embed=em)
            except:
                await bot.say(":x: Error verifying that bot!")

@bot.event
async def on_member_join(member):
    if member.bot is True:
        role = discord.utils.get(member.server.roles, name = "Not Yet Verified")
        await bot.add_roles(member, role)

@bot.event
async def on_message(message):
    if message.channel.id == bot_request:
        if message.author.id != bot.user.id:
            if len(message.content) == 18:
                try:
                    message.content = int(message.content)
                except ValueError:
                    await bot.send_message(message.author, "Please use a valid bot ID in #bot-requests")
                
                invite = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0".format(message.content)
            
                color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])
                color = int(color, 16)
                embed = discord.Embed(title = "Bot Added! | Please Wait For It To Be Verified!",description = ".",
                                      colour=discord.Colour(value=color), timestamp = datetime.datetime.utcnow())
                embed.add_field(name = "Bot Submitted By:", value = "{}".format(message.author.mention))
                embed.add_field(name = "Invite Link:", value = "'[{}]({})'".format("Invite Link", invite))
                await bot.delete_message(message)
                await bot.send_message(message.channel, embed = embed)
                await bot.send_message(verif, embed = embed)
            else:
                await bot.delete_message(message)
                await bot.send_message(message.author, ":x: | Please, Bot ID's Only In #bot-requests")
    await bot.process_commands(message)

if not os.environ.get('TOKEN'):
        print("No Token Found")
bot.run(os.environ.get('TOKEN').strip('\"'))
