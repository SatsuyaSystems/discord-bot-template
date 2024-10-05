import yaml, logging, os, time, discord, pytz, datetime, importlib.util

from colorama import Fore, init
from discord import app_commands

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
commands_dir = 'commands'
for filename in os.listdir(commands_dir):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        module_path = os.path.join(commands_dir, filename)
        
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, 'Command'):
            command_instance = module.Command(client, cfg)
            logging.info(f"Registered command from {filename}")

@client.event
async def on_ready():
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