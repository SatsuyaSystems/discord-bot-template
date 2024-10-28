# Discord Bot Template

A simple template to easily create Discord bots. 

### Overview

| Feature       | Note                                         |
|---------------|----------------------------------------------|
| Commands      | [Create new commands](#adding-commands)      |
| Tasks         | [Create Background Tasks](#adding-tasks)     |

> Remember to modify and rename the `config.yml.example` to `config.yml` before you start.


## Adding Commands

To add commands, follow these steps:
1. Create a new command based on the example in the `commands` folder.
2. Place the new command file in the `commands` folder.
3. Restart the bot.

After restarting, you should see the new command in Discord without needing to register anything.
You can use subfolders to manage your Commands, for example `commands/managment/banUser.py` would work.

## Adding Tasks

For tasks such as syncing a database or crawling in the background:
1. Create a new task based on the example in the `tasks` folder.
2. Place the new task file in the `tasks` folder.
3. Restart the bot.

Your task should start running immediately after the bot restarts.

## Intends

You can modify the used Intends in the main.py file as you need them.
