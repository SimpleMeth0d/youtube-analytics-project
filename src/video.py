import os

from googleapiclient import discovery


API_KEY = os.getenv("YT_API_KEY")

api_service_name = "youtube"
api_version = "v3"

youtube = discovery.build(api_service_name, api_version, developerKey=API_KEY)


class Video:
    """Класс для видео из ютуба"""

    def __init__(self, video_id: str):
        """Экземпляр инициализируется id видео"""
        self.video_id = video_id
        self.video_title = self.get_video_info()['items'][0]['snippet']['title']
        self.video_url = f"https://youtu.be/{video_id}"
        self.view_count = int(self.get_video_info()['items'][0]['statistics']['viewCount'])
        self.like_count = int(self.get_video_info()['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return f'{self.video_title}'

    def get_video_info(self):
        """Получает данные о видео по его id"""
        video_id = self.video_id
        video_info = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
        return video_info


class PLVideo(Video):
    """Дочерний класс от Video"""

    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется 'id видео' и 'id плейлиста'"""
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f'{self.video_title}'


# video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
# video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
# print(video1.get_video_info())
# print(video2.get_video_info())
