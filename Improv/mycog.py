from redbot.core import commands
import random
from redbot.core.bot import Red

class Improv(commands.Cog):
  def __init__(self, bot: Red):
    self.bot = bot

    # variable declaration
    self.improv_channel = '661816778262839304'
    self.last_user = ''
    self.latest_sentence = ''

  # message listener
  @commands.Cog.listener()
  async def on_message(self, message):
    # escape listener if message is not applicable
    if str(message.channel.id) != self.improv_channel:
      return
    if message.author.id == self.bot.user.id:
      return

    # get message content
    message_content = str(message.content)
    print(message_content)
    # save new user
    this_user = str(message.author.id)

    # call improv logic
    message_content_list = message_content.split()
    is_approved = False

    if len(message_content_list) == 1:
      is_approved = True
    
    #deal with people putting punctuation in their 1 word message_content
    temp_punctuation_list = ['?', '!', '.']
    word_length = len(message_content_list[0])
    is_punctuated = False
    for punc in temp_punctuation_list:
      if punc in message_content:
        is_punctuated = True
    if is_punctuated and (word_length > 1):
      is_approved = False
    if message_content == '....':
      is_approved = True
    for punc in temp_punctuation_list:
      if punc == message_content:
        is_approved = True
    if this_user == self.last_user:
      is_approved = False
    if (self.latest_sentence == '') and is_punctuated:
      is_approved = False

    # not approved: delete it
    if not is_approved:
      await message.delete()
      print('Deleted: ' + message_content)
      return

    # detect punctuation, post sentence, and reset saved sentence
    preface_list = ["And Albert Einstein said: ", 'A new scientific study shows that: ', 'Everyone learned this as a child: ', 'Deep in the Mormon scriptures, it tells us that: ', 'The runes reveal the truth that: ', "Scewt signals in sign language: ", "After hours of thought, Godlike realizes that: ", "Haunter's latest tattoo: ", "Scientists have just translated this secret alien message: ", "Linguists have just decoded the Nazis' last secret: ", "Paul Revere rides down the street exclaiming: ", "Steven Hawking's last words: ", "Intelligence has just intercepted Sierra's latest DM to Atmos: ", "Donald Trump approves this message: ", "*swoon* Boy of the week snapped me this: ", "Breaking news: ", "The letters in the alphabet soup form a message: ", "The tag inside of Koala's fursuit says: ", "Tripping on meth, Bryn screams: ", "In feces, Bryn spells out a special message on the bottom of the pool: ", "Linda screams to the Warzone kiddies: "]
    punctuation_list = ['?', '!', '.', '....']
    for punctuation in punctuation_list:
      if message_content == punctuation:
        self.latest_sentence += message_content
        random_preface = random.randint(0, len(preface_list) - 1)
        post_sentence = preface_list[random_preface] + self.latest_sentence
        await message.channel.send(post_sentence)
        self.latest_sentence = ''
        return

    # message is approved, add it to saved sentence
    if len(self.latest_sentence) == 0:
      first_word = message_content[0].upper() + message_content[1:]
      self.latest_sentence = first_word
    else:
      self.latest_sentence += ' ' + message_content
    # save new user as last user
    self.last_user = this_user
    return
