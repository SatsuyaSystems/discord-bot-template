import yaml, logging, os, time, discord, pytz, datetime, importlib.util

from colorama import Fore, init
from discord import app_commands

from lib.load_tasks import load_tasks
from lib.load_commands import load_commands

init(convert=True, autoreset=True)

with open('config.yml', 'r') as file:
    cfg = yaml.safe_load(file)

intents     : discord.Intents           = discord.Intents().all()
client      : discord.Client            = discord.Client(intents=intents,member_cache_flags=discord.MemberCacheFlags.all())
tree        : app_commands.CommandTree  = app_commands.CommandTree(client)
client.tree                             = tree

if not os.path.exists('./logs'):
    os.mkdir('./logs')

logging.basicConfig(
    level= int( cfg['bot']['log_level'] ),
    format= (f'[%(asctime)s] {Fore.YELLOW} {"[%(levelname)s]":7} {Fore.RESET} %(message)s'),
    handlers=[
        logging.FileHandler(f"./logs/{  time.strftime('%Y-%m-%d_%H_%M_%S') }.log",'w','utf-8'),
        logging.StreamHandler()
    ]
)


@client.event
async def on_ready():
    await load_tasks(client, cfg)
    await load_commands(client, cfg)
    
    logging.info(f"Bot is ready as {client.user.name}#{client.user.discriminator} ({client.user.id})")

    if cfg['dc']['sync_guild'] != -1:
        await client.tree.sync() 
    else:
        client.tree.sync_guild(guild=discord.Object(id=cfg['dc']['sync_guild']))

@client.event
async def on_message(msg) -> None:
    if msg.author.id == client.user.id: return

    for member in msg.mentions:
        if member.timed_out_until != None:
            # Compare the timed_out_until datetime with the current datetime
            if member.timed_out_until > datetime.datetime.now(pytz.utc):
                await msg.reply(f"<@{member.id}> ist auf der stillen Treppe!")

client.run(cfg['dc']['token'])