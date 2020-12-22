from redbot.core import commands
from redbot.core.bot import Red
import random
import datetime
from redbot.core import Config
import discord

class randococks(commands.Cog):
  def __init__(self, bot: Red):
    self.bot = bot
    self.config = Config.get_conf(self, identifier=1027)
    self.config.register_global(
      conf_current_month = 13,
      conf_current_seed = 1304
    )

    self.middle_list = ["all-beef thermometer", "21st digit", "Ace in the hole", "Acorn Andy", "Action Jackson", "Adam Halfpint", "Admiral Winky", "African black snake", "Afro man", "AIDS baster", "AIDS grenade", "Alabama blacksnake", "Albino cave dweller", "All-day sucker", "Anaconda", "Anal impaler", "Anal intruder", "Anal Spear", "Ankle spanker", "Apple-headed monster", "Ass blaster", "Ass pirate", "Ass wedge", "Astralgod", "Auger-headed gut wrench", "Baby maker", "Baby's arm holding an apple", "Baby's arm in a boxing glove", "Bacon bazooker", "Bacon rod", "Badboy", "Bagpipe", "Bald Avenger", "Bald butler", "Bald-headed beauty", "Bald-headed giggle stick", "Bald-headed hermit", "Bald-headed Jesus", "Bald-headed yogurt slinger", "Bald-headed spunk-juice dispenser", "Ball buddy", "Baloney pony", "Banana", "Bat and balls", "Battering ram", "Bayonet", "Bavarian Beefstick", "Beard splitter", "Bearded blood sausage", "Bearded burglar", "Beastus maximus", "Beaver buster", "Beaver Cleaver", "Bed snake", "Beef baton", "Beef bayonet", "Beef belt buckle", "Beef bugle", "Beef bus", "Beef missile", "Beef soldier", "Beef stick", "Beefy McManstick", "Bell rope", "Belly stick", "Best leg of three", "(Big) Beanpole", "Big & the twins", "Big us", "Big Jake the one-eyed snake", "Big Jim and the Twins", "Big Johnson", "Big Lebowski", "Big number one", "Big Mac", "Big red", "Big rod", "Big Uncle", "Biggus us", "Bilbo Baggins", "Bishop", "Bishop with his nice red hat", "blaster", "stick", "Bits and pieces", "Blind butler", "Blind snake", "Blinky", "Blood blunt", "Blood slug", "Blood sword", "Blow pop", "Blowtorch", "Blue steel", "Blue-veined jackhammer", "Blue-veined junket pumper", "Blue-veined piccolo", "Blue-veined puss chucker", "Blue-veiner", "Blunt", "Bob", "Bob Dole", "Bob Johnson", "Bobo", "Bone", "Bone phone", "Bone rollercoaster", "Boneless beef", "Boneless fish", "boner", "Boney cannelloni", "Bone-her", "Bookmark", "Bop gun", "Bottle rocket", "Bow-legged swamp donkey", "Box buster", "Boybrush", "Bradford and the pair", "Bratwurst", "Breakfast burrito", "Breakfast wood", "Broom", "Brutus", "Bubba", "Bulbulous big-knob", "Bumtickler", "Bush beater", "Bush rusher", "Bushwhacker", "Buster Hymen", "Buster McThunderstick", "Butt blaster", "Butt pirate", "Butter churn", "Butterknife", "Candy cane", "Canelo", "Caped crusader", "Captain Bilbo", "Captain Crook", "Captain Hook", "Captain Howdy", "Captain Kirk", "Captain Winky", "Carnal stump", "Cattle prod", "Cave hunter", "Cax", "Cervix crusader", "Cervix pounder", "Chancellor", "Chap", "Charlie Russell the one-eyed muscle", "Cheese staff", "Cherry picker", "Cherry poppin' daddy", "Cherry splitter", "Chi Zi Wang", "Chick sticker", "Chicksicle", "Chief of staff", "Chimbo", "Chimney cleaner", "Choo-choo", "Choad (chode)", "Chorizo", "Chowder dumper", "Chubby", "Chubby conquistador", "Chum", "Chunk 'o' love", "Chunder thunder", "Cigar", "Circus boy", "Clam digger", "Clam hammer", "Clam sticker", "Clit tickler", "Cob", "Codger", "Colon cowboy", "Colon crusader", "Colossus", "Coral branch", "Corndog", "Cornholer", "Cornstalk", "Cornstalk cowboy", "Crack hunter", "Crack smacker", "Cramstick", "Crank", "Crank shaft", "Cream-filled meat stick", "Cream bandit", "Cream cannon", "Creamsicle", "Creamstick", "Cream spritzer", "Crimson chitterling", "Crimson Darth Vader", "Crippler", "Crotch cobra", "Crotch cowboy", "Crotch rocket", "Crotch vomiter", "Crushin' Russian", "Cum pump", "Cummingtonite", "Cunny-catcher", "cunt destroyer", "Cupid's arrow", "Curious George", "Custard cannon", "Custard pump", "Cyclops", "Daddy Long-stroke", "Danger the one-e ranger", "Danglin' fury", "Danglin' wang", "Dangling participle", "Dart of love", "Darth Vader", "Davy Crockett", "Deep-veined purple-helmeted spartan of love", "Demeanor", "Diamond cutter", "Digit", "Diller", "Dilly-ho-ho", "Ding-a-ling", "Ding-dong", "Dingaroo", "Dingle", "Dingle dangle", "Dingledong", "Dinglehopper", "Dingus", "Dingy", "Dinky", "Dipstick", "Dirk Diggler", "Divining rod", "Dobber", "Docking tube", "Dog knot", "Dolphin", "Dong", "Dong-bong", "Dong-stick", "Dongle", "Donker", "Donkey Kong", "Doo-dad", "Doo-dar", "Doodle"]
    self.ending_list = ["Now that's a waifu destroyer!", 'Time to stuff some chocolate!', "NOW THAT'S A GACHI STEAK!", 'Woa!', 'Amazing!', 'Sugooiiii', 'OwO!', '[glomps]', 'UwU', 'I wish I had one that big!', 'Kawaii!!!', 'GOOOOLDEN cock!', 'COCKADOODLEDOOOO!!!', 'WAAAAOW', 'Insane!']

  @commands.command()
  async def cock(self, ctx, *args):
    # get seed and month
    saved_month = await self.config.conf_current_month()
    saved_seed = await self.config.conf_current_seed()

    # check for re-roll
    now = str(datetime.datetime.now())
    temp_list = now.split('-')
    new_month = temp_list[1]
    if new_month != saved_month:
      new_seed = random.randint(1, 10000)
      await self.config.conf_current_month.set(new_month)
      await self.config.conf_current_seed.set(new_seed)

      saved_seed = new_seed
      await ctx.send('NEW RANDOM SEED ROLL!!!! CHECK OUT YOUR NEW SIZE FOR THE MONTH!!!!')

    # handle checking someone elses cock
    author_id  = int(ctx.author.id)
    if len(args) != 0:
      target = args[0]
      if target[:3] == '<@!':
        author_id = int(target[3:-1])
      else:
        member = ctx.guild.get_member_named(target)
        if member is None:
          await ctx.send(str(ctx.author.name) + " that isn't a real person. stop being retarded.")
          return
        author_id = member.id

    #user = discord.utils.get(ctx.guild.members, id=str(author_id))
    user = await self.bot.fetch_user(str(author_id))
    random.seed(saved_seed * author_id)
    length = (random.randint(1, 125) * 0.1)
    length_string = "{:.1f}".format(length)
    if length_string[-1] == '0':
      length_string = length_string[:-2]
    random.seed()
    await ctx.send('Looks like ' + user.display_name + "'s " + self.middle_list[random.randint(0, len(self.middle_list) - 1)] + ' is ' + length_string + ' inches long! ' + self.ending_list[random.randint(0, len(self.ending_list) - 1)])
