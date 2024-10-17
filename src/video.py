import sys, os, json
sys.path.insert(0, '..')
from googleapiclient.discovery import build


def printj(dict_to_print: dict):
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
    
    
class Video():

    def __init__(self, video_id: str):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self._video_id = video_id
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=video_id
                                       ).execute()
        self.title = self.video_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=AWX4JnAnjBE' + self.video_id
        self.views_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        
    @property
    def video_id(self):
        """Возвращает id видео."""
        return self._video_id
    
    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        printj(self.video_response)
        
class PLVideo():
    
    def __init__(self, video_id: str, playlist_id: str):
        """
        Экземпляр инициализируется id видео и id плейлиста. 
        Дальше все данные будут подтягиваться по API.
        """
        self._video_id = video_id
        self._playlist_id = playlist_id
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=video_id
                                       ).execute()
        self.title = self.video_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + self.video_id
        self.views_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        
    @property
    def video_id(self):
        """Возвращает id видео."""
        return self._video_id
    
    @property
    def playlist_id(self):
        """Возвращает id видео."""
        return self._playlist_id
    
    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        printj(self.video_response)
        
        