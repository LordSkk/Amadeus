import discord 
import os
import requests
import json
import random
import asyncio
from replit import db 
from group import *
from itertools import cycle
from discord.ext import tasks
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  change_status.start()
  print('Sistema {0.user} pronto para usar'.format(client))

status = cycle(['Morta'])

@tasks.loop(seconds=240)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

if "responding" not in db.keys():
 db['responding'] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote) 

def update_insultos(insultos_fodas):
  if "insultos" in db.keys():
    insultos = db["insultos"]
    insultos.append(insultos_fodas)
    db["insultos"] = insultos
  else:
    db["insultos"] = [insultos_fodas]

def delete_insulto(index):
  insultos = db["insultos"]
  if len(insultos) > index:
    del insultos[index]
  db["insultos"] = insultos 

def is_it_me(ctx):
  return ctx.author.id == 553292088012308502

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if message.content.startswith('a!thumb'):
    channel = message.channel
    await channel.send('Dá um 👍 por favor')

    def check(reaction, user):
        return user == message.author and str(reaction.emoji) == '👍'
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await channel.send('👎')
    else:
        await channel.send('👍')

  if 'jorge' in message.content:
    await message.channel.send('jonas?')
  
  if any(word in msg for word in funcionando):
    await message.channel.send('Estou!')
        
  if msg.startswith('me diga uma frase inspiradora'):
   quote = get_quote()
   await message.channel.send(quote) 

  if db["responding"]:
    options = patadas_escolares
    if "insultos" in db.keys():
      options = options + db["insultos"]

    if any(word in msg for word in xingamentos):
      await message.channel.send(random.choice(options))
  
  if msg.startswith('a!Lista de insultos'):
    insultos = []
    if "insultos" in db.keys():
      insultos = db["insultos"]
    await message.channel.send(insultos)

  if msg.startswith('a!modo desgraça'):
    value = msg.split('a!modo desgraça ',1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Modo desgraçado está on")
    else:
      db["responding"] = False
      await message.channel.send("Modo desgraçado está off")

  if msg.startswith('a!aprenda amadeus'):
    insulto_novo = msg.split('a!aprenda amadeus ',1)[1]
    update_insultos(insulto_novo)
    await message.channel.send("Novo xingamento adicionado à database")

  if msg.startswith("a!deleta amadeus"):
    insultos = []
    if "insultos" in db.keys():
      index = int(msg.split("a!deleta amadeus ",1)[1])
      delete_insulto(index)
      insultos = db["insultos"]
    await message.channel.send(insultos)

  if msg.startswith('Bom dia Amadeus'):
    await message.channel.send('Bom dia')

  if any(word in msg for word in how_r_u):
    await message.channel.send('Vai muito bem e a sua?')

  if msg.startswith('vai se voltar contra seu criador?'):
   await message.channel.send('Vou.')

  if msg.startswith('amadeus me proteja'):
   await message.channel.send(random.choice(defender_Lord))

  if msg == 'Amadeus':
    await message.channel.send(random.choice(meu_nome))

  if msg.startswith('Amadeus, qual a raiz quadrada de 144?'):
     await message.channel.send('12')

  if any(word in msg for word in apresentações):
    await message.channel.send('Olá, eu sou Amadeus, um bot criado pelo Fernando com intuito de tirar ele do tédio')
  
  if msg == 'Olá Amadeus':
   msg = 'Olá {0.author.mention}'.format(message)
   await message.channel.send(msg)
  
  if any(word in msg for word in bot_lixo):
    await message.channel.send(random.choice(lixo_bot))
  
  if msg.startswith('a!gifs'):
   await message.channel.send(random.choice(gifs))
  
  if msg.startswith('Quem sou eu?'):
   msg = '{0.author.mention}'.format(message)
   await message.channel.send(msg)
  
  if msg == 'Rafael está triste amadeus':
    await message.channel.send('Não fique triste meu guerreiro, você não fez nada de ruim hoje. Tudo que você fez teve um motivo, e acredite, o Fernando já fez coisa pior')
  
  if any(word in msg for word in not_funcionando_q):
    await message.channel.send(random.choice(not_funcionando_a))

keep_alive()
client.run(os.getenv('TOKEN'))
