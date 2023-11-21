import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import asyncio
import discord.opus
from discord.opus import load_opus
from discord.ext.commands.errors import MemberNotFound
from discord.ext.commands import BadArgument
from discord.ext import commands
from discord.ui import View
from discord.ui.button import Button
from discord.ui.button import ButtonStyle
from discord.ui import View, Button
from discord import ButtonStyle
import os
from dotenv import load_dotenv


# Opus library 
load_opus('/opt/homebrew/Cellar/opus/1.4/lib/libopus.0.dylib')

# bdya d bot
intents = discord.Intents.default()
intents.typing = True
intents.message_content = True
intents.presences = False
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)



# default help command 
bot.remove_command('help')


players = []  # Store player members
roles = []    # Store roles
voice_channel = None  # Store the voice channel connection

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


# Help command como
@bot.command()
async def como(ctx):
    embed = discord.Embed(
        title='Help Command',
        description='lcommands li t9ed tkhdem bihom lbot o li mafhemch had l3jeb ysewel @Kira ilaaa kant fahma tahia',
        color=discord.Color.blue()
    )

    # Category: Shuffle
    embed.add_field(
        name='**Shuffle Commands for The Game**',
        value=(
            '`!shuffle <name1> <name2> ...`: Shuffles and displays a list of names in a circle.\n'
            '`!players <player1> <player2> ...`: Sets the list of players for the game.\n'
            '`!roles <role1> <role2> ...`: Sets the list of roles for the game.\n'
            '`!guru <@player>`: Sends shuffled roles to the mentioned player.\n'
            '`!startgame`: displays time when the game starts.\n'
            '`!endgame`: displays time when the game ends.\n'
        ),
        inline=False
    )

    # Category: sounds
    embed.add_field(
        name='**play sounds in voice channel**',
        value=(
            '`!sounds `: display sounds menu \n'
            '`!music`: display music menu.\n'
            '`!game`: display menu for game music.\n'
        ),
        inline=False
    )

        # Category: Players
    embed.add_field(
        name='**play commands**',
        value=(
            '`!pause `: pause played sound \n'
            '`!resume`: resume music.\n'
            '`!stop`: stop music from playing.\n'
            '`!volume <number>`: stop music from playing.\n'
        ),
        inline=False
    )

    # Category: bot
    embed.add_field(
        name='**Bot commands**',
        value=(
            '`!join`: make the bot join voice channel.\n'
            '`!disconnect`: disconnect bot from voice channel.\n'
            '`!ping`: Check the bot\'s latency.\n'
            '`!info`: get bot infos.\n'
            '`!como`: get this help menu.\n'

        ),
        inline=False
    )

    # Category: move
    embed.add_field(
        name='**move members**',
        value=(
            '`!aji <@player>`: bring member to current voice channel.\n'
            '`!sir <@player> <voice channel>`: send member to a specific voice channel.\n'
            '`!dini <voice channel>`: send me to a specific voice channel.\n'
            '`!ajiw <@player1> <@player2> <@player3> ..`: bring members to current voice channel.\n'
           
        ),
        inline=False
    )

   # Category: xp
    embed.add_field(
        name='**Levels commands **',
        value=(
            '`!setxp <@player> <number>`: sets xp of a player.\n'
            '`!myxp `: get your xp and level in wlidat.\n'
            '`!getxp <@player>`: get xp and level of a player.\n'
           
        ),
        inline=False
    )

    await ctx.send(embed=embed)





############################################ SHUFFLE COMMAND FOR NEW GAME ##########################################
@bot.command()
async def shuffle(ctx, *names):
    if not names:
        await ctx.send("Please provide a list of names to shuffle.")
        return
    
    names = list(names)
  
    random.shuffle(names)
    
    # image for drawing
    img = Image.new('RGB', (400, 400), color=(73, 109, 137))
    draw = ImageDraw.Draw(img)
    


    font = ImageFont.truetype("ARIAL.TTF", 18)
    
    # radius d circle
    radius = 135
    
    # angle step mabin kola name
    angle_step = 360 / len(names)
    
    for i, name in enumerate(names):
        angle_deg = i * angle_step
        angle_rad = math.radians(angle_deg)
        x = 200 + radius * math.cos(angle_rad)
        y = 200 + radius * math.sin(angle_rad)
        
        # bounding box of the text
        bbox = draw.textbbox((x, y), name, font=font)
        
        # text width and height
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text
        x -= text_width // 2
        y -= text_height // 2
        
        # Draw the text on the image
        draw.text((x, y), name, font=font, fill="white")
    
    # Save the image to a buffer
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    
    img_byte_array.seek(0)
    
    # nsifto db limage to the Discord channel
    await ctx.send(file=discord.File(img_byte_array, filename='shuffled_names.png'))


############################################ START NEW GAME  ##########################################
@bot.command()
async def players(ctx, *args):
    global players
    players = list(args)
    await ctx.send(f"Players list: {', '.join(players)}")

@bot.command()
async def roles(ctx, *args):
    global roles
    roles = list(args)
    await ctx.send(f"Roles list: {', '.join(roles)}")

@bot.command()
async def guru(ctx, player: discord.Member):
    if not players or not roles:
        await ctx.send("Please provide the list of players and roles using !players: and !roles: commands.")
        return
    
    if not player:
        await ctx.send("Please mention a player using !guru: command.")
        return

    if len(players) > len(roles):
        diff = len(players) - len(roles)
        for _ in range(diff):
            roles.append("wlidat")

    if len(players) < len(roles):
        await ctx.send("There are more roles than players. Please adjust the number of roles.")
        return

    shuffled_data = list(zip(players, roles))
    random.shuffle(shuffled_data)

   
    with open("img/wlidat.jpeg", "rb") as file:
        image = discord.File(file)
    
    
    await player.send(file=image)

     # Prepare the text message
    message = "\n \t __**LIST DIAL WLIDAT :**__\n"
    for shuffled_player, shuffled_role in shuffled_data:
        message += f"\t \t {shuffled_player} --> {shuffled_role}\n"
  
     # Send the text message
    await player.send(message)


    await ctx.send(f"Shuffled roles sent to {player.mention}.")




############################################ BOT COMMAND ##########################################

@bot.command()
async def join(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        # deconnecta mn voice channel
        await voice_channel.disconnect()
        await ctx.send("rani aslan kayn fl voice channel malk dayr haka.")

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()



@bot.command()
async def volume(ctx, vol: int):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_channel:
        if 0 < vol <= 100:
            voice_channel.source = discord.PCMVolumeTransformer(voice_channel.source, volume=vol / 100)
            await ctx.send(f"Volume adjusted to {vol}%")
        else:
            await ctx.send("Please provide a volume between 1 and 100.")
    else:
        await ctx.send("I'm not connected to a voice channel.")



@bot.command()
async def reset_volume(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    
    if voice_channel:
        voice_channel.source = discord.PCMVolumeTransformer(voice_channel.source, volume=1.0)
        await ctx.send("Volume reset to 100%")
    else:
        await ctx.send("I'm not connected to a voice channel.")

############################################ WLIDATI THE GAME SOUNDS COMMAND ##########################################
@bot.command()
async def night(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        # ydeconnecta b3da
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

   
    sound_file_path = "wolf.mp3"
    
   
    volume = 0.5

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))


@bot.command()
async def start(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
       
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "teenwolf.mp3"

    
    volume = 0.3

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def night2(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
       
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "forest.mp3"

    
    volume = 0.1

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))




############################################ SOUNDS COMMAND ##########################################
##############################################################################################################################
##############################################################################################################################
@bot.command()
async def cops(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
      
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

  
    sound_file_path = "police.mp3"

   
    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def keddab(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
      
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    sound_file_path = "ayb.mp3"

    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def mii(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    sound_file_path = "mii.mp3"

    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def tom(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    sound_file_path = "tom scream.mp3"

    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def wachouf(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
       
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

   
    sound_file_path = "wa chouf chi chwia ldik jih.mp3"

    
    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def sirt9(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "wa ta sir t9wed.mp3"

   
    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def wlad9(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "wa wlad 9.mp3"

    
    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))


@bot.command()
async def yak(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "yakakhoya.mp3"

    
    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def b9afia(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
       
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "b9afia.mp3"

   
    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def awalan(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
       
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "awalan.mp3"

    
    volume = 0.7

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def alarm(ctx):

    
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
       
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "alarm.mp3"

   
    volume = 0.8

    #while True:
    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))
       

@bot.command()
async def got(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

   
    sound_file_path = "gott.mp3"
    
    
    volume = 0.3

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def birthday(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
        
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "happybirthday.mp3"
    
    
    volume = 0.3

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))


@bot.command()
async def boardgame(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
      
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

    
    sound_file_path = "boardgame.mp3"
    
    
    volume = 0.5

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

@bot.command()
async def amongus(ctx):
    global voice_channel

    if voice_channel is not None and voice_channel.is_connected():
       
        await voice_channel.disconnect()

    channel = ctx.author.voice.channel
    voice_channel = await channel.connect()

   
    sound_file_path = "amongus.mp3"
    
   
    volume = 0.6

    voice_channel.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(sound_file_path), volume=volume))

    #voice_channel.play(discord.FFmpegPCMAudio(sound_file_path))

##############################################################################################################################
##############################################################################################################################




############################################ PLAY SOUNDS COMMAND ##########################################

@bot.command()
async def pause(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_channel.is_playing():
        voice_channel.pause()

@bot.command()
async def resume(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_channel.is_paused():
        voice_channel.resume()

@bot.command()
async def stop(ctx):
    voice_channel = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_channel.is_playing():
        voice_channel.stop()



############################################ MUTE/UNMUTE COMMAND ##########################################


@bot.command()
async def mute(ctx, target_member: discord.Member):
    # Check if the command sender has the "mute members" permission
    if ctx.author.voice and ctx.author.guild_permissions.mute_members:
        voice_channel = ctx.author.voice.channel

        # Check if the bot is in the same voice channel
        if ctx.voice_client and ctx.voice_client.channel == voice_channel:
            # Iterate through members in the voice channel and mute them
            for member in voice_channel.members:
                if member != target_member and not member.bot:  # Mute all except the target member and bots
                    await member.edit(mute=True)
            await ctx.send(f"koulchi fl voice channel t9te3 lih l7es mn ghir {target_member.display_name}.")
        else:
            await ctx.send("khasni nkon fl voice channel a chrif .")
    else:
        await ctx.send("You don't have the 'Mute Members' permission or you are not in a voice channel.")


@bot.command()
async def unmute(ctx):
    # Check if the command sender has the mute_members permission
    if ctx.author.guild_permissions.mute_members:
        # Check if the command sender is in a voice channel
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            # Check if the bot is in the same voice channel
            if ctx.voice_client and ctx.voice_client.channel == voice_channel:
                # Iterate through members in the voice channel and unmute them
                for member in voice_channel.members:
                    if not member.bot:  # Exclude bots from unmuting
                        await member.edit(mute=False)
                await ctx.send("All members in the voice channel have been unmuted.")
            else:
                await ctx.send("khasni nkon fl voice channel a chrif")
        else:
            await ctx.send("khas tconnecta fl voice channel bach tkhdem bhad l command.")
    else:
        await ctx.send("You don't have permission to use this command.")



@bot.command()
async def say(ctx, *, message):
    # Check if the command author is an admin
    if ctx.author.guild_permissions.administrator:
        await ctx.send(message)
        await ctx.message.delete()  # Delete the original command message
    else:
        await ctx.send("You don't have permission to use this command.")


##############################################################################################################################
############################################# MOVE COMMANDS ############################################# 
##############################################################################################################################

#doesnt check if command sender is connected to voice channel
#give voice channel exact name
@bot.command()
async def move(ctx, target_member: discord.Member, target_channel: discord.VoiceChannel):
    # Check if the command sender has the "Move Members" permission
    """move commaaaand."""
    if ctx.author.guild_permissions.move_members:
        # Check if the target user exists
        if target_member:
            # Check if the target voice channel exists
            if target_channel:
                # Get the voice channel by ID to check if it exists
                voice_channel = ctx.guild.get_channel(target_channel.id)

                if voice_channel:
                    # Check if the target user is already in the target voice channel
                    if target_member.voice and target_member.voice.channel == voice_channel:
                        await ctx.send(f"{target_member.display_name} is already in {voice_channel.name}.")
                        return

                    # Check if the target user is connected to any voice channel
                    if target_member.voice:
                        try:
                            await target_member.move_to(voice_channel)
                            await ctx.send(f"{target_member.display_name} has been moved to {voice_channel.name}.")
                        except discord.errors.Forbidden:
                            await ctx.send("I don't have permission to move members.")
                    else:
                        await ctx.send(f"{target_member.display_name} is not connected to any voice channel.")
                else:
                    await ctx.send("Target voice channel does not exist.")
            else:
                await ctx.send("Target voice channel does not exist.")
        else:
            await ctx.send("Target user does not exist.")
    else:
        await ctx.send("You don't have the 'Move Members' permission.")



@bot.command()
async def sir(ctx, target_member: discord.Member, *, target_channel_alias: str):
    # Define a dictionary of channel aliases
    channel_aliases = {
        "game night": "「🕹」GAME NIGHT",
        "bolici ou chefar": "「🕹」Bolici ou chefar",
        "tik tok": "「🕹」TIK TOK",
        "aft": "「💤」AFK",
        "wlidati the game": "👹WLIDATI THE GAME",
        "wlidati 1": "👹WLIDATI 1",
        "wlidati 2": "👹WLIDATI 2",
        "wlidati 3": "👹WLIDATI 3",
        "wlidati 4": "👹WLIDATI 4",
        "wlidati 5": "👹WLIDATI 5",
        "wlidati 6": "👹WLIDATI 6",
        "ma9bara": "👹MA9BARA",
        "brtouch": "「🍆」Brtouch l3chraan",
        "brtouch 2": "「🍆」Brtouch 2.0",
        "l7iban": "「❤」 l7iban",
        "l7iban 3": "l7iban  a trois",
        "movie night": "「🎬」ᴍᴏᴠɪᴇ ɴɪɢʜᴛ",
        "music": "「🎧」ᴍᴜsɪᴄ",
        "coworking": "「💻 」ᴄᴏᴡᴏʀᴋɪɴɢ",
       
    }

    # Check if the command sender has the "Move Members" permission
    if ctx.author.guild_permissions.move_members:
        # Check if the target user exists
        if target_member:
            # Get the target voice channel by alias
            target_channel_name = channel_aliases.get(target_channel_alias.lower())  

            if target_channel_name:
                voice_channel = discord.utils.get(ctx.guild.voice_channels, name=target_channel_name)

                if voice_channel:
                    # Check if the target user has the "View Channel" permission for the target voice channel
                    if voice_channel.permissions_for(target_member).view_channel:
                        # Check if the target user is already in the target voice channel
                        if target_member.voice and target_member.voice.channel == voice_channel:
                            await ctx.send(f"{target_member.display_name} is already in {voice_channel.name} malk malk")
                            return

                        # Check if the target user is connected to any voice channel
                        if target_member.voice:
                            try:
                                await target_member.move_to(voice_channel)
                                await ctx.send(f"{target_member.display_name} has been moved to {voice_channel.name}.")
                            except discord.errors.Forbidden:
                                await ctx.send("I don't have permission to move members.")
                        else:
                            await ctx.send(f"{target_member.display_name} gaa3ma mconnecter f ta chi voice channel pff!")
                    else:
                        await ctx.send(f"{target_member.display_name} does not have 'View Channel' permission for {voice_channel.name}.")
                else:
                    await ctx.send(f"Voice channel '{target_channel_name}' not found.")
            else:
                await ctx.send(f"Alias '{target_channel_alias}' not recognized.")
        else:
            await ctx.send("Target user does not exist.")
    else:
        await ctx.send("You don't have the 'Move Members' permission. hder m3a chi admin")


@bot.command()
async def dini(ctx, *, target_channel_alias: str):
    
    channel_aliases = {
        "game night": "「🕹」GAME NIGHT",
        "bolici ou chefar": "「🕹」Bolici ou chefar",
        "tik tok": "「🕹」TIK TOK",
        "aft": "「💤」AFK",
        "wlidati the game": "👹WLIDATI THE GAME",
        "wlidati 1": "👹WLIDATI 1",
        "wlidati 2": "👹WLIDATI 2",
        "wlidati 3": "👹WLIDATI 3",
        "wlidati 4": "👹WLIDATI 4",
        "wlidati 5": "👹WLIDATI 5",
        "wlidati 6": "👹WLIDATI 6",
        "ma9bara": "👹MA9BARA",
        "brtouch": "「🍆」Brtouch l3chraan",
        "brtouch 2": "「🍆」Brtouch 2.0",
        "l7iban": "「❤」 l7iban",
        "l7iban 3": "l7iban  a trois",
        "movie night": "「🎬」ᴍᴏᴠɪᴇ ɴɪɢʜᴛ",
        "music": "「🎧」ᴍᴜsɪᴄ",
        "coworking": "「💻 」ᴄᴏᴡᴏʀᴋɪɴɢ",
        # Add more aliases as needed
    }

    # Check if the command sender has the "View Channel" permission
    if ctx.author.guild_permissions.view_channel:
        # Get the target voice channel by alias
        target_channel_name = channel_aliases.get(target_channel_alias.lower())  

        if target_channel_name:
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name=target_channel_name)

            if voice_channel:
                # Check if the command sender is already in the target voice channel
                if ctx.author.voice and ctx.author.voice.channel == voice_channel:
                    await ctx.send(f"You are already in {voice_channel.name}.")
                    return

                # Check if the command sender is connected to any voice channel
                if ctx.author.voice:
                    # Check if the command sender has "View Channel" permission for the target voice channel
                    if voice_channel.permissions_for(ctx.author).view_channel:
                        try:
                            await ctx.author.move_to(voice_channel)
                            await ctx.send(f"You have been moved to {voice_channel.name}.")
                        except discord.errors.Forbidden:
                            await ctx.send("I don't have permission to move you to a different channel.")
                    else:
                        await ctx.send(f"You don't have 'View Channel' permission for {voice_channel.name}.")
                else:
                    await ctx.send("You are not connected to any voice channel. Connect first and try again.")
            else:
                await ctx.send(f"Voice channel '{target_channel_name}' not found.")
        else:
            await ctx.send(f"Alias '{target_channel_alias}' not recognized.")
    else:
        await ctx.send("You don't have the 'View Channel' permission to access voice channels.")


@bot.command()
async def aji(ctx, target_member: discord.Member):
    
    try:
        # Check if the command sender is in a voice channel
        if ctx.author.voice:
            target_channel = ctx.author.voice.channel

            # Check if the member is already in the target voice channel
            if target_member.voice and target_member.voice.channel == target_channel:
                await ctx.send(f"{target_member.display_name} is already in {target_channel.name} malk dayr haka!")
                return

            # Check if the target user exists
            if target_member:
                # Check if the target user is connected to a voice channel
                if target_member.voice:
                    # Check if the command sender has the "Move Members" permission
                    if ctx.author.guild_permissions.move_members:
                        try:
                            await target_member.move_to(target_channel)
                            await ctx.send(f"{target_member.display_name} has been moved to {target_channel.name}.")
                        except discord.errors.Forbidden:
                            await ctx.send("I don't have permission to move members.")
                    else:
                        await ctx.send("You don't have the 'Move Members' permission. hder m3a chi admin ")
                else:
                    await ctx.send(f"{target_member.display_name} is not connected to a voice channel pff!")
            else:
                raise BadArgument()
        else:
            await ctx.send("waa rah khas tkon mconnecter f chi voice channel bach tjib chi7d 3ndk baraka mn l3ya9a")
    except BadArgument:
        await ctx.send(f"Member not found.")
 


@bot.command()
async def ajiw(ctx, *members: discord.Member):
    # Check if the command sender is in a voice channel
    if ctx.author.voice:
        target_channel = ctx.author.voice.channel

        # Check if the command sender has the "Move Members" permission
        if ctx.author.guild_permissions.move_members:
            for member in members:
                try:
                    await member.move_to(target_channel)
                    await ctx.send(f"{member.display_name} has been moved to {target_channel.name}.")
                except discord.errors.Forbidden:
                    await ctx.send(f"I don't have permission to move {member.display_name}.")
                except discord.ext.commands.errors.MemberNotFound:
                    await ctx.send(f"Member {member} not found. Moving other members.")
                    continue
        else:
            await ctx.send("You don't have the 'Move Members' permission.")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def kolchi2(ctx):
    # Check if the command sender is in a voice channel
    if ctx.author.voice:
        target_channel = ctx.author.voice.channel

        # Check if the command sender has the "Move Members" permission
        if ctx.author.guild_permissions.move_members:
            # Check if there are members in the command sender's channel
            if target_channel:
                # Get all members in their current voice channel
                members_to_move = [member for member in ctx.author.voice.channel.members if member != ctx.author]

                # Move each member to the command sender's channel if they have "View Channel" permission
                for member in members_to_move:
                    if target_channel.permissions_for(member).view_channel:
                        try:
                            await member.move_to(target_channel)
                            await ctx.send(f"{member.display_name} has been moved to {target_channel.name}.")
                        except discord.errors.Forbidden:
                            await ctx.send(f"I don't have permission to move {member.display_name}.")
                    else:
                        await ctx.send(f"{member.display_name} doesn't have 'View Channel' permission in {target_channel.name}.")
            else:
                await ctx.send("There are no members in your current voice channel.")
        else:
            await ctx.send("You don't have the 'Move Members' permission.")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def kolchi(ctx):
    # Check if the command sender is in a voice channel
    if ctx.author.voice:
        target_channel = ctx.author.voice.channel

        # Check if the command sender has the "Move Members" permission
        if ctx.author.guild_permissions.move_members:
            # Get all voice channels in the server
            all_voice_channels = ctx.guild.voice_channels

            # Move members from other voice channels to the command sender's channel
            for voice_channel in all_voice_channels:
                if voice_channel != target_channel:
                    for member in voice_channel.members:
                        try:
                            await member.move_to(target_channel)
                            await ctx.send(f"{member.display_name} has been moved to {target_channel.name}.")
                        except discord.errors.Forbidden:
                            await ctx.send(f"I don't have permission to move {member.display_name}.")
        else:
            await ctx.send("You don't have the 'Move Members' permission.")
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

##############################################################################################################################
##############################################################################################################################
@bot.command()
async def restart(ctx):
    await ctx.send("Restarting...")
    await bot.close()



@bot.command()
async def ping(ctx):
    
    await ctx.send(f'Ping! Latency: {round(bot.latency * 1000)}ms')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command()
async def goodbye(ctx):
   
    await ctx.send('Goodbye!')

@bot.command()
async def info(ctx):
   
    await ctx.send('waalo makayn mat3ref l code diali mreeewen')







##############################################################################################################################
##############################################################################################################################

class SoundButton(Button):
    def __init__(self, label, sound_path, style=ButtonStyle.grey, emoji=None):
        super().__init__(label=label, style=style, emoji=emoji)
        self.sound_path = sound_path


    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)

        # Check if the bot is already connected to a voice channel
       # if guild.voice_client is not None and guild.voice_client.is_connected():
            #voice_client = guild.voice_client
        #else:

           # Check if the member is not found or is not connected to a voice channel
        if not member or not member.voice or not member.voice.channel:
        
            await interaction.response.send_message(content="You need to be in a voice channel to use this button.", ephemeral=True)
            return
    
        voice_channel = member.voice.channel


         # Check if the bot is already connected to the same voice channel
        if guild.voice_client and guild.voice_client.is_connected() and guild.voice_client.channel == voice_channel:
            voice_client = guild.voice_client
        else:
        # Connect to the voice channel
            voice_client = await voice_channel.connect()


        # Stop the currently playing sound
        voice_client.stop()

        # Get the member who played the sound
        played_by_member = interaction.user.mention

        # Play the selected sound
        voice_client.play(discord.FFmpegPCMAudio(self.sound_path))
        await interaction.response.send_message(content=f"Playing sound: {self.label} by {played_by_member}", ephemeral=False)

class SoundView(View):
    def __init__(self, buttons):
        super().__init__()
        for button in buttons:
            self.add_item(button)

@bot.command()
async def sounds(ctx):
    buttons_group_1 = [
        SoundButton(label="wa mii", sound_path='sounds/mii.mp3',emoji="🎵"),
        SoundButton(label="tom scream", sound_path='sounds/tom scream.mp3', emoji="😱"),
        SoundButton(label="cops", sound_path='sounds/police.mp3', emoji="🚓")
    ]

    buttons_group_2 = [
        SoundButton(label="amongus", sound_path='sounds/amongus.mp3', emoji="🕹️"),
        SoundButton(label="b9a fia", sound_path='sounds/b9afia.mp3', emoji="🤣"),
        SoundButton(label="kedaab", sound_path='sounds/ayb.mp3', emoji="🤨"),
          
    ]

    buttons_group_5 = [
        
        SoundButton(label="Lmonkaar", sound_path='sounds/lahoma hadchi hada monkar.mp3', emoji="😖"),
        SoundButton(label="haayhay", sound_path='sounds/hay hay hay.mp3',emoji="😏"),
        SoundButton(label="Yaak", sound_path='sounds/yakakhoya.mp3', emoji="🔊"),
        
       
    ]

    buttons_group_6 = [
        
        SoundButton(label="la la mabghaytch", sound_path='sounds/mabghaytch.mp3', emoji="🔊"),
        SoundButton(label="b9a fia l7al", sound_path='sounds/b9afia.ogg', emoji="🔊"),
        SoundButton(label="mowgli", sound_path='sounds/mowgli.mp3', emoji="🔊"),
        
    ]

    buttons_group_7 = [
        
        SoundButton(label="Miaaw", sound_path='sounds/MIAW.mp3', emoji="🐱"),
        SoundButton(label="ghandrb mouk", sound_path='sounds/ghandrbmok.mp3',emoji="🫖"),
        SoundButton(label="Hero", sound_path='sounds/hero.mp3', emoji="🤨"),
    ]

   # buttons_group_3 = [
    #    SoundButton(label="ghandrb mouk", sound_path='sounds/ghandrbmok.mp3',emoji="🫖"),
    #    SoundButton(label="awalan", sound_path='sounds/awalan.mp3',emoji="🤌"),
     #   SoundButton(label="wa ta sir ***", sound_path='sounds/wa ta sir t9wed.mp3', emoji="👋"),
        
   # ]

   # buttons_group_4 = [
     #   SoundButton(label="wa wlad **", sound_path='sounds/wa wlad 9.mp3',emoji="🖕"),
      #  SoundButton(label="wa chouf ldik jih", sound_path='sounds/wa chouf chi chwia ldik jih.mp3', emoji="🦶")
        
        
   # ]

    view_group_1 = SoundView(buttons_group_1)
    view_group_2 = SoundView(buttons_group_2)
    view_group_5 = SoundView(buttons_group_5)
    view_group_6 = SoundView(buttons_group_6)
    view_group_7 = SoundView(buttons_group_7)
   # view_group_3 = SoundView(buttons_group_3)
   # view_group_4 = SoundView(buttons_group_4)


    await ctx.send("Sounds Menu", view=view_group_1)
    await ctx.send("", view=view_group_2)
    await ctx.send("", view=view_group_5)
    await ctx.send("", view=view_group_6)
    await ctx.send("", view=view_group_7)
    #await ctx.send("ataansyou **tkhsar lhedra** ‼️", view=view_group_3)
   # await ctx.send("", view=view_group_4)

##############################################################################################################################
##############################################################################################################################


@bot.command()
async def game(ctx):

    buttons_group_1 = [
        SoundButton(label="🌙 Night", sound_path='sounds/forest.mp3'),
        SoundButton(label="wake up", style=ButtonStyle.green, sound_path='sounds/alarm.mp3'),
        SoundButton(label="werewolves", sound_path='sounds/wolf.mp3')
    ]

    view_group_1 = SoundView(buttons_group_1)

    await ctx.send("game Menu", view=view_group_1)




##############################################################################################################################
##############################################################################################################################

@bot.command()
async def music(ctx):
    buttons_group_1 = [
        SoundButton(label="game of thrones", sound_path='sounds/got.mp3', emoji="🐺"),
        SoundButton(label="boardgames", sound_path='sounds/boardgame.mp3', emoji="🃏"),
        
    ]

    view_group_1 = SoundView(buttons_group_1)

    await ctx.send("music Menu", view=view_group_1)


############################################# DISCONNECT COMMAND ############################################# 



@bot.command()
async def disconnect(ctx):
    guild = ctx.guild

    if guild.voice_client is not None and guild.voice_client.is_connected():
        # Disconnect the bot from the voice channel
        await guild.voice_client.disconnect()
        await ctx.send("azul!")
    else:
        await ctx.send("rani aslan makaynch pff!!.")


############################################# start game COMMAND ############################################# 

@bot.command(name='startgame')
async def startgame(ctx):
    # Get the current date and time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

   
    image_path = 'img/wlidati.jpeg'

    # Create an embed
    embed = discord.Embed(title='🕹Game Starting ...', description=f'', color=0x00ff00)

   
    embed.add_field(name='🕰 Current Time', value=current_time, inline=False)

  
    with open(image_path, 'rb') as image_file:
        embed.set_image(url='attachment://wlidati.jpeg')
        image = discord.File(image_file, filename='wlidati.jpeg')


    await ctx.send(file=image, embed=embed)



@bot.command(name='endgame')
async def end_game(ctx):
  
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   
    embed = discord.Embed(title=f'🕹 Game ended at: {current_time}', color=0xFF0000)

    await ctx.send(embed=embed)




############################################# ranking system game COMMAND ############################################# 


# Dictionary to store user XP (user_id: xp)
user_xp = {}

# Dictionary to map XP thresholds to "Wlidat LVL" role names
xp_lvl_roles = {
    0: 'Wlidat LVL0',
    100: 'Wlidat LVL1',
    150: 'Wlidat LVL2',
    250: 'Wlidat LVL3',
    300: 'Wlidat LVL4',
    350: 'Wlidat LVL5',
    400: 'Wlidat LVL6',
    450: 'Wlidat LVL7',
    500: 'Wlidat LVL8',
  
}

# Dictionary to map general XP thresholds to role names
xp_general_roles = {
    0: '0 xp',
    25: '25 xp',
    50: '50 xp',
    75: '75 xp',
    100: '100 xp',
    125: '125 xp',
    150: '150 xp',
    175: '175 xp',
    200: '200 xp',
    225: '225 xp',
    250: '250 xp',
    275: '275 xp',
    300: '300 xp',
    325: '325 xp',
    350: '350 xp',
    375: '375 xp',
    400: '400 xp',
    425: '425 xp',
    450: '450 xp',
    475: '475 xp',
    500: '500 xp',
    525: '525 xp',
    550: '550 xp',
    575: '575 xp',
    600: '600 xp',
    625: '625 xp',
    650: '650 xp',
    675: '675 xp',
    700: '700 xp',
    725: '725 xp',
    750: '750 xp',
    775: '775 xp',
    800: '800 xp',
    825: '825 xp',
    850: '850 xp',
    875: '875 xp',
    900: '900 xp',
    925: '925 xp',
    950: '950 xp',
    975: '975 xp',
    1000: '1000 xp',


}

@bot.command(name='setxp')
async def set_xp(ctx, member: discord.Member, xp: int):
    # Check if the entered XP is a multiple of 5
    if xp % 5 != 0:
        await ctx.send('Please provide an XP value that is a multiple of 5.')
        return

    # Check if the entered XP is within the defined general XP roles
    if xp not in xp_general_roles:
        await ctx.send('Invalid XP value. Please choose from the allowed XP values.')
        return

    # Check if the command sender has the manage_roles permission
    if ctx.author.guild_permissions.manage_roles:
        # Set XP for the specified member
        user_xp[member.id] = xp

        # Remove previous  XP roles
        for role_name in xp_general_roles.values():
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role and role in member.roles:
                await member.remove_roles(role)

        # Remove higher "Wlidat LVL" roles
        for threshold, role_name in xp_lvl_roles.items():
            if xp < threshold:
                break
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if role and role in member.roles:
                await member.remove_roles(role)

        # Assign the corresponding general XP role based on XP
        role_general = discord.utils.get(ctx.guild.roles, name=xp_general_roles[xp])
        if role_general:
            await member.add_roles(role_general)

        # Assign the corresponding "Wlidat LVL" role based on XP
        for threshold, role_name in reversed(list(xp_lvl_roles.items())):
            if xp >= threshold:
                role_lvl = discord.utils.get(ctx.guild.roles, name=role_name)
                if role_lvl:
                    await member.add_roles(role_lvl)
                    await ctx.send(f'Successfully set XP {xp} for {member.display_name} and assigned role {role_name}.')
                    break

    else:
        await ctx.send('You do not have the permission to manage roles')



@bot.command(name='myxp')
async def my_xp(ctx):
    # Get the XP 
    user_id = ctx.author.id
    xp = user_xp.get(user_id, 0)

    # Get the roles related to XP and "Wlidat LVL"
    xp_roles = [role.name for role in ctx.author.roles if role.name.startswith(('0 xp', 'Wlidat LVL'))]


    message = f'Your current XP: {xp} \n Your Wlidat Level: {", ".join(xp_roles)}'

    await ctx.send(message)



@bot.command(name='getxp')
async def get_xp(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    # Get the XP for the specified user
    user_id = member.id
    xp = user_xp.get(user_id, 0)

    # Get the XP-related roles for the specified user
    xp_roles = [role.name for role in member.roles if role.name.startswith(('0 xp', 'Wlidat LVL'))]

    message = f'l XP dial {member.display_name} howa : {xp}\nlevel d wlidat howa : {", ".join(xp_roles)}'
   

    await ctx.send(message)



# BOT_TOKEN

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
bot.run(bot_token)

