import json
import os
from googleapiclient.discovery import build


class Mixin:
    @classmethod
    def get_service(cls):
        """Получение информации о сервисе"""
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube


class Channel(Mixin):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.data_response = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.data_response['items'][0]['snippet']['title']
        self.description = self.data_response['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(self.data_response['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.data_response['items'][0]['statistics']['videoCount'])
        self.views_count = int(self.data_response['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.data_response, file, indent=2)


