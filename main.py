import aiohttp
import discord
import os
import datetime
import json
import asyncio
from discord.ext import commands
from io import BytesIO
from PIL import Image
from webserver import keep_alive

def is_it_me(ctx):
  return ctx.author.id == 686220733747298448

def get_prefix(client, message):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]
# pfx = "?"
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents.all())
client.remove_command('help')

@client.event
async def on_command_error(ctx, error):
  raise error

black = 0x000000

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"No Nut November!"))
  print('Bot is Ready.')

@client.event
async def on_guild_join(guild):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
  prefixes[f'{guild.id}'] = "="
  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f)

@client.event
async def on_member_join(member):
  channel = client.get_channel(id)
  guild = member.guild
  role = guild.get_role(id)
  embed = discord.Embed(
    title="New Member!",
    description = f"""
Hey **{member.mention}** welcome to **{guild}**!

> First read the rules in <#id>!
> Read more about us in <#id>,
> Go to <#id> to Talk and Hang out!
    """,
    color = discord.Colour.random()
  )
  embed.set_footer(text="Welcome!")
  embed.set_thumbnail(url=member.avatar_url)
  await channel.send(content=member.mention, embed=embed)
  await member.add_roles(role)

@client.event
async def on_member_remove(member):
  channel = member.guild.get_channel(906628171166781560)
  await channel.send(f"**{member}** just Left, Adios.")

deleted = set()
@client.event
async def on_message_delete(message):
  if message.mentions:
    for s in message.mentions:
      if s == message.author:
        return
      elif s == client.user:
        return
      elif message.author == client.user:
        return
      elif message.author == message.author.bot:
        return
      elif s == message.author.bot:
        return
      else:
        await message.channel.send(f"{s.mention} was Ghost Pinged by {message.author.mention}.")
  msg = message.content or message.attachments
  if not message.author.bot == True:
    if not msg == message.attachments:
      deleted.clear()
      deleted.add(message)

@client.command(aliases=['snip'])
async def snipe(ctx):
  if deleted == set():
    await ctx.send("There's nothing to snipe!")
    return
  else:
    for msg in deleted:
      if msg.channel.id == ctx.message.channel.id:
        embed = discord.Embed(timestamp = msg.created_at,
        description = msg.content,
        color = discord.Colour.dark_green())
        embed.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
        await ctx.send(embed=embed)
      else:
        await ctx.send("There's nothing to snipe!")

@client.command()
async def cprefix(ctx, prefix):
  with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)
  prefixes[f'{ctx.guild.id}'] = f"{prefix}"
  with open('prefixes.json', 'w') as f:
    json.dump(prefixes, f)
  await ctx.send(f"The prefix was changed to **{prefix}**")

# HELPMOD
@client.command()
async def help(ctx, command=None):
  if command == None:
    embed = discord.Embed(title="Help Manual", color = discord.Colour.teal())
    embed.add_field(name=f"{get_prefix(client, ctx.message)}help moderation", value="Gives help for Moderation Commands.", inline=True)
    embed.add_field(name=f"{get_prefix(client, ctx.message)}help roles", value="Gives help for Role Commands.", inline=True)
    embed.add_field(name=f"{get_prefix(client, ctx.message)}help others", value="Gives help for other Commands.", inline=True)
    embed.add_field(name=f"{get_prefix(client, ctx.message)}help emojis", value="Gives help for Emoji Commands.", inline=True)
    await ctx.send(embed=embed)
  if command == 'moderation':
    embed = discord.Embed(title="Moderation\nOnly Moderators and above can use these Commands.", color = discord.Colour.teal())
    embed.add_field(name="Purge", value=f"Purges Messages.\nUsage:\n**{get_prefix(client, ctx.message)}purge <amount>**", inline=True)
    embed.add_field(name="Kick", value=f"Kicks a User.\nUsage:\n**{get_prefix(client, ctx.message)}kick <user> <reason>**", inline=True)
    embed.add_field(name="Ban", value=f"Bans a User.\nUsage:\n**{get_prefix(client, ctx.message)}ban <user> <reason>**", inline=True)
    embed.add_field(name="Unban", value=f"Unbans a User.\nUsage:\n**{get_prefix(client, ctx.message)}unban <user>**", inline=True)
    embed.add_field(name="Mute", value=f"Mutes a User.\nUsage:\n**{get_prefix(client, ctx.message)}mute <user> <reason>**", inline=True)
    embed.add_field(name="Unmute", value=f"Unmutes a User.\nUsage:\n**{get_prefix(client, ctx.message)}unmute <user>**", inline=True)
    embed.add_field(name="Lock", value=f"Locks The Channel.\nUsage:\n**{get_prefix(client, ctx.message)}lock <channel>**", inline=True)
    embed.add_field(name="Unlock", value=f"Unlocks A Previously Locked Channel.\nUsage:\n**{get_prefix(client, ctx.message)}unlock <channel>**", inline=True)
    embed.add_field(name="Setnick", value=f"Sets the Nickname of a Member.\nUsage:\n**{get_prefix(client, ctx.message)}setnick <member> <nickname>**", inline=True)
    await ctx.send(embed=embed)
  if command == 'roles':
    embed = discord.Embed(title="Roles\nOnly Moderators and above can use these Commands.", color = discord.Colour.teal())
    embed.add_field(name="Role", value=f"Adds a role to a member. \nUsage:\n**{get_prefix(client, ctx.message)}role <member> <role> [role]**", inline=True)
    embed.add_field(name="Crole", value=f"Creates a Role. \nUsage:\n**{get_prefix(client, ctx.message)}crole <role>**", inline=True)
    embed.add_field(name="Drole", value=f"Deletes a Role. \nUsage:\n**{get_prefix(client, ctx.message)}drole <role>**", inline=True)
    await ctx.send(embed=embed)
  if command == 'others':
    embed = discord.Embed(title="Others\nOnly The Avatar command can be used by everyone.", color = discord.Colour.teal())
    embed.add_field(name="Toggle", value=f"Enable and Disable Commands. \nUsage:\n**{get_prefix(client, ctx.message)}toggle <command>**", inline=True)
    embed.add_field(name="Avatar", value=f"Displays the Avatar of a user. \nUsage:\n**{get_prefix(client, ctx.message)}av <user>**", inline=True)
    embed.add_field(name="Slowmode", value=f"Sets the slowmode in a channel. \nUsage:\n**{get_prefix(client, ctx.message)}slowmode <seconds>**", inline=True)
    embed.add_field(name="Snipe", value=f"Snipes the Last Deleted Message!\nUsage:\n{get_prefix(client, ctx.message)}snipe", inline=True)
    embed.add_field(name="Say", value=f"The Bot Says The Message.\nUsage:\n**{get_prefix(client, ctx.message)}say <message>**", inline=True)
    embed.add_field(name="Membercount", value=f"The Member Count.\nUsage:\n**{get_prefix(client, ctx.message)}membercount**", inline=True)
    embed.add_field(name="Serverinfo", value=f"Gives info about the Server.\nUsage:\n**{get_prefix(client, ctx.message)}sinfo**", inline=True)
    embed.add_field(name="Remind", value=f"A reminder, simple.\nUsage:\n**{get_prefix(client, ctx.message)}remind <time> <task>**", inline=True)
    embed.add_field(name="Wanted", value=f"A Surprise.\nUsage:\n**{get_prefix(client, ctx.message)}wanted <user>**", inline=True)
    await ctx.send(embed=embed)
  if command == 'emojis':
    embed = discord.Embed(title="Emojis\nOnly Moderators with the **Manage Emojis** Permission Can Use These Commands.", color = discord.Colour.teal())
    embed.add_field(name="Emojiadd", value=f"Adds An Emoji To The Server, Make Sure The Max Emoji Limit isn't full!\nUsage:\n**{get_prefix(client, ctx.message)}emojiadd <emojilink> <emojiname>**", inline=True)
    embed.add_field(name='Emojiremove', value=f'Removes an Emoji From The Server.\nUsage:\n**{get_prefix(client, ctx.message)}emojiremove <emoji>**', inline=True)
    await ctx.send(embed=embed)

# PURGE
# @client.command()
# @commands.has_permissions(manage_messages=True)
# async def purge(ctx, amount=1002, member: discord.Member=None,):
#   # if member == None:
#   #   pass
#   amount = amount+1
#   if member is None:
#     await ctx.channel.purge(limit=amount)
#   elif member is not None:
#     await ctx.channel.purge(limit=amount, check=chemck(ctx, member))

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=1002):
  channel = ctx.message.channel
  # messages = []
  #async for message in channel.history(limit=amount + 1):
    # messages.append(message)
  await channel.purge(limit = amount + 1)

# KICK
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked!')

# BAN AND UNBAN
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user:discord.User, *, arg=None):
  if arg == None:
    arg = 'No Reason given.'
  try:
    await ctx.guild.ban(user, reason=arg)
    embed = discord.Embed(description=f"""
✅ ***{user} was Banned.*** | {arg}
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)
  except:
    await ctx.send("I could not ban that user.")

@ban.error
async def banerror(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'''
**Ban**

**How To Use:**
{get_prefix(client, ctx.message)}ban <user> <reason>

**Example Use:**
{get_prefix(client, ctx.message)}ban @-1Doge#9999 Being Unfriendly
    ''')

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, user: discord.User):
  try:
    await ctx.guild.unban(user)
    embed = discord.Embed(description=f"✅ ***{user} was unbanned.***", color = discord.Colour.green())
    await ctx.send(embed=embed)
  except:
    await ctx.send("Not a previously banned member.")

@client.command()
@commands.has_permissions(manage_messages=True)
async def say (ctx, *, arg):
  await ctx.send(arg)

@say.error
async def sayrror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You can't use that you hoe.")

# MUTE COMMAND
@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member : discord.Member, time=None,*, reason=None):
  if time is None:
    time = '5m'
  mute_role = ctx.guild.get_role(id)
  if (member.guild_permissions.administrator):
    return await ctx.send(f"{member} is an Admin so I cannot mute them.")
  else:
    if discord.utils.get(member.roles, name='Muted') is not None:
      await ctx.send(F"{member} is already Muted.")
    else:
      await member.add_roles(mute_role)
      embed = discord.Embed(
      description=f"***✅ {member} was Muted | Reason: {reason}***",
      color = discord.Colour.dark_green())
      await ctx.send(embed=embed)
      def convert(time):
        pos = ['s', 'm', 'h', 'd']

        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

        unit = time[-1]

        if unit not in pos:
          return -1
        try:
          val = int(time[:-1])
        except:
          return -2
        
        return val * time_dict[unit]
      converted_time = convert(time)
      # if converted_time == -1:
      #   await ctx.send("You didn't answer the time correctly.")
      #   return
      # if converted_time == -2:
      #   await ctx.send("The Time must be an integer.")
      #   return
      await asyncio.sleep(converted_time)
      await member.remove_roles(mute_role)
      embed = discord.Embed(description=f"✅ ***{member} was Unmuted.***", color = discord.Colour.green())
      await ctx.send(embed=embed)

@mute.error
async def murror(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f'''
**Mute**

**How To Use:**
{get_prefix(client, ctx.message)}mute <member> <reason>

**Example Use:**
{get_prefix(client, ctx.message)}mute @-1Doge#4337 Breaking The Rules.
    ''')

'''
@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member : discord.Member, timme:int=None,*, reason=None):
  if timme is None:
    timme = 300
  mute_role = ctx.guild.get_role(906860427609272340)
  if (member.guild_permissions.administrator):
    return await ctx.send(f"{member} is an Admin so I cannot mute them.")
  else:
    if discord.utils.get(member.roles, name='Muted') is not None:
      await ctx.send(F"{member} is already Muted.")
    else:
      await member.add_roles(mute_role)
      embed = discord.Embed(
      description=f"***✅ {member} was Muted | Reason: {reason}***",
      color = discord.Colour.dark_green())
      await ctx.send(embed=embed)
      await asyncio.sleep(timme)
      await member.remove_roles(mute_role)
      embed = discord.Embed(description=f"✅ ***{member} was Unmuted.***", color = discord.Colour.green())
      await ctx.send(embed=embed)
'''

@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx,member : discord.Member):
  muterole = ctx.guild.get_role(id)
  if discord.utils.get(member.roles, name='Muted') is None:
    return await ctx.send("That Member is not Muted.")
  else:
    await member.remove_roles(muterole)
    embed = discord.Embed(description=f"✅ ***{member} was unmuted.***",
      color = discord.Colour.green())
    await ctx.send(embed=embed)

@unmute.error
async def unmurror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have the perms to use this command.")

@client.command(aliases=['createrole', 'creater'])
@commands.has_permissions(manage_roles=True) 
async def crole(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'✅ Role `{name}` has been Created.')

@crole.error
async def croleerror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have the perms to use this command.")

@client.command()
@commands.has_permissions(manage_roles=True)
async def drole(ctx, *, role: discord.Role):
    await role.delete()
    await ctx.send(f'✅ Role `{role}` has been Deleted')

@drole.error
async def drror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have the perms to use this command.")

@client.command()
@commands.has_permissions(manage_channels=True)
@commands.cooldown(3,30,commands.BucketType.user)
async def toggle(ctx, *, command):
  command = client.get_command(command)
  if command is None:
    await ctx.send('❌ What sort of Command is even that?')
  if command == 'toggle':
    return await ctx.send("❌ You can't disable toggle idiot.")
  else:
    command.enabled = not command.enabled
    ternary = 'enabled' if command.enabled else 'disabled'
    await ctx.send(f'✅ I have {ternary} {command.qualified_name}.')

#ROLES ADDING AND REMOVING
@client.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx,member: discord.Member,*,input_role):
    input_role = input_role.split(', ')
    server_roles = ctx.guild.roles
    for r in input_role:
        for s in server_roles:
            if s.name.lower().startswith(r.lower()):
                if s not in member.roles:
                    await member.add_roles(s)
                    embed = discord.Embed(description=f"✅ **Added {s.mention} to {member.mention}**")
                    await ctx.send(embed=embed)
                else:
                  await member.remove_roles(s)
                  embed = discord.Embed(description=f"✅ **Removed {s.mention} from {member.mention}**")
                  await ctx.send(embed=embed)

@role.error
async def rolerror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("❌ You don't have the **Manage Role** Perm to use that Command.")

@role.error
async def rolemrror(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"""
**Role**

**How To Use:**
{get_prefix(client, ctx.message)}role <member> <roles>

**Example Use:**
{get_prefix(client, ctx.message)}role @-1Doge#4337 Community
  """)

@client.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.send(f"✅ Set Slowmode To {seconds}!")

@slowmode.error
async def slowmodor(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You don't have the perms to use this command.")

@client.command()
async def wanted(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author

  wanted = Image.open("wanted.jpg")

  asset = member.avatar_url_as(size = 128)
  data = BytesIO(await asset.read())
  profilepic = Image.open(data)

  profilepic = profilepic.resize((117, 117))

  wanted.paste(profilepic, (32, 75))

  wanted.save("wantedpic.jpg")

  await ctx.send(file = discord.File("wantedpic.jpg"))
  os.remove("wantedpic.jpg")

@client.command(aliases=['serverinfo'])
async def sinfo(ctx):
  name = ctx.guild.name
  id = ctx.guild.id
  owner = ctx.guild.owner
  membercount = ctx.guild.member_count
  channels = ctx.guild.text_channels
  voicech = ctx.guild.voice_channels
  roles = ctx.guild.roles
  categories = ctx.guild.categories
  embed = discord.Embed(
    title=name,
    color = discord.Colour.dark_blue()
  )
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Member Count", value=membercount, inline=True)
  embed.add_field(name="Role Count", value=f"{len(roles)}")
  embed.add_field(name="Channel Categoies", value=f"{len(categories)}", inline=True)
  embed.add_field(name="Text Channels", value=f"{len(channels)}", inline=True)
  embed.add_field(name="Voice Channels", value=f"{len(voicech)}", inline=True)
  embed.set_footer(text=f"ID: {id}")
  await ctx.send(embed=embed)

@client.command(aliases=['eadd', 'emadd'])
@commands.has_permissions(manage_emojis=True)
async def emojiadd(ctx, url: str=None, *, name):
  guild = ctx.guild
  async with aiohttp.ClientSession() as ses:
    async with ses.get(url) as r:
      try:
        img_or_gif = BytesIO(await r.read())
        b_value = img_or_gif.getvalue()
        if r.status in range(200, 299):
          emoji = await guild.create_custom_emoji(image=b_value, name=name)
          ternary = f'<a:{name}:{emoji.id}>' if emoji.animated==True else f'<:{name}:{emoji.id}>'
          em = discord.Embed(description=f"✅ Successfully created Emoji {ternary}", color = discord.Colour.green())
          await ctx.send(embed=em)
          await ses.close()
        else:
          em = discord.Embed(description=f"❌ Error when making request | {r.status} response.", color = discord.Colour.red())
          await ctx.send(embed=em)
          await ses.close()
      except discord.HTTPException:
        em = discord.Embed(description=f"❌ File Size is Too Big or Max Emoji Limit Reached.")
        await ctx.send(embed=em)

@client.command(aliases=['eremove', 'emremove'])
@commands.has_permissions(manage_emojis=True)
async def emojiremove(ctx, emoji: discord.Emoji):
  em = discord.Embed(description=f"✅ Successfully deleted Emoji {emoji}")
  await ctx.send(embed=em)
  await emoji.delete()

@client.command()
async def membercount(ctx):
  guild = ctx.guild
  embed=discord.Embed(title="Members", description=guild.member_count, color = discord.Colour.dark_blue())
  await ctx.send(embed=embed)

@client.command(aliases=['avatar'])
async def av(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author
  embed = discord.Embed(
    title = f"{member}'s Avatar!",
    description = "**Avatar**",
    color = discord.Colour.dark_blue()
  )
  embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
  embed.set_image(url=member.avatar_url)

  await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel=None):
  roleneedstobelocked = ctx.guild.get_role(id)
  if channel == None:
    channel = ctx.channel
    await channel.set_permissions(roleneedstobelocked, send_messages=False)
    embed = discord.Embed(title="Channel Locked.", description=f"""
*✅ **{ctx.channel.mention} Has Been Locked!***
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)
  else:
    await channel.set_permissions(roleneedstobelocked, send_messages=False)
    embed = discord.Embed(title="Channel Locked.", description=f"""
*✅ **{channel.mention} Has Been Locked!***
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel=None):
  roleneedstobeunlocked = ctx.guild.get_role(id)
  if channel == None:
    channel = ctx.channel
    await channel.set_permissions(roleneedstobeunlocked, send_messages=True)
    embed = discord.Embed(title="Channel Unlocked.", description=f"""
*✅ **{ctx.channel.mention} Has Been Unlocked!***
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)
  else:
    await channel.set_permissions(roleneedstobeunlocked, send_messages=True)
    embed = discord.Embed(title="Channel Unlocked.", description=f"""
*✅ **{channel.mention} Has Been Unlocked!***
    """, color = discord.Colour.green())
    await ctx.send(embed=embed)

# @client.command()
# @commands.has_any_role(906816175617503272)
# async def sname(ctx, *, gname):
#   guild = ctx.guild
#   embed = discord.Embed(description=f"✅ Server Name Changed from **{guild.name}** to **{gname}**.", color = discord.Colour.green())
#   await ctx.send(embed=embed)
#   await guild.edit(name=gname)

@client.command(aliases=['nickname', 'setnick'])
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member=None, *, nickname):
  if member == None:
    member = ctx.message.author
  try:
    await member.edit(nick=nickname)
    embed = discord.Embed(description=f"✅ Nickname changed to {nickname}", color = discord.Colour.green())
    await ctx.send(embed=embed)
  except:
    return await ctx.send(f"I could not change the name for {member}.")

@nick.error
async def nickerror(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("You need the **Manage Nicknames** Permission to use this Command.")

@client.command(aliases=['remindme', 'rem'])
async def remind(ctx, time, *, task):
  def convert(time):
    pos = ['s', 'm', 'h', 'd']
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
    unit = time[-1]
    if unit not in pos:
      return -1
    try:
      val = int(time[:-1])
    except:
      return -2
    return val * time_dict[unit]
  converted_time = convert(time)
  if converted_time == -1:
    await ctx.send("You didn't answer the time correctly.")
    return
  if converted_time == -2:
    await ctx.send("The Time must be an integer.")
    return
  await ctx.send(f"Reminder set for **{task}**, it will last **{time}**.")
  await asyncio.sleep(converted_time)
  embed = discord.Embed(title="Reminder!", description=f"""
Hey {ctx.author.mention} here's your reminder for **{task}**! [Jump To Original Message]({ctx.message.jump_url})
  """, color = discord.Colour.green(), timestamp = datetime.datetime.now(datetime.timezone.utc))
  await ctx.author.send(embed=embed)
  await ctx.send(f"Check your DMs {ctx.author.mention}")

keep_alive()
TOKEN = os.environ.get("Botto")
client.run(TOKEN)