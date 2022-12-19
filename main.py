import discord
from os import environ

from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


game_sessions = {}

@client.event
async def on_message(message):
  # Check if the message is a command to join the game
  if message.content.startswith('!join'):
    # Check if the user is already in a game session
    if message.author in game_sessions:
      await message.channel.send('You are already in a game session!')
      return
    
    # Check if there are any open game sessions
    open_session = None
    for session in game_sessions.values():
      if len(session) < 2:
        open_session = session
        break
    
    # If there are no open sessions, create a new one
    if open_session is None:
      open_session = []
      game_sessions[len(game_sessions)] = open_session
    
    # Add the user to the game session
    open_session.append(message.author)
    await message.channel.send(f'{message.author.mention} has joined the game!')
    
    # If the session is full, start the game
    if len(open_session) == 2:
      await message.channel.send('The game has started!')

load_dotenv()
token = environ["TOKEN"]
client.run(token)