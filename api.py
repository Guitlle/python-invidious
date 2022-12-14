import requests
from urllib.parse import urlparse, parse_qs


class InvidiousAPI():

    def __init__(self, url):
        self.url = url

    def get_playlist(self, plid=None, url=None):
        if url:
            urldata = urlparse(url)
            query = parse_qs(urldata.query)
            plid = query['list']
        if plid:
            playlist_response = requests.get(f'{self.url}/api/v1/playlists/{plid}')
            return playlist_response.json()

        return None

    def get_video_data(self, vid=None, url=None):
        if url:
            urldata = urlparse(url)
            query = parse_qs(urldata.query)
            vid = query['v']
        if vid:
            video_response = requests.get(f'{self.url}/api/v1/videos/{vid}')
            return video_response.json()

        return None

    def get_audio(self, vid=None, url=None, video_data=None):
        if video_data is None:
            video_data = self.get_video_data(vid, url)
        if video_data is None:
            return None

        audio_formats = [stream for stream in video_data['adaptiveFormats'] if stream['type'].startswith('audio/mp4')]
        if len(audio_formats) > 0:
            data = audio_formats[-1]
            data['title'] = video_data['title']
            return data

        return None

    def get_playlist_videos(self, plid=None, url=None):
        playlist_data = self.get_playlist(plid, url)
        if playlist_data is None:
            return None
        videos = []
        for video in playlist_data['videos']:
            videos.append(self.get_video_data(video['videoId']))

        return videos, playlist_data

    def get_playlist_audios(self, plid=None, url=None):
        audios = []
        videos, playlist = self.get_playlist_videos(plid, url)
        for video in videos:
            audios.append(self.get_audio(video_data=video))

        return audios, playlist

