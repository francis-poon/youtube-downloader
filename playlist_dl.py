from pytube import Playlist
from pytube import YouTube
import os
import glob
from pydub import AudioSegment


def main():
    download_types = ['Playlist']
    download_type = ''
    download_instructions = {
        'Playlist': playlist_download
    }
    
    print('Welcome to 25GreenBeans\' YouTube Downloader. Select your download type to begin:')
    count = 0
    for download_type in download_types:
        count += 1
        print(f'\t{count}. {download_type}')
    download_type = download_types[int(input(f'Select 1-{count}: ')) - 1]
    
    download_instructions[download_type]()
    

def playlist_download():
    playlist_url = input('\nEntering playlist mode.\n\nPlease enter playlist URL and make sure the playlist is not private.\nURL: ')
    if int(input('Would you like to:\n1. Download all\n2. Download specific songs\nSelect 1 or 2: ')) == 1:
        target_tracks = []
        # TODO: make these inputs loop for user confirmation
        print('Downloading all videos from {playlist title}.')
        # input('Is that correct (Y\N)?: ')
    else:
        target_tracks = get_target_tracks_list(input('Enter the videos that you want to download (ie. 1-3, 5, 8-10, 12, 17): '))
        
    # TODO: Add variable output directory
        
    cur_dir = os.getcwd() + '\\'
    tmp_dir = cur_dir + 'tmp\\'
    output_dir = cur_dir + 'output\\'
    
    print(f'\nCreating temp directory at {tmp_dir} and output directory at {output_dir}')
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
        
    
    playlist = Playlist(playlist_url)
    if len(target_tracks) == 0:
        download_range = range(0, len(playlist.video_urls))
        # TODO: fix these print statements and add to else too
        print(f'Number of videos in playlist: {len(playlist.video_urls)}')
        print('Downloading {end-start+1} videos #{start}-{end}.')
    else:
        start = min(target_tracks)
        end = max(target_tracks)
        max_length = len(playlist.video_urls)
        if start < 1:
            start = 1
        elif start > max_length:
            start = max_length
            
        if end < 1:
            end = 1
        elif end > max_length:
            end = max_length
            
        download_range = range(start - 1, end)

    count = 0
    skipped = 0
    skipped_urls = []
    videos = []
    
    
    video_urls = playlist.video_urls
    print(target_tracks)
    if input('Continue? ') == 'N':
        exit
    for position in download_range:
        if len(target_tracks) != 0 and (position + 1) not in target_tracks:
            continue
        
        url = video_urls[position]
        try:
            video = YouTube(url)
            while video.title == 'YouTube':
                video = YouTube(url)
                
            filename = f'{video.title}'
            count += 1
            print(f'({position + 1}): ' + filename)
            
            video.streams.get_audio_only().download(filename=filename, output_path=tmp_dir)
        except:
            print(f'({position + 1}): Skipped {url}')
            skipped_urls += [url]
            skipped += 1
    
    print(f'{count} videos downloaded, {skipped} skipped.\nSkipped URLs: {skipped_urls}\nBeginning converison to audio...')
    
    os.chdir(tmp_dir)
    extension = '*.mp4'
    count = 0
    for video in glob.glob(extension):
        count += 1
        mp3_filename = output_dir + os.path.splitext(os.path.basename(video))[0] + '.mp3'
        print(f'({count}) {mp3_filename}')
        AudioSegment.from_file(video).export(mp3_filename, format='mp3')
        os.remove(video)
    os.chdir('./..')
        
    print('Conversion completed, removing temp directory.')
    os.removedirs(tmp_dir)
        

# TODO: Add a class that uses def __contains__ to make this more elegent
def get_target_tracks_list(target_track_string):
    target_track_string = ''.join(target_track_string.split())
    target_tracks = []
    
    for entry in target_track_string.split(','):
        if '-' in entry:
            a = entry.split('-')
            for x in range(int(a[0]), int(a[1]) + 1):
                target_tracks += [x]
        else:
            target_tracks += [int(entry)]

    # TODO: make into a set
    list.sort(target_tracks)
    return target_tracks


main()





























    

