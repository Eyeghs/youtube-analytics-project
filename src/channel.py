from googleapiclient.discovery import build
import sys
sys.path.insert(0, '..')
import os, json

def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class Channel:
    """Класс для ютуб-канала"""
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self._channel_id = channel_id
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.channel_id
        self.subscribets_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.views_count = self.channel['items'][0]['statistics']['viewCount']
        
    def __str__(self) -> str:
        """Выводит в консоль информацию о канале."""
        return f"{self.title} {self.url}"
    
    def __add__(self, other):
        """Складывает каналы."""
        if not isinstance(other, Channel):
            raise TypeError('Требуется канал')
        return int(self.subscribets_count) + int(other.subscribets_count)
    
    def __sub__(self, other):
        """Вычитает каналы."""
        if not isinstance(other, Channel):
            raise TypeError('Требуется канал')
        return int(self.subscribets_count) - int(other.subscribets_count)
    
    def __eq__(self, other):
        """Сравнивает каналы."""
        if not isinstance(other, Channel):
            raise TypeError('Требуется канал')
        return self.subscribets_count == other.subscribets_count
    
    def __lt__(self, other):
        """Сравнивает каналы."""
        if not isinstance(other, Channel):
            raise TypeError('Требуется канал')
        return self.subscribets_count < other.subscribets_count
    
    def __le__(self, other):
        """Сравнивает каналы."""
        if not isinstance(other, Channel):
            raise TypeError('Требуется канал')
        return self.subscribets_count <= other.subscribets_count
    
    def __gt__(self, other):
        """Сравнивает каналы."""
        if not isinstance(other, Channel):
            raise TypeError('Требуется канал')
        return self.subscribets_count > other.subscribets_count
    
    def __ge__(self, other):
        """Сравнивает каналы."""
        if not isinstance(other, Channel):
            raise TypeError('Требуется канал')
        return self.subscribets_count >= other.subscribets_count
        
    @property
    def channel_id(self) -> str:
        """Возвращает id канала."""
        return self._channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        printj(self.channel)
        
    @classmethod
    def get_service(cls) -> dict:
        """Получает сервис API."""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
    
    def to_dict(self) -> dict:
        """Сохраняет в словарь значения атрибутов экземпляра `Channel`."""
        return {
            'id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscribets_count': self.subscribets_count,
            'video_count': self.video_count,
            'views_count': self.views_count
        }
    
    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`."""
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent = 4)