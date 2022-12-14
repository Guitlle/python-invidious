import api
import argparse
from urllib.parse import urlparse, parse_qs
import os
import requests


def download_playlist_audios(url, playlist, audios):
    print('Creating output folder, if it already exists the download will be stopped...')
    os.mkdir(playlist['title'])
    os.chdir(playlist['title'])
    print(f'Downloading playlist {playlist["title"]}')
    for audio in audios:
        print(f'Downloading audio for {audio["title"]}')
        download_audio(url, audio)

def download_audio(url, audio_data, audio_format='mp4'):
    filename = f'{audio_data["title"]}.{audio_format}'
    split_parts = audio_data['url'].split('videoplayback?')
    download_url = f'{url}/videoplayback?{split_parts[1]}'
    with requests.get(download_url, stream=True) as data_response:
        with open(filename, 'wb') as f:
            for chunk in data_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog = 'Invidious CLI',
                    description = 'Simple CLI interface for Invidious API')

    parser.add_argument('url')
    parser.add_argument('-d', '--download', help='Download audio(s)', action='store_true')
    parser.add_argument('-v', '--video', help='Download video(s)', action='store_true')
    args = parser.parse_args()

    urldata = urlparse(args.url)
    query = parse_qs(urldata.query)

    url = f'{urldata.scheme}://{urldata.netloc}'
    api = api.InvidiousAPI(url)

    if args.video:
        print('Not supported yet')
        exit()
    elif args.download:
        if urldata.path == '/playlist':
            audios, playlist = api.get_playlist_audios(plid=query['list'][0])
            download_playlist_audios(url, playlist, audios)
        elif urldata.path == '/watch':
            audio = api.get_audio(vid=query['v'])
            download_audio(url, audio)
