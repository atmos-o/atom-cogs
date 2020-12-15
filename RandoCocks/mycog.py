from redbot.core import commands
from redbot.core.bot import Red
import random
import datetime

class RandoCocks(commands.Cog):
  def __init__(self, bot: Red):
    self.bot = bot
    self.middle_list = ['has', 'is packing', 'is endowed with', 'wields', 'is hiding']
    self.ending_list = ['rock hard steel.', 'a baby-making wand.', 'waifu-destroying power. OwO', 'man meat. COCKADOODLEDOO!!', 'a manly turkey baster.', 'chocolate stuffing power.', 'GACHI STEAK!']

  @commands.command()
  async def cock(self, ctx):
    # get seed and month
    data_file = open('data.txt', 'r')
    saved_data = data_file.readline()
    saved_data_list = saved_data.split()
    saved_month = saved_data_list[0]
    saved_seed = int(saved_data_list[1])
    data_file.close()

    # check for re-roll
    now = str(datetime.datetime.now())
    temp_list = now.split('-')
    new_month = temp_list[1]
    if new_month != saved_month:
      new_seed = random.randint(1, 10000)
      data_file = open('data.txt', 'w')
      data_file.write(new_month + ' ' + str(new_seed))
      data_file.close()
      saved_seed = new_seed
      await ctx.send('NEW RANDOM SEED ROLL!!!! CHECK OUT YOUR NEW SIZE FOR THE MONTH!!!!')

    author_id  = int(ctx.author.id)
    random.seed(saved_seed * author_id)
    length = (random.randint(1, 135) * 0.1)
    length_string = "{:.1f}".format(length)
    if length_string[-1] == '0':
      length_string = length_string[: -2]
    random.seed()
    await ctx.send(ctx.author.name + ' ' + self.middle_list[random.randint(0, len(self.middle_list) - 1)] + ' ' + length_string + ' inches of ' + self.ending_list[random.randint(0, len(self.ending_list) - 1)])