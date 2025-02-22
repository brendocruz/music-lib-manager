import os
import sys
from dotenv import load_dotenv

from schemas import TargetArtistSchema
from models import Artist, AlbumType
from jsonfiles import load_json
from typing import cast

SONGS_DIRECTORY  = 'songs'
LYRICS_DIRECTORY = 'lyrics'

def load_library() -> list[Artist]:
	metadata_dir = os.path.expanduser(os.environ['METADATA_DIRECTORY'])
	songs_dir    = os.path.join(metadata_dir, SONGS_DIRECTORY)
	songs_files  = os.listdir(songs_dir)

	songs_paths: list[str] = []
	for file in songs_files:
		abs_path = os.path.join(songs_dir, file)
		songs_paths.append(abs_path)

	songs_data = []
	for path in songs_paths:
		data = load_json(path)
		songs_data.extend(data)

	schema = TargetArtistSchema()
	artists = cast(list[Artist], schema.load(songs_data, many=True))
	return artists

def embed(artists: list[Artist]) -> None:
	print(artists)

def status(artists: list[Artist]) -> None:
	for artist in artists:
		print(artist.name)
		for album_type in AlbumType:
			print("\t", album_type.pluralize().upper())
			for album in getattr(artist, album_type.pluralize()):
				print("\t\t", album.name)


def download(artists: list[Artist]) -> None:
	print(artists)

def handle_command() -> str:
	if len(sys.argv) < 2:
		exit()
	return sys.argv[1]

def main() -> None:
	command = handle_command()

	artists = load_library()
	
	if command == 'download':
		download(artists)
	elif command == 'status':
		status(artists)
	elif command == 'embed':
		embed(artists)
	else:
		raise ValueError('Invalid command')

if __name__ == '__main__':
	load_dotenv()
	main()
