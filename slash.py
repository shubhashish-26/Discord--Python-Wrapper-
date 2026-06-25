import requests

from .embeds import *
from .user import *


class OptionsType:
    SUB_COMMAND       = 1
    SUB_COMMAND_GROUP = 2
    STRING            = 3
    INTEGER           = 4
    BOOLEAN           = 5
    USER              = 6
    CHANNEL           = 7
    ROLE              = 8
    MENTIONABLE       = 9
    NUMBER            = 10


class Interaction:
    API_URL = 'https://discord.com/api/v9'

    def __init__(self, respond_content):
        self.interaction_content = respond_content
        self.user = User(self.interaction_content.member)


    def respond(self, content:str = None, embed=EmptyEmbed):
        url = self.API_URL + f'/interactions/{self.interaction_content.id}/{self.interaction_content.token}/callback'
        json = {
            'type': 4,
            'data': {
                'content': content if content else '',
                'embeds': [embed.to_dict] if embed else [],
            }
        }
        response = requests.post(url, json=json)


class Slash:
    API_URL = 'https://discord.com/api/v9'

    def __init__(self, token, application_id):
        self.token = token
        self.application_id = application_id
        self.commands = None

    def create_slash_for_guild(self, commands:dict):
        url = self.API_URL + f'/applications/{self.application_id}/guilds/729664714518560769/commands'
        self.commands = commands
        headers = {
            'Authorization': f'Bot {self.token}'
        }
        for key, value in self.commands.items():
            try:
                options = value['options']
                print(options)
            except:
                options = []

            payload = {
                'name': key,
                'description': value['description'],
                'options': options
            }

            r = requests.post(url, headers=headers, json=payload)

    def slash_responder(self, name, content):
        try:
            interaction_function = self.commands.get(name).get('function')
            interaction = Interaction(content)
            #################################
            interaction_function(interaction)
        except Exception as e:
            print(e)


class SubcommandGroup:
    def __init__(self, name:str, description:str, options:list):
        self.name = name
        self.description = description
        self.options = options

    @property
    def _todict(self):
        data = {
            'name': self.name,
            'description': self.description,
            'type': OptionsType.SUB_COMMAND_GROUP,
            'options': [option._todict for option in self.options]
        }
        return data


class Subcommand:
    def __init__(self, name:str, description:str, options:list):
        self.name = name
        self.description = description
        self.options = options

    @property
    def _todict(self):
        data = {
            'name': self.name,
            'description': self.description,
            'type': OptionsType.SUB_COMMAND,
            'options': [option._todict for option in self.options]
        }
        return data


class CommandOptions:
    def __init__(self,
                 name:str, 
                 description:str,
                 type:int,
                 required:bool = False, 
                 choices:list = None):
        self.name = name
        self.description = description
        self.required = required
        self.type = type
        self.choices = None

        if choices:
            self.choices = choices

    @property
    def _todict(self):
        data = {
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'required': self.required,
            'choices': [choice._todict for choice in self.choices] if self.choices else []
        }
        return data
        

class Choices:
    def __init__(self, name:str, value:str):
        self.name = name
        self.value = value

    @property
    def _todict(self):
        data = {
            'name': self.name,
            'value': self.value
        }
        return data