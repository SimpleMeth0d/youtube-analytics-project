from datetime import timedelta
from src.channel import Mixin
import isodate


class PlayList(Mixin):

    def __init__(self, playlist_id):
        """Класс плейлиста"""

        self.playlist_id = playlist_id
        self.data_response = self.get_service().playlists().list(id=playlist_id,
                                                                 part='snippet').execute()

        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        self.title = self.data_response['items'][0]['snippet']['title']
        self.__playlists_data = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                        part='contentDetails,snippet',
                                                                        maxResults=50,
                                                                        ).execute()

        self.__video_ids = [video['contentDetails']['videoId'] for video in self.__playlists_data['items']]
        self.__videos_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                                  id=','.join(self.__video_ids)
                                                                  ).execute()

    def __str__(self):
        return self.playlist_id

    def __repr__(self):
        return f"PlayList({self.playlist_id}, {self.url})"

    @property
    def total_duration(self) -> timedelta:
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста"""
        total_duration = timedelta()

        for video in self.__videos_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration

        return total_duration

    def total_seconds(self):
        """Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста в секундах"""
        return self.total_duration.seconds

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста"""
        result_url = ''
        count_likes = 0

        for video in self.__videos_response['items']:
            if int(video['statistics']['likeCount']) > count_likes:
                count_likes = int(video['statistics']['likeCount'])
                result_url = f"https://youtu.be/{video['id']}"

        return result_url
