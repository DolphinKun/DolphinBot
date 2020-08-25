import json
import time

import requests
import socketio
from bs4 import BeautifulSoup
import config
import random


class Core:
    def get_ws_server(self):
        socket_info = requests.get("https://cytu.be/socketconfig/" + config.channel + ".json", headers={
            "User-Agent": random.choice(config.user_agents)
        })
        socket_info = json.loads(socket_info.text)
        server_url = socket_info["servers"][0]["url"]
        if "https" in server_url:
            server_url = str(server_url).replace("https", "wss")
        else:
            server_url = str(server_url).replace("http", "ws")
        return server_url

    def connect(self, anon=False):
        self.sio = socketio.Client()
        headers = {
            "User-Agent": random.choice(config.user_agents)
        }
        if config.login_enabled and not anon:
            login_key = self.login()
            headers["Cookie"] = "auth=" + login_key
            if login_key is False:
                print("Error: invalid login!")
                exit()
        server_url = self.get_ws_server()
        self.sio.connect(server_url + '/socket.io', headers=headers)
        self.sio.emit("joinChannel", {"name": config.channel})
        # login
        if not anon:
            self.sio.emit("login", {"name": config.nick})
        # send welcome message
        time.sleep(3)
        if not anon:
            self.sio.emit("chatMsg", {"msg": config.welcome_message, "meta": {}})

    def login(self):
        s = requests.session()
        s.headers = {
            "User-Agent": random.choice(config.user_agents)
        }
        login_page = s.get("https://cytu.be/login").text
        soup = BeautifulSoup(login_page, parser="html.parser", features="lxml")
        form = soup.find("form")
        fields = form.findAll("input")
        form_data = dict((field.get('name'), field.get('value')) for field in fields)
        form_data["name"] = config.nick
        form_data["password"] = config.password
        post_login = s.post("https://cytu.be/login", data=form_data)
        if post_login.cookies["auth"]:
            return post_login.cookies["auth"]
        return False
