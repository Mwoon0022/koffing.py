import discord
import logging
import os
import itertools
from discord.ext import tasks
from keep_alive import keep_alive
from koff_commands import sets
from urllib.request import Request, urlopen
import pypokedex
import cogs
import json



#‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵


client = discord.Client()
logging.basicConfig(level=logging.INFO)
status = itertools.cycle(['Try ~help', 'kough kough | ~help'])

@client.event
async def on_ready():
    change_status.start()
    print("Bot's up, les gooo")

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

botPrefix = '~'


#‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵


@client.event
async def on_message(msg):

    if msg.content.startswith(botPrefix) and not msg.content.startswith(botPrefix+botPrefix):

        print('e')

        ctx = msg.content.lower()[len(botPrefix):].strip()
        channel = msg.channel

        

        #‿︵‿︵‿︵‿︵‿︵ SETS ‿︵‿︵‿︵‿︵‿︵


        if ctx.startswith('sets '):

          ctx = ctx.split(' ')
          gen = ctx[1]
          poke = ctx[2:]

          if isinstance(poke, list):
              poke = ' '.join(poke)

          print(f'poke: {poke}')

          error = f"**invalid format error**\n```{botPrefix}sets <gen no.> <pokemon>[-forme]```"

          if int(gen.strip()) not in [1 , 2 , 3 , 4 ,5 , 6 , 7 , 8]:
            
            await channel.send(error)
            print('invalid gen')
          else:
            try:
              pypoke = pypokedex.get(name=cogs.pokedebug(poke))
            except:
              print('invalid poke')
              await channel.send(error)

          poke = poke.capitalize()
          if '-' in str(poke):
              enum = (poke.find('-'))
              poke = f'{poke[:enum]}-{poke[enum + 1:].capitalize()}'

          poke = poke.capitalize()
          if ' ' in str(poke):
              enum = (poke.find(' '))
              poke = f'{poke[:enum]} {poke[enum + 1:].capitalize()}'

          if 'keldeo' in poke.lower():
              poke = 'Keldeo'  

          req = Request(f'https://pkmn.github.io/smogon/data/sets/gen{gen}.json', headers={'User-Agent': 'Mozilla/5.0'})
          with urlopen(req) as url:
            sets_data = json.loads(url.read().decode())
          sets_data = sets_data[poke] 

          try:
            ' '.join(poke) #remove gaps if poke is iterable
          except:
            pass


          #‿︵‿︵‿︵‿︵‿︵ DROPDOWN ‿︵‿︵‿︵‿︵‿︵


          class Dropdown(discord.ui.Select):
              def __init__(self):

                  
                  options = [
                      #discord.SelectOption(label='Gen', description=gen, emoji='🟥')
                  ]

                  for key in sets_data.keys():

                    for __set__ in sets_data[key].keys():
                      
                      options.append(discord.SelectOption(label=f"{key} ― {__set__}"))

                  super().__init__(placeholder='Choose a set...', min_values=1, max_values=1, options=options)

              async def callback(self, interaction: discord.Interaction):
                  format_ = self.values[0]
                  battle_format = format_.split(' ― ')[0]
                  set_ = format_.split(' ― ')[1]
                  s = sets_data[battle_format][set_]

                  embed = sets.process(s, format_, poke, interaction.user)

                  await interaction.response.send_message(embed = embed)

          class DropdownView(discord.ui.View):
              def __init__(self):
                  super().__init__()

                  # Adds the dropdown to our view object.
                  self.add_item(Dropdown())
          
          view = DropdownView()

          await channel.send('a', embed = sets.get(sets_data, gen, poke, pypoke, msg.author) , view = view)        


#‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵‿︵


keep_alive()
secwet = os.environ['token']
client.run(secwet)