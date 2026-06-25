import threading
import json

from .gateway import DiscordWebsocket
from ._http import HTTP
from .slash import Slash
from .user import user

class Message(dict):
    def __getattr__(self, key):
        try:
            if isinstance(self[key], dict):
                return Message(self[key])
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)


class Bot:
    def __init__(self, command_prefix = '+') -> None:
        self.token = None
        self.command_prefix = command_prefix
        self.status = "dnd"
        self.activity_type = None
        self.activity_name = None
        self.conn = DiscordWebsocket()
        self.http = HTTP(self.token)
        self.slash = None
        ####################
        self.application_id = None
        self.slash_func_names = {}
        ####################
        self.event_func_names = {}
        self.command_func_names = {}
        ####################
        self.identify = {
            'op': 2,
            'd': {
                'token': self.token,
                'properties': {
                    '$os': 'windows',
                    '$browser': 'my_library',
                    '$device': 'my_library'
                },
                'compress': False,
                'large_threshold': 250,
                'presence': {
                    'activities': [{
                        'name': self.activity_name,
                        'type': self.activity_type
                    }],
                    'status': self.status,
                    'afk': False
                },
                'intents': 1 << 9
            }
        }


    def run(self, token):
        self.token = token
        self.identify['d']['token'] = self.token
        self.user = user(self.token)

        self.conn.connect()
        self.conn.ws.on_open = self.on_open
        self.conn.ws.on_error = self.on_error
        self.conn.ws.on_close = self.on_close
        self.conn.ws.on_message = self.on_websocket_message


    def send(self, channel_id, message):
        self.http.send_message(channel_id, message)


    def event(self, func):
        self.event_func_names[func.__name__] = func

    def command(self, func):
        self.command_func_names[func.__name__] = func

    def slash_command(self, *args, **kwargs):
        def inner(func):
            if len(kwargs) + len(args) > 3:
                raise Exception('You can only pass name and description while creating a slash command!')
            if not kwargs.get('description'):
                raise Exception('description is a required parameter!')
            name = func.__name__ if not kwargs.get('name') else kwargs.get('name')
            for command_name in self.slash_func_names:
                if command_name == name:
                    raise Exception('You have already made a slash command with this name!')
            self.slash_func_names[name] = {}
            self.slash_func_names[name]['description'] = kwargs.get('description')
            self.slash_func_names[name]['function'] = func
            if kwargs.get('options'):
                self.slash_func_names[name]['options'] = [option._todict for option in kwargs.get('options')]
        return inner

    def register_slash(self):
        self.slash = Slash(self.token, self.application_id)
        self.slash.create_slash_for_guild(self.slash_func_names)


    def on_error(self, ws, error):
        print(f'Error -> {error}')

    def on_open(self, ws):
        print('Connected with Discord Websocket!\n')

    def on_close(self, ws):
        print('Closed!')

    def on_websocket_message(self, ws, message):
        data = json.loads(message)
        print(json.dumps(data, indent=4))

        op = data['op']
        event_type = data['t']

        if op == 10:
            heartbeat = data['d']['heartbeat_interval']
            keep_alive = threading.Thread(target=self.conn.heartbeating, args=(ws, heartbeat,))
            keep_alive.start()
            ws.send(json.dumps(self.identify))

        if op == 0:
            try:
                if not self.application_id:
                    self.application_id = data['d']['application']['id']
                    self.register_slash()
            except Exception as e:
                print(e)

            if event_type == 'MESSAGE_CREATE':
                if self.event_func_names.get('on_message'):
                    content = data['d']
                    message = Message(content)
                    thread = threading.Thread(target=self.event_func_names.get('on_message'), args=(message,))
                    thread.start()

            if event_type == 'READY':
                if self.event_func_names.get('on_ready'):
                    function = self.event_func_names.get('on_ready')
                    function()


            if event_type == 'INTERACTION_CREATE':
                interaction_name = data['d']['data']['name']
                if self.slash_func_names.get(interaction_name):
                    content = data['d']
                    message = Message(content)
                    self.slash.slash_responder(interaction_name, message)

