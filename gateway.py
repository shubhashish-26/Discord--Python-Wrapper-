import json
import time
import threading

import websocket
import random


class DiscordWebsocket:
    GATEWAY_URL = "wss://gateway.discord.gg/?v=9&encoding=json"

    # OP CODES
    DISPATCH = 0
    HEARTBEAT = 1

    def __init__(self):
        self.ws = websocket.WebSocketApp(url=self.GATEWAY_URL)
        self.thread = None


    def heartbeating(self, ws, interval):
        time.sleep((interval/1000)*random.random())
        payload = json.dumps({'op': 1, 'd': None})
        ws.send(payload)
        while True:
            time.sleep(interval/1000)
            ws.send(payload) 

    def connect(self):
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()