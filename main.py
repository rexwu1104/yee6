import discord
import os
import json
import datetime
from discord.ext import commands
from keep_alive import keep_alive as k

bot = commands.Bot(command_prefix = 'yee ')
bot.remove_command("help")

def check(ctx):
  return ctx.author.guild_permissions.administrator == True or ctx.author.id == 606472364271599621

@bot.event
async def on_ready():
  status = discord.Streaming(name="yee help", url="https://www.twitch.tv/yee6discord")
  await bot.change_presence(activity=status)
  print("yee~~~~~")

@bot.event
async def on_message_delete(msg):
  with open("deleted_message.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)
  jdata[str(msg.channel.id)] = [msg.content, msg.author.mention]
  with open("deleted_message.json", "w", encoding="utf8") as jfile:
    json.dump(jdata, jfile)

@bot.command()
async def gay(ctx, name=None):
  await ctx.message.delete()
  if name is not None:
    try:
      mention = name.strip('<').strip('@').strip('!').strip('>').strip('&')
      await ctx.send(f"i agree {bot.get_user(int(mention)).mention} is gay")
    except:
      members = ctx.guild.members
      for member in members:
        if member is not None:
          if member.nick is not None:
            if (name in member.nick or name in member.name) and member != bot.user:
              await ctx.send(f"i agree {member.mention} is gay")
            elif member == bot.user:
              await ctx.send(f"no you are gay {ctx.author.mention}")
          elif name in member.name:
            await ctx.send(f"i agree {member.mention} is gay")

@bot.command()
async def help(ctx, cmd=None):
  await ctx.message.delete()
  embed = discord.Embed(color=0xffffff, timestamp=datetime.datetime.utcnow())
  if cmd is None:
    embed.set_author(name=f"help\n使用者: {ctx.message.author.name}")
    embed.add_field(name="gay", value="指定一位人為gay\n最好用mention\n用名子也行")
    embed.add_field(name="snipe", value="查看當前頻道最後一個被刪除的訊息")
    embed.add_field(name="poll", value="舉行投票(總共可以二十個選項)(管理員專用)")
    embed.add_field(name="say", value="講話(管理員專用)")
  elif cmd == "gay":
    embed.set_author(name="gay")
    embed.add_field(name="使用方法:", value="yee gay <name>")
  elif cmd == "snipe":
    embed.set_author(name="snipe")
    embed.add_field(name="使用方法:", value="yee snipe")
  elif cmd == "poll":
    embed.set_author(name="poll")
    embed.add_field(name="使用方法:", value="yee poll <title> <choice...>")
  elif cmd == "say":
    embed.set_author(name="say")
    embed.add_field(name="使用方法:", value="yee say <message>")
  await ctx.send(embed=embed)

@bot.command()
async def snipe(ctx):
  await ctx.message.delete()
  with open("deleted_message.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)
  if jdata[str(ctx.message.channel.id)] is not None:
    embed = discord.Embed(color=0x102938, timestamp=datetime.datetime.utcnow())
    embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator)
    embed.add_field(name="被刪除的訊息:", value=jdata[str(ctx.message.channel.id)][0])
    embed.add_field(name="發出訊息的人的人:", value=jdata[str(ctx.message.channel.id)][1])
    await ctx.send(embed=embed)

@bot.command()
@commands.check(check)
async def poll(ctx, title, *, choice):
  await ctx.message.delete()
  embed = discord.Embed(color=0x000000, timestamp=datetime.datetime.utcnow())
  with open("emoji.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)
  if choice is not None:
    choices = choice.split()
    times = 0
    text = str()
    for emoji in jdata:
      choices[times] = [choices[times]]
      choices[times].append(emoji)
      times += 1
      if times == len(choices):
        break
    times = 0
    for choice, emoji in choices:
      text += emoji + " " + choice + "\n"
      times += 1
      if times == len(choices):
        break
    times = 0
    embed.set_author(name=text)
    msg = await ctx.send("**" + title + "**", embed=embed)
    for emoji in jdata:
      await msg.add_reaction(emoji)
      times += 1
      if times == len(choices):
        break

@bot.command()
@commands.check(check)
async def say(ctx, *, msg):
  await ctx.message.delete()
  embed = discord.Embed(color=0x192480)
  embed.set_author(name=ctx.author.name + "#" + ctx.author.discriminator)
  embed.add_field(name="輸入的訊息:", value=msg)
  await ctx.send(embed=embed)
      
@bot.command()
@commands.is_owner()
async def invite(ctx):
  await ctx.message.delete()
  for guild in bot.guilds:
    invites = await guild.invites()
    for invite in invites:
      await ctx.author.send(invite.url)
      break

for filen in os.listdir('./cmds'):
	if filen.endswith('.py'):
		bot.load_extension(f'cmds.{filen[:-3]}')

k()
bot.run("NzE1NzMxMjYzMzQ4Mjc3Mjc4.XtBetg.b53KAakkL451aA7gxBtw0lCh1Hc")