import os, importlib, logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import discord.Client
    from configuration_file import ConfigurationFile


async def load_modals(client: 'discord.Client', cfg: 'ConfigurationFile') -> None:
    """
    Loads Discord UI modals from the 'modals' directory.
    This function dynamically imports and registers modal classes.
    """
    modals_dir = 'modals'
    if not os.path.exists(modals_dir):
        logging.warning(f"Modals directory '{modals_dir}' not found. Skipping modal loading.")
        return

    for filename in os.listdir(modals_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            # Construct the module name from the file path.
            module_name = filename[:-3]
            try:
                # Dynamically import the module.
                module = importlib.import_module(f'modals.{module_name}')

                # Check if the module has a 'setup' function.
                if hasattr(module, 'setup'):
                    # The setup function should contain the modal class definition
                    # and any necessary registration logic.
                    await module.setup(client, cfg)
                    logging.info(f"Loaded modal module from {filename}")
            except Exception as e:
                logging.error(f"Failed to load modal from {filename}: {e}", exc_info=True)
