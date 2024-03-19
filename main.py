import yaml, logging, os, time, discord, pytz, datetime

from colorama import Fore, init
from discord import app_commands
from lib import startup, database

init(convert=True, autoreset=True)

with open('config.yml', 'r') as file:
    cfg = yaml.safe_load(file)

intents     : discord.Intents           = discord.Intents().all()
client      : discord.Client            = discord.Client(intents=intents,member_cache_flags=discord.MemberCacheFlags.all())
tree        : app_commands.CommandTree  = app_commands.CommandTree(client)
client.tree                             = tree
DB : database.Database = database.Database(client, cfg)

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
    os.system( 'clear' )
    
    logging.info("===================")
    logging.info("hello pterodactyl")
    logging.info("===================")

    startup.register_tasks(client, cfg)
    startup.load_commands(client, cfg)

    await client.tree.sync()

@client.event
async def on_message(msg) -> None:
    if msg.author.id == client.user.id: return

    if msg.channel.id in [952289841947742238,1008742773895209061] and len(msg.attachments) < 1:
        try: await msg.delete()
        except discord.errors.NotFound: pass
        except Exception as err: logging.error( err ) 

    for member in msg.mentions:
        if member.timed_out_until != None:
            # Compare the timed_out_until datetime with the current datetime
            if member.timed_out_until > datetime.datetime.now(pytz.utc):
                await msg.reply(f"<@{member.id}> ist auf der stillen Treppe!")

client.run(cfg['dc']['token'])