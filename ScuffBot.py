import os
import random
import youtube_dl
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


if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token" : ""}
    
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)




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


client.remove_command("help")

@client.command()
async def help(ctx):
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
async def info(ctx):
    embed = discord.Embed(title = "Bot Information", 
                          description = "Created by: <@152557345241563138> \nDM him if you have any questions or concerns\n\nIf you are looking for a command list, type -help", 
                          color = discord.Colour.purple())
    embed.set_thumbnail(url = "https://i.imgur.com/jv4qYz9.jpg")
    await ctx.send(embed = embed)

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
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = ctx.author.voice.channel
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


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
        
@client.command()
async def bruh(ctx):
    responses = ["bruh",
                 "https://tenor.com/view/bruh-bye-ciao-gif-5156041",
                 "https://tenor.com/view/bruh-really-tell-me-more-no-way-wth-gif-21239271",
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
                 "https://tenor.com/view/bruh-dog-bruh-moment-gif-19928725",
                 "https://media.tenor.com/images/8cb0df7519dd635d97505b0b6e10b9f0/tenor.gif",
                 "https://media1.tenor.com/images/e74f1e9fbe531e208fd18b8ff6170dd3/tenor.gif?itemid=16818912",
                 "https://media.tenor.com/images/ac562aeedd3811aa5d2654a8de0a5e72/tenor.gif",
                 "https://media.tenor.com/images/6ec7601094698b939d5d795ba7e3ac9c/tenor.gif",
                 "https://media.tenor.com/images/e614e4ff1732a66fccaf3164a85aef04/tenor.gif",
                 "https://media.tenor.com/images/8ea6c43f8568cef7c2e4483e6d9544de/tenor.gif",
                 "https://media.tenor.com/images/42e40851da9b71547113e9d86f072ab6/tenor.gif",
                 "https://media.tenor.com/images/8bd7afa72a2192b87a1bea611111cd98/tenor.gif",
                 "https://media1.tenor.com/images/b00797bafe2ea3b0f18529a2abfe3664/tenor.gif?itemid=4180987",
                 "https://media1.tenor.com/images/2bd9e7557bf4fbbf74eb935756cc0835/tenor.gif?itemid=19468228",
                 "https://media.tenor.com/images/7b81d2d9258f8fbacd6384321054239e/tenor.gif",
                 "https://media.tenor.com/images/c84b1ce761175bf62c0b9e3e9effebb0/tenor.gif",
                 "https://media.tenor.com/images/f34768293db6cc1b64e7aa2cc4137668/tenor.gif",
                 "https://media.tenor.com/images/674d6a37e5ea1ee67195d4f98d6ad64d/tenor.gif",
                 "https://media.tenor.com/images/00e77afbbcaeb15e82ce8b6dcd1b1c49/tenor.gif",
                 "https://media.tenor.com/images/a6ba42e4cf82a0ffe9afb7093c67f048/tenor.gif",
                 "https://media.tenor.com/images/8cb0df7519dd635d97505b0b6e10b9f0/tenor.gif",
                 "https://media.tenor.com/images/3a706e74b79252ffae1c0216d135bba1/tenor.gif",
                 "https://media.tenor.com/images/7daaf93915b1088f62eb354b774a2c24/tenor.gif",
                 "https://media.tenor.com/images/acd588f27cc25ad4af5f4b0012af5e64/tenor.gif",
                 "https://media.tenor.com/images/f3a90bf4bcef2a0ee8cd27137db80b5b/tenor.gif",
                 "https://media.tenor.com/images/04a929ffc0e86bc926b74cd97ddb6b18/tenor.gif",
                 "https://media.tenor.com/images/6dcd04dddc779a7fb845ad5df3d278e0/tenor.gif",
                 "https://media.tenor.com/images/aa8dd1a3d68f3c93c0d2480194b52cf2/tenor.gif",
                 "https://media.tenor.com/images/9afc6a9a6007665d67a14f058fab880f/tenor.gif",
                 "https://media.tenor.com/images/33ab9247074063b952a7c2019ca3ac11/tenor.gif",
                 "https://media.tenor.com/images/8d85c1768191c2f48c34450e3b8cd62f/tenor.gif",
                 "https://media.tenor.com/images/85e88d1c4c85cdf968e18e1029beb224/tenor.gif",
                 "https://media.tenor.com/images/2f81d51fdf23693d53a405c084977610/tenor.gif",
                 "https://media.tenor.com/images/0d0caa1e9ba95bd11271a5260dc9ad29/tenor.gif",
                 "https://media.tenor.com/images/c70ddcf6a954d3a61d18df493a19a553/tenor.gif",
                 "https://media.tenor.com/images/3c3a9f019759e025edbd879e03404d64/tenor.gif",
                 "https://media.tenor.com/images/2d0e501e44116fd8d7ba0ce9b8628e6a/tenor.gif",
                 "https://media.tenor.com/images/c69c6f9099f83e3d078136e4ed726614/tenor.gif",
                 "https://media.tenor.com/images/a518a7f5070fd49740aba7d5d21f338b/tenor.gif",
                 "https://media.tenor.com/images/8ef529da5848eb8ce49b47743db0ea4c/tenor.gif",
                 "https://media.tenor.com/images/f84ef42646770dd4543fc2395679f655/tenor.gif",
                 "https://media.tenor.com/images/c1492a3a2c64f38edfac863aab22b0f2/tenor.gif",
                 "https://media.tenor.com/images/ab2f7ad7df28aa96349cb9bd4203a670/tenor.gif",
                 "https://media.tenor.com/images/61a8dbd306cb2c3effa059622404f58a/tenor.gif",
                 "https://media.tenor.com/images/6c119d9bcf1e6d1ed1b1f14f3a868299/tenor.gif",
                 "https://media.tenor.com/images/488fe34854f22832db0ba51d3e9a3d81/tenor.gif",
                 "https://media.tenor.com/images/0175ef04fc82f1c7d9a2d360d085ada5/tenor.gif",
                 "https://media.tenor.com/images/23bd1d2d75ae0592848b6b87e8eaabc4/tenor.gif",
                 "https://media.tenor.com/images/ba1b5de1380aaeb591c71baed6c64294/tenor.gif",
                 "https://media.tenor.com/images/e46d3c4fdf9f3d27d33629521b24bbc2/tenor.gif",
                 "https://media.tenor.com/images/4d542d778b102fa60140594da0ec9993/tenor.gif",
                 "https://media.tenor.com/images/d4dd819d00c4735081477cf41f4d9c8b/tenor.gif",
                 "https://media.tenor.com/images/0072975fa22a982536009b1db9ff0c9c/tenor.gif",
                 "https://media.tenor.com/images/d770395d6c01810e65acb3b5e170388b/tenor.gif",
                 "https://media.tenor.com/images/301869566f5577d1f62d99127bac4bc6/tenor.gif",
                 "https://media.tenor.com/images/6f196290a00f2e2f1c0cad41d6a03dee/tenor.gif",
                 "https://media.tenor.com/images/5d40df515f8c181c89e7836feab7a5e1/tenor.gif",
                 "https://media.tenor.com/images/41f55b5a17690c071e94897d52a64989/tenor.gif",
                 "https://media.tenor.com/images/1b9e8aabec14816f4fb35aa10ca066d8/tenor.gif",
                 "https://media.tenor.com/images/bf089ebcae4981d777664c3fed12d587/tenor.gif",
                 "https://media.tenor.com/images/23c86194b91ccbae0b6750444680d10d/tenor.gif",
                 "https://media.tenor.com/images/43cf77b130f29c850ebeca3a97b60c76/tenor.gif",
                 "https://media.tenor.com/images/2e165321639af098ed8e49eb9c6a2af0/tenor.gif",
                 "https://media.tenor.com/images/3a64efd558b4cfeda97b42aace1d9ba5/tenor.gif",
                 "https://media.tenor.com/images/36ec0170540b9316e5f543e4a06b740d/tenor.gif",
                 "https://media.tenor.com/images/1caf728fd4fd3dea759f7b76635c9ddd/tenor.gif",
                 "https://media.tenor.com/images/803aae9b1aa5d0f6d5f41ce32f967db1/tenor.gif",
                 "https://media.tenor.com/images/9b4f5d6293877e179f462ee0ddc065f0/tenor.gif",
                 "https://media.tenor.com/images/5ed4165dd6d54c6c3877277c91646b80/tenor.gif",
                 "https://media.tenor.com/images/6be085a5acbb2a984f575d45a83449b2/tenor.gif",
                 "https://media.tenor.com/images/d0a11e276e0a05901f71fcf5e2fa38da/tenor.gif",
                 "https://media.tenor.com/images/c7b710d0eea09e4e094ebc608aa60698/tenor.gif",
                 "https://media.tenor.com/images/6fedb6ff66eb625311d6074aaff9c571/tenor.gif",
                 "https://media.tenor.com/images/c9f092a0fe28155c4693012c9783efd3/tenor.gif",
                 "https://media.tenor.com/images/6aca64408a594d354b85b84fd94118a9/tenor.gif",
                 "https://media.tenor.com/images/456be536f34143a24eb684445b49ce1d/tenor.gif",
                 "https://media.tenor.com/images/e0fc2163658966e17e4deaca2ee7fcdf/tenor.gif",
                 "https://media.tenor.com/images/064f7fb22c86f1b7405d4713497f6610/tenor.gif"]
    
    await ctx.send(f"{random.choice(responses)}")


client.run(TOKEN)
