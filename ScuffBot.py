import os
import random
import discord
from discord.ext.commands import Bot, has_permissions, CheckFailure

import json

from discord.ext import commands


intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '-', intents = intents)

OWNERID = 152557345241563138

players = {}

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name = "with yo mama"))
    print('bruh')


if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token" : ""}
    
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)


TOKEN = configData["Token"]

@client.event 
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color = discord.Colour.red())
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
        await ctx.send(embed=embed)
    else:
        embed.add_field(name = f':x: Error', value = f"```{error}```")
        await ctx.send(embed = embed)
        raise error


@client.command()
async def info(ctx):
    embed = discord.Embed(title = "Bot Information", 
                          description = "Created by: <@152557345241563138> \nDM him if you have any questions or concerns\n", 
                          color = discord.Colour.purple())
    embed.add_field(name = "Just for fun:", value = "-------------------------", inline = False)
    embed.add_field(name = "-bruh", value = "Prints out a random gif tagged with bruh", inline = True)
    embed.add_field(name = "-8ball *\*question*\*", value = "Asks the 8ball a question", inline = True)
    embed.add_field(name = "Admin Commands:", value = "-------------------------", inline = False)
    embed.add_field(name = "-clear *\*number*\*", value = "Deletes 'x' amount of previous messages which includes the command message", inline = True)
    embed.add_field(name = "-kick *\*user*\* *\*reason*\*", value = "Kicks a user from the server. \nA reason is not required", inline = True)
    embed.add_field(name = "-ban *\*user*\* *\*reason*\*", value = "Bans a user from the server. \nA reason is not required", inline = True)
    embed.add_field(name = "-unban *\*user*\*", value = "Unbans a user. \nNo need to use '@' when mentioning the user", inline = True)
    embed.set_thumbnail(url = "https://i.imgur.com/jv4qYz9.jpg")
    await ctx.send(embed = embed)


@client.command()
async def bruh(ctx):
    responses = ["bruh",
                 "https://tenor.com/view/bruh-bye-ciao-gif-5156041",
                 "https://tenor.com/view/bruh-really-tell-me-more-no-way-wth-gif-21239271",
                 "https://tenor.com/view/bruh-toongeek-toon-geek-gif-14920844",
                 "https://tenor.com/view/mr-krabs-bruh-cringe-meme-gif-20821912",
                 "https://tenor.com/view/bruh-kanye-west-rapper-drop-shattered-gif-17839027",
                 "https://media.tenor.com/images/96e223599d598fa72d54581fccb1bc7e/tenor.gif",
                 "https://media.tenor.com/images/5f10dc6aeacf6beba81597866ae32ccc/tenor.gif",
                 "https://media1.tenor.com/images/5f246afc9eb3a9a1ee0f81091247a4d8/tenor.gif?itemid=19321120",
                 "https://media1.tenor.com/images/dfad879f35beff0fa147242f51494a56/tenor.gif?itemid=14698316",
                 "https://media.tenor.com/images/523359146a6048de2db2aff4eecc0cea/tenor.gif",
                 "https://media.tenor.com/images/36873cebf8d6e24182385de6a9866768/tenor.gif",
                 "https://media1.tenor.com/images/58024c34bb6049eb766f29451043fd87/tenor.gif?itemid=20945073",
                 "https://media.tenor.com/images/b3bc71f95ec4d0b896306aaffe8e382f/tenor.gif",
                 "https://media1.tenor.com/images/eabe3ebc6c96382a752cc71f0da6235a/tenor.gif?itemid=20291001",
                 "https://tenor.com/view/bruh-dog-bruh-moment-gif-19928725"]
    
    await ctx.send(f"{random.choice(responses)}")


@client.command(aliases = ["8ball"])
async def _8ball(ctx, *, question):
    responses = ["It is Certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes dude",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "idk lol",
                 "bruh",
                 "Cannot predict now.",
                 "lmao what",
                 "no.",
                 "?????????? ofc no",
                 "My reply is no.",
                 "My sources say no.",
                 "Very doubtful.",
                 "Outlook not so good."]
    
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")    

@client.command()
@has_permissions(administrator = True)
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)


@client.command()
@has_permissions(administrator = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)


@client.command()
@has_permissions(administrator = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"Banned {member.mention}")


@client.command()
@has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


client.run(TOKEN)
