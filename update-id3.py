import argparse
import glob
import re
from collections import Counter

import eyed3


def get_tracks(path):
    return glob.glob(path, recursive=True)


def update_title_tags(track_files):
    albums = []
    for track_file in track_files:
        album_track = eyed3.core.load(track_file)
        album_tag = album_track.tag
        albums.append(album_tag.album)

    album_tracks = Counter(albums)
    print(dict(album_tracks))

    for i, track_file in enumerate(track_files):
        track = eyed3.core.load(track_file)
        tag = track.tag
        title_sections = re.split('\d\d -', tag.title)

        track_current_num = tag.track_num[0] if tag.track_num[0] else 0
        track_current_str = str(track_current_num).zfill(2)
        new_name = f"{track_current_str} - {title_sections[-1].lstrip()}"
        print(f"Saving track title {new_name}")
        tag.title = new_name

        known_max_track = tag.track_num[1] if tag.track_num[1] else dict(album_tracks)[tag.album]
        max_track = known_max_track if known_max_track >= track_current_num else track_current_num
        tag.track_num = (track_current_num, max_track)
        print(f"Saving track number info as ({track_current_num}, {max_track})")
        tag.save()

        curr_cnt = i + 1
        if curr_cnt % 50 == 0:
            print(f'Completed {curr_cnt} of {len(track_files)}')
        if curr_cnt == len(track_files):
            print('Processing complete!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Re-title a series of mp3 files to "{track_num} - {title}"')
    parser.add_argument('path', metavar='p', type=str,
                        help='path to your audio files, can use bash-style globbing')
    args = parser.parse_args()
    track_files = get_tracks(args.path)
    update_title_tags(track_files)
