"""
----------------------------------------------
Program by: Technohamster

Python version:          Year:
        3.9             2022

Thank you for using my program! Good luck)
----------------------------------------------
"""
from pytube import YouTube
from pytube import Playlist, Channel
import os
from termcolor import cprint

import configparser


BLACK_LIST = str.maketrans("", "", "!@#$%^&*_+|+\/:;[]{}<>")


def video_download(link, path):
    try:
        video = YouTube(link)
        print(f'downloading video {video.title}')
        filepath = os.path.join(path, video.title) + '.mp4'
        if not os.path.isfile(filepath):
            video.streams.get_highest_resolution().download(path)
            print('VIDEO DOWNLOADED')
    except Exception as exeption:
        message = f'ERROR: {exeption}'
        cprint(message, 'red')


def playlist_download(link, path):
    try:
        playlist = Playlist(link)
        playlist_name = playlist.title.translate(BLACK_LIST)
        print(f'DOWNLOADING PLAYLIST {playlist_name}')
        if not os.path.exists(os.path.join(path, playlist_name)):
            os.mkdir(os.path.join(path, playlist_name))
        i = 1

        for video in playlist.videos:
            filepath = os.path.join(path, playlist_name, video.title) + '.mp4'
            if not os.path.isfile(filepath):
                print(f'downloading video {i} of {playlist.length} {video.title}')
                video.streams.get_highest_resolution().download(os.path.join(path, playlist_name), filename_prefix=f'{i} ')
            i += 1
        print('PLAYLIST DOWNLOADED')
    except Exception as exeption:
        if exeption == 'regex_search: could not find match for (?:v=|\/)([0-9A-Za-z_-]{11}).*←[0m':
            exeption = 'link issue'
        message = f'ERROR: {exeption}'
        cprint(message, 'red')


def channel_download(path):
    link = input('Enter the link to the channel\n')
    #try:
    channel = Channel(link)

    confirm = input(f'Are you sure you want to download ALL the videos from the "{channel.channel_name}" channel?\n '
                    f'It may take a long time!\n'
                    f'Y or N\n')
    if confirm.upper() == 'Y':
        if not os.path.exists(os.path.join(path, channel.channel_name.translate(BLACK_LIST))):
            os.mkdir(os.path.join(path, channel.channel_name))
        print(f'Downloading videos from the {channel.channel_name} channel')
        i = 1

        for video in channel.videos:
            filepath = os.path.join(path, channel.channel_name, video.title) + '.mp4'
            if not os.path.isfile(filepath):
                print(f'downloading video {i} of {len(channel.videos)} {video.title}')
                video.streams.get_highest_resolution().download(os.path.join(path, channel.channel_name))
            i += 1
    '''except Exception as exeption:
        message = f'ERROR: {exeption}'
        cprint(message, 'red')'''


def check_settings():

    config = configparser.ConfigParser()
    config.read('settings.ini')
    download_path = config['DEFAULT']['download_path']

    if not download_path:
        while True:
            download_path = input('It looks like this is your first time running this program. \n'
                                  'Please set the preferred folder for saving the video.\n')
            if os.path.exists(download_path):
                config['DEFAULT']['download_path'] = download_path
                with open('settings.ini', 'w') as configfile:
                    config.write(configfile)
                break
            else:
                cprint('Such a folder does not exist!', 'red')

    return download_path


def change_settings():
    config = configparser.ConfigParser()

    while True:
        download_path = input('Please set the preferred folder for saving the video.\n')

        if os.path.exists(download_path):
            config['DEFAULT']['download_path'] = download_path
            with open('settings.ini', 'w') as configfile:
                config.write(configfile)
            break
        else:
            cprint('Such a folder does not exist!', 'red')

    return download_path


def add_queue():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    new_link = input()
    while new_link.lower() != 'back':
        config['DEFAULT']['queue'] = config['DEFAULT']['queue'] + '\|/' + new_link
        new_link = input()
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)


def download_queue(path):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    queue_list = config['DEFAULT']['queue'].split('\|/')
    for link in queue_list:
        if 'list=' in link:
            playlist_download(link, path)
        else:
            video_download(link, path)
    config['DEFAULT']['queue'] = ''

    with open('settings.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == '__main__':

    download_path = check_settings()


    while True:
        command = input('Enter the link to the video or playlist\n'
                        'Enter "channel" to download ALL the videos of the channel\n'
                        'Enter "queue" to start downloading from a file with queue \n'
                        'Enter "add" to add links into queue'
                        'Enter "stop" to close the program\n'
                        'Enter "change" to change download path\n')

        if command.lower() == 'queue':
            download_queue(download_path)

        elif command.lower() == 'stop':
            break

        elif command.lower() == 'add':
            print('Enter the links one by one. \n'
                  'To return to the menu, type "back"')
            add_queue()

        elif command.lower() == 'channel':
            channel_download(download_path)

        elif command.lower() == 'change':
            download_path = change_settings()

        else:
            if 'list=' in command:
                playlist_download(command, download_path)
            else:
                video_download(command, download_path)
    quit()
