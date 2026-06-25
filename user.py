import requests
import datetime

bot_credentials = {}

class User:
    '''
    Represents a User.

    Attributes
    ----------
    data: :class:`dict`
        User's data in form of a dictionary.
    '''
    
    EPOCH = 1420070400000
    BASE = 'https://cdn.discordapp.com'

    __slots__ = (
        'name',
        'id',
        'discriminator',
        '_avatar',
        '_banner',
        '_display_name',
        '_accent_color',
        '_guild_avatar',
        'joined_at',
        'permissions',
        '_is_booster',
        'bot',
        '_public_flags',
        '_state'
    )

    def __init__(self, data) -> None:
        for key, _ in data.items():
            if isinstance(data[key], dict):
                self._update(data[key])
                self._update_user_guild_properties(data)
            else:
                self._update(data)
            break

    def _update(self, data):
        self.name = data['username']
        self.id = int(data['id'])
        self.discriminator = data['discriminator']
        self._avatar = data['avatar']
        self._banner = data.get('banner', None)
        self._accent_color = data.get('accent_color', None)
        self.bot = data.get('bot', False)
        self._public_flags = data.get('public_flags', 0)

    def _update_user_guild_properties(self, data):
        self._display_name = data['nick']
        self._guild_avatar = data['avatar']
        self.joined_at = data['joined_at']
        self.permissions = data['permissions']
        self._is_booster = data['premium_since']

    
    @property
    def display_name(self) -> str:
        return self._display_name

    @property
    def mention(self):
        return f'<@{self.id}>'

    @property
    def created_at(self) -> datetime:
        timestamp = ((self.id >> 22) + self.EPOCH) / 1000
        time = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
        return time

    @property
    def avatar_url(self) -> str:
        if self._avatar is not None:
            animated = self._avatar.startswith('a_')
            format = 'gif' if animated else 'png'
            url = f'{self.BASE}/avatars/{self.id}/{self._avatar}.{format}?size=1024'
        else:
            index = int(self.discriminator) % 5
            url = f'{self.BASE}/embed/avatars/{index}.png'
        return url

    def __repr__(self) -> str:
        return f'{self.name}#{self.discriminator}'


def user(token:str = None, id:int = None) -> User:
    '''
    A function that return's an `User` object.

    Parameters
    ----------
    token: :class:`str`
        The bot's token. Needs to be
        passed only during the `Bot`
        class initialisation.
    id: :class:`int` Optional
        The id of the user, whom you
        want to get the details.
    '''
    if token is not None:
        bot_credentials['token'] = token

    url = f"https://discord.com/api/v9/users/{id if id is not None else '@me'}"
    print(url)
    headers = {
        "Authorization": f"Bot {bot_credentials['token']}"
    }
    response = requests.get(url, headers=headers).json()
    print(response)
    return User(response)

