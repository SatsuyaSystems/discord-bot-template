import yaml, logging, os, time, discord, pytz, datetime

from colorama import Fore, init
from discord import app_commands

from lib.load_tasks import load_tasks
from lib.global_registry import g_data
from lib.load_commands import load_commands
from lib.configuration_file import ConfigurationFile
from lib.load_events import load_events

cfg = g_data.get_or_create(
    "cfg",
    ConfigurationFile,
    "./config.yml",
)

init(convert=True, autoreset=True)

intents     : discord.Intents           = discord.Intents().all()
client      : discord.Client            = discord.Client(intents=intents,member_cache_flags=discord.MemberCacheFlags.all())
tree        : app_commands.CommandTree  = app_commands.CommandTree(client)
client.tree                             = tree

if not os.path.exists('./logs'):
    os.mkdir('./logs')

logging.basicConfig(
    level= int( cfg.data['bot']['log_level'] ),
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
    await load_events(client, cfg)

    if cfg.data['dc']['sync_guild'] == -1:
        await client.tree.sync() 
    else:
        await client.tree.sync(guild=discord.Object(id=cfg.data['dc']['sync_guild']))
    
    logging.info(f"Bot is ready as {client.user.name}#{client.user.discriminator} ({client.user.id})")

@client.event
async def on_message(msg) -> None:
    if msg.author.id == client.user.id: return

    print( f"{Fore.CYAN}[{datetime.datetime.now(pytz.timezone('Europe/Berlin')).strftime('%H:%M:%S')}] {Fore.RESET}{msg.author.name}: {msg.content}" )

client.run(cfg.data['dc']['token'])