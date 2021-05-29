import argparse
import glob
import eyed3


def get_tracks(path):
    return glob.glob(path, recursive=True)


def update_title_tags(track_files):
    for i, track_file in enumerate(track_files):
        track = eyed3.core.load(track_file)
        tag = track.tag
        original_path = '/'.join(track_file.split('/')[:-1])
        new_name = f"{str(tag.track_num[0]).zfill(2)} - {tag.title}"
        tag.title = new_name
        tag.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Re-title a series of mp3 files to "{track_num} - {title}"')
    parser.add_argument('path', metavar='p', type=str, required=True,
                        help='path to your mp3s, can use bash-style globbing')
    args = parser.parse_args()
    track_files = get_tracks(args.path)
    update_title_tags(track_files)
