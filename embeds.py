import datetime


class _EmptyEmbed:
    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return 'Embed.empty'

    def __len__(self) -> int:
        return 0

EmptyEmbed = _EmptyEmbed()


class Embed:
    '''Represents a Discord Embed

    Attributes
    ----------
    title: :class:`str`
        The title of the Embed
    description: :class:`str`
        The description of the Embed
    color: :class:`int`
        The color of the Embed
    type: :class:`str`
        The type of the embed. Usually "rich".
    timestamp: :class:`datetime.datetime`
        The timestamp of the mebed content.
    url: :class:`str`
        The URL of the Embed.
    '''

    __slots__ = (
        'title',
        'description',
        'color',
        'type',
        'url',
        'timestamp',
        '_fields',
        '_footer',
        '_image',
        '_thumbnail',
        '_video',
        '_provider',
        '_author'
    )
    def __init__(self,
                 title = EmptyEmbed,
                 description = EmptyEmbed,
                 color = EmptyEmbed,
                 timestamp:datetime.datetime = None,
                 url = EmptyEmbed,
                 type:str = 'rich') -> None:

        self.title = title
        self.description = description
        self.color = color,
        self.type = type,
        self.url = url
        
        if timestamp:
            self.timestamp = timestamp

        if self.title is not EmptyEmbed:
            self.title = str(self.title)

        if self.description is not EmptyEmbed:
            self.description = str(self.description)

        if self.url is not EmptyEmbed:
            self.url = str(self.url)

        if self.color is not EmptyEmbed:
            self.color = self.color[0]

    @property
    def to_dict(self) -> dict:
        result = {}

        for key in self.__slots__:
            if key[0] == '_' and hasattr(self, key):
                result[key[1:]] = getattr(self, key)

        if self.type:
            result['type'] = self.type[0]

        if self.description:
            result['description'] = self.description

        if self.title:
            result['title'] = self.title

        if self.url:
            result['url'] = self.url

        if self.color:
            result['color'] = self.color

        try:
            if self.timestamp:
                result['timestamp'] = self.timestamp
        except Exception as e:
            print(e)

        return result

    def set_thumbnail(self, url:str, proxy_url:str = None, height:int = None, width:int = None) -> None:
        self._thumbnail = {'url': url}
        if proxy_url:
            self._thumbnail['proxy_url'] = proxy_url
        if height:
            self._thumbnail['height'] = height
        if width:
            self._thumbnail['width'] = width

    def set_image(self, url:str, proxy_url:str = None, height:int = None, width:int = None) -> None:
        self._image = {'url': url}
        if proxy_url:
            self._image['proxy_url'] = proxy_url
        if height:
            self._image['height'] = height
        if width:
            self._image['width'] = width

    def set_footer(self, text:str, icon_url:str = None, proxy_icon_url:str = None) -> None:
        self._footer = {'text':text}
        if icon_url:
            self._footer['icon_url'] = icon_url
        if proxy_icon_url:
            self._footer['proxy_icon_url'] = proxy_icon_url

    def set_author(self, name:str, url:str = None, icon_url:str = None, proxy_icon_url:str = None) -> None:
        self._author = {'name':name}
        if url:
            self._author['url'] = url
        if icon_url:
            self._author['icon_url'] = icon_url
        if proxy_icon_url:
            self._author['proxy_icon_url'] = proxy_icon_url

    def add_field(self, name:str, value:str, inline:bool = True):
        field = {
            'name':name,
            'value':value,
            'inline':inline
        }

        try:
            self._fields.append(field)
        except AttributeError:
            self._fields = [field]