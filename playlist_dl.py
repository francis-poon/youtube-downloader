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
    
    
    
    download_instructions[download_type]()
    
    # Step 1: Ask if they want to download from a playlist or video link(s)
    print('Welcome to 25GreenBeans\' YouTube Downloader. Select your download type to begin:')
    count = 0
    for download_type in download_types:
        count += 1
        print(f'\t{count}. {download_type}')
    download_type = download_types[int(input(f'Select 1-{count}: ')) - 1]
    
    # Step 2: Ask what type of file output they would like
    print('Select the file type that you would like to download as:')
    count = 0
    for file_ext in file_extensions:
        count += 1
        print(f'\t{count}. {file_ext}')
    
    # Step 3: Ask where the user would like the output to go
    
    
    # Step 4: Create temporary directory and download
    
    
    # Step 5: If output format was a video, then move tmp dir files into output out dir, else convert files into out dir
    
    
    # Step 6: Cleanup. Remove any tmp directories and files created
    
    

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
    
    return tmp_dir
    
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
    
# Converts file with extention ext_in in input to file with extention ext_out in output
def media_file_conversion(input_dir, output_dir, input_ext, output_ext):
    os.chdir(tmp_dir)
    
    count = 0
    for video in glob.glob('*.' + input_ext):
        count += 1
        mp3_file_name = output_dir + os.path.splitext(os.path.basename(video))[0] + '.' + output_ext
        
        print(f'({count}) {mp3_filename}')
        
        AudioSegment.from_file(video).export(mp3_filename, format=output_ext)
        os.remove(video)
    os.chdir(output_dir)
    
    return count

# TODO: Add a class that uses def __contains__ to make this more elegent
def get_target_tracks_list(target_track_string):
    target_track_string = ''.join(target_track_string.split())
    target_tracks = set()
    
    for entry in target_track_string.split(','):
        if '-' in entry:
            a = entry.split('-')
            for x in range(int(a[0]), int(a[1]) + 1):
                target_tracks.add(x)
        else:
            target_tracks.add(int(entry))

    return target_tracks


main()





























    

