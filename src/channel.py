import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.data_response = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.data_response['items'][0]['snippet']['title']
        self.description = self.data_response['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(self.data_response['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.data_response['items'][0]['statistics']['videoCount'])
        self.views_count = int(self.data_response['items'][0]['statistics']['viewCount'])

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_name):
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.data_response, file, indent=2)


