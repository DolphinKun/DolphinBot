import os
import sys
import importlib

import config

loaded_plugins = {}


def load_plugins(dolphin_bot):
    global loaded_plugins
    sys.path.insert(0, 'plugins')
    for plugin in os.listdir("plugins"):
        if "cache" not in plugin:
            plugin_name = plugin.strip(".py")
            plugin_module = importlib.import_module(plugin_name)
            pm = getattr(plugin_module, "pm")
            plugin_commands = getattr(plugin_module, "commands")
            if config.debug_mode:
                print("[DolphinBot] Loaded plugin: " + plugin_name)
            loaded_plugins[plugin_name] = [plugin_module, plugin_commands, pm]
