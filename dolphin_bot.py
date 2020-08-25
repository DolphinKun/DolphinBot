import time

import config
import core
import plugins


class DolphinBot(core.Core):
    def call_plugin(self, plugin_function, plugin_name, data):
        module = getattr(plugin_function, plugin_name)
        module(self, data)

    def __init__(self):
        self.anon_mode = False
        self.muted = False
        self.start_time = int(time.time())
        self.connect(self.anon_mode)
        self.flood_prevention = []
        # plugin time!
        plugins.load_plugins(self)
        self.loaded_plugins = plugins.loaded_plugins

        @self.sio.on("chatMsg")
        def chat_msg(data, dolphinbot=self):
            if data["username"] == config.nick or data["username"] in self.flood_prevention:
                return False
            if self.muted:
                return False
            self.flood_prevention.append(data["username"])
            command = str(data["msg"]).split(" ")[0]
            for plugin_name, plugin_data in self.loaded_plugins.items():
                skip_command = False
                if not len(plugin_data[1]):
                    skip_command = True
                if command in plugin_data[1] or skip_command == True:
                    if plugin_data[2] is False:
                        self.call_plugin(plugin_data[0], plugin_name, data)
            time.sleep(3)
            self.flood_prevention.remove(data["username"])

        @self.sio.on("pm")
        def pm(data, dolphinbot=self):
            if data["username"] == config.nick or data["username"] in self.flood_prevention:
                return False
            self.flood_prevention.append(data["username"])
            command = str(data["msg"]).split(" ")[0]
            for plugin_name, plugin_data in self.loaded_plugins.items():
                skip_command = False
                if not len(plugin_data[1]):
                    skip_command = True
                if command in plugin_data[1] or skip_command is True:
                    if plugin_data[2] is True:
                        self.call_plugin(plugin_data[0], plugin_name, data)
            self.flood_prevention.remove(data["username"])

        @self.sio.on("addUser")
        def add_user(data, dolphinbot=self):
            if data["name"] == config.nick:
                return False
            if self.muted:
                return False
            for plugin_name, plugin_data in self.loaded_plugins.items():
                if hasattr(plugin_data[0], plugin_name + "_user_join"):
                    self.call_plugin(plugin_data[0], plugin_name + "_user_join", data)

    def send_message(self, message="", send_to=""):
        if send_to != "":
            message = send_to + ": " + message
            if self.anon_mode:
                return False
        self.sio.emit("chatMsg", {"msg": message, "meta": {}})

    def send_pm(self, send_to="", message=""):
        if self.anon_mode:
            return False
        self.sio.emit("pm", {"to": send_to, "msg": message, "meta": {}})

    def send_alert(self, message):
        self.send_message("[DolphinBot] " + str(message))
