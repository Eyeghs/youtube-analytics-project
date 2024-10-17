import sys
import os
import isodate
import json
from datetime import timedelta
from googleapiclient.discovery import build
sys.path.insert(0, '..')


def printj(dict_to_print: dict):
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class PlayList():
    def __init__(self, playlist_id):
        self._playlist_id = playlist_id
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_info = youtube.playlists().list(id=playlist_id, part='snippet',).execute()
        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self._playlist_id
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50,).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = youtube.videos().list(part='contentDetails,statistics', id=','.join(self.video_ids)).execute()

    @property
    def video_id(self):
        """Возвращает id плейлиста."""
        return self._playlist_id

    def printj_info(self):
        return printj(self.playlist_videos)

    def printj_video_in_playlist(self):
        """Выводит в консоль информацию о всех видео в плейлисте."""
        for playlist in self.playlist_videos['items']:
            printj(playlist)

    @property
    def total_duration(self):
        duration_sum = timedelta(0)
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_sum += duration
        return duration_sum

    def show_best_video(self):
        most_likes = 0
        video_id = ''
        for video in self.video_response['items']:
            if int(video['statistics']['likeCount']) > most_likes:
                video_id = 'https://youtu.be/' + video['id']
        return video_id
