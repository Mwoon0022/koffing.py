import pypokedex
import cogs
from db import formats
import discord
import urllib
from db import koffing as koff

bot_icon = 'https://media.discordapp.net/attachments/805074788623056946/887626784873521152/New_Piskel_3.png'
default_colour = discord.Color.from_rgb(222, 31, 63)

  

def get(data, gen, mon, pypoke, author):
    if isinstance(mon, list):
      if len(mon)>1:
        mon = ' '.join(mon)
      else:
        mon = str(mon)
    
    poke = mon.capitalize()
    if '-' in str(poke):
      enum = (poke.find('-'))
      poke = f'{poke[:enum]}-{poke[enum + 1:].capitalize()}'
    if 'keldeo' in poke.lower():
      poke = 'Keldeo'
    sett = data

    set_format = sett.keys()
    formatsFinal = ' | '.join(set_format)
    print(formatsFinal)

    hp_s = pypoke.base_stats[0]
    atk_s = pypoke.base_stats[1]
    def_s = pypoke.base_stats[2]
    spa_s = pypoke.base_stats[3]
    spd_s = pypoke.base_stats[4]
    spe_s = pypoke.base_stats[5]

    embed = sets_embed(title = ' ឵឵  ឵឵  ឵឵  ', text = f"""

 **Formats:** {formatsFinal}

`HP  {str(hp_s).ljust(3)}` {cogs.stats(hp_s)}
`ATK {str(atk_s).ljust(3)}` {cogs.stats(atk_s)}
`DEF {str(def_s).ljust(3)}` {cogs.stats(def_s)}          
`SPA {str(spa_s).ljust(3)}` {cogs.stats(spa_s)} 
`SPD {str(spd_s).ljust(3)}` {cogs.stats(spd_s)}
`SPE {str(spe_s).ljust(3)}` {cogs.stats(spe_s)}
 ឵឵  ឵឵  ឵឵  
""", thumbnail = f"https://www.smogon.com/dex/media/sprites/xy/{mon.lower()}.gif", header = f'#{pypoke.dex} ─ {poke}', author = author)

    return embed

def sets_embed(**kwargs):
    title = kwargs.get('title',"default")
    text = kwargs.get('text',"default")
    thumbnail = kwargs.get('thumbnail', bot_icon)
    header = kwargs.get('header', False)
    icon = "https://cdn2.bulbagarden.net/upload/9/93/Bag_Pok%C3%A9_Ball_Sprite.png"
    author = kwargs.get('author', False)

    embed = discord.Embed(title = title, description = text, color=default_colour)
    embed.set_thumbnail(url = thumbnail)
    if header:
      embed.set_author(name=f'{header}', icon_url=f"{icon}")
    if author:
      embed.set_footer(text = f"{koff.name} v{koff.version} │ requested by {author}", icon_url = bot_icon)

    return embed

def process(s, format_, poke, author):

  try:
    moves = s["moves"]
    moves_f = []
    if type(moves) == type('e'):
      moves_f = f'{moves}'
    else:
      for x in moves:
        x = str(x).replace(',', ' / ')
        x = x.replace("'", '')
        x = x.replace('"', '')
        x = x.replace('[', '')
        x = x.replace(']', '')
        x = x.capitalize()
        moves_f.append(f'{x}')

      moves = '\n'.join(moves_f)

  except KeyError as k: 
    print(k)
    moves = 'not given'

  try: 
    item = s["item"]
    itemOne = item
    if isinstance(item, list):
      itemOne = item[1]
      if isinstance(itemOne, list):
        itemOne = itemOne[1]
    if isinstance(item,list):
      item = ' \ '.join(item)
    print(f'item one - {itemOne}')
  except KeyError as k: 
    print(k)

    item = '-'
    itemOne = 'gold-bottle-cap'

  try:
    nature = s["nature"]
    if isinstance(nature,list):
      nature = ' \ '.join(nature)
  except KeyError as k: 
    print(k)
    nature = '-'

  try:
    ability = s["ability"]
    if isinstance(ability,list):
      ability = ' \ '.join(ability)
    ability = f'\n`Ability` {ability}'
  except KeyError as k: 
    print(k)
    ability = ''

  try:
    ivs = cogs.iev(s["ivs"], 'i')
    print(ivs)
    ivs = f'\n{ivs}'
  except KeyError as k: 
    print(k)
    ivs = ''
  
  try:
    evs = cogs.iev(s["evs"], 'e')
    print(evs)
    evs = f'\n{evs}'
  except KeyError as k: 
    print(k)
    evs = ''  


  embed = discord.Embed(description = f"""\n
`Item` {item}{ability}
`Nature` {nature}{ivs}{evs}
```
{moves}```""", color = default_colour )

  embed.set_footer(text = f'requested by {author}')
  embed.set_thumbnail(url = f"https://img.pokemondb.net/sprites/items/{itemOne.lower().replace(' ', '-')}.png")
  embed.set_author(name = f'{poke} - {format_}', icon_url = 'https://archives.bulbagarden.net/media/upload/9/93/Bag_Pok%C3%A9_Ball_Sprite.png')

  return embed







  
        
