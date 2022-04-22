import discord
from discord.ext import commands
import os
import yaml
import traceback
import sys
with open("config.yml") as f:
  data = yaml.load(f, Loader=yaml.FullLoader)
try:
  assert "data" in globals()
except Exception:
  print("Something went wrong loading the config!", file=sys.stderr)
  sys.exit(1)


bot = commands.Bot(
  intents = discord.Intents.all(),
  command_prefix = commands.when_mentioned_or(data["prefixes"]),
  help_command = None,
  case_insensitive = True,
  activity = discord.Streaming("!help"),
  status = discord.Status.dnd,
  owner_ids = data["owners"]
)

print("""  ____            _        ____        _   
 |  _ \          (_)      |  _ \      | |  
 | |_) | __ _ ___ _  ___  | |_) | ___ | |_ 
 |  _ < / _` / __| |/ __| |  _ < / _ \| __|
 | |_) | (_| \__ \ | (__  | |_) | (_) | |_ 
 |____/ \__,_|___/_|\___| |____/ \___/ \__|
                                           
 """)

@bot.event
async def on_ready():
  print(f"Logged in as {bot.user.name} ({str(bot.user.id)})")
  
@commands.is_owner()
@bot.command(hidden=True)
async def reload(ctx):
  for file in os.listdir('cogs'):
    if file.endswith('.py'):
      try:
        if f'cogs.{file[:-3]}' in bot.extensions:
          bot.reload_extension(f'cogs.{file[:-3]}')
        else:
          bot.load_extension(f'cogs.{file[:-3]}')
      except Exception:
        traceback.print_exc()
        print("If the bot is unmodified, contact pennacap#0797")
      
for file in os.listdir('cogs'):
    if file.endswith('.py'):
      try:
        bot.load_extension(f'cogs.{file[:-3]}')
      except Exception as e:
        traceback.print_exc()
        print("If the bot is unmodified, contact pennacap#0797")

bot.run(data["token"])
