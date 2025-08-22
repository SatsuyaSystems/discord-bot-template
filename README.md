# Discord Bot Template

A simple template to build Discord bots fast.

### Overview

| Feature  | Note                                                |
|----------|-----------------------------------------------------|
| Commands | [Add slash/context menu commands](#adding-commands) |
| Events   | [Handle Discord events](#adding-events)             |
| Modals   | [Use UI modals](#adding-modals)                     |
| Tasks    | [Run background tasks](#adding-tasks)               |

Important: Copy/rename `config.yml.example` to `config.yml` and fill in your token before starting.


## Adding Commands

Commands are auto-discovered from `commands/**.py` (subfolders allowed). Create a file that exposes a `Command` class and register handlers on `client.tree`.

Steps:
1) Create `commands/my_feature.py` (copy from `commands/example.py.example` and rename to `.py`).
2) Implement a `Command` class with `__init__(self, client, cfg)` and register your command(s):
	- Slash: `@client.tree.command(name="...")`
	- Context menu: `@client.tree.context_menu(name="...")`
3) Restart the bot. Commands are synced at startup (optionally to a specific guild via `dc.sync_guild` in `config.yml`).

Notes:
- You can organize by folders, e.g. `commands/admin/ban.py` works.
- See `commands/modal_command_example.py.example` for a context-menu command that opens a modal.


## Adding Events

Events are small modules in `events/` that register handlers via a simple registry.

Steps:
1) Create `events/on_message.py` (copy from `events/on_message.py.example` and rename to `.py`).
2) Export an async `setup(client, cfg)` and call `register_event("on_message", handler)` where `handler` is `async def handler(message): ...`.
3) Restart the bot.

Tips:
- Event names follow discord.py’s event names, e.g. `on_message`, `on_member_join`, etc.
- Put any per-event state you need inside `setup` or use the global registry (see `lib/global_registry.py`).


## Adding Modals

Modals live in `modals/` and are auto-loaded. Define a `ui.Modal` subclass and provide an async `setup(client, cfg)` (even if it just logs).

Steps:
1) Create `modals/usernote.py` (copy from `modals/modal_example.py.example` and rename to `.py`).
2) Implement a `discord.ui.Modal` subclass; use fields like `ui.TextInput` and handle `on_submit`.
3) Open the modal from a command, e.g. inside a slash or context-menu handler: `await interaction.response.send_modal(MyModal(...))`.
4) Restart the bot.

See the pairing example: `commands/modal_command_example.py.example` uses `modals/usernote.py` to store notes.


## Adding Tasks

Tasks are background loops discovered from `tasks/**.py`.

Steps:
1) Create `tasks/my_task.py` (copy from `tasks/example.py.example` and rename to `.py`).
2) Implement:
	- `async def task(client, cfg): ...` that waits for readiness and loops as needed.
	- `def register(client, cfg): return task(client, cfg)`
3) Restart the bot. Tasks are scheduled with `asyncio.create_task(...)` at startup.


## Intents

You can adjust the used Discord intents in `main.py` to match your needs.


## Library Reference (short)

- `lib/configuration_file.py` — Loads/saves YAML config (`config.yml`).
- `lib/global_registry.py` — Simple global singleton registry (used to share instances like config).
- `lib/load_commands.py` — Walks `commands/`, imports `.py` files, instantiates `Command(client, cfg)`.
- `lib/load_events.py` — Loads `events/` modules and provides a registry (`register_event`, `handle_event`).
- `lib/load_modals.py` — Imports `modals/` modules and calls their async `setup(client, cfg)`.
- `lib/load_tasks.py` — Imports `tasks/` modules and schedules the coroutine returned by `register(...)`.
