import discord
from discord.ext import commands
from core.classes import Cog_

class Remind(Cog_):
  @commands.command()
  async def set_remind(self, ctx, who, when, *, thing):
    pass

def setup(bot):
  bot.add_cog(Remind(bot))