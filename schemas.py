from marshmallow import Schema, fields, post_dump, post_load, pre_dump, pre_load
from typing import Any

from models import Track, AlbumType, Album, Artist

class TargetTrackSchema(Schema):
	track     = fields.String(required=True)
	number    = fields.Integer(required=True)
	link      = fields.String(required=True)
	lyrics    = fields.String(missing=True)
	overwrite = fields.Boolean(missing=True, load_default=False)
	album     = fields.Nested(lambda: TargetAlbumSchema(exclude=('tracks',)))

	@pre_dump
	def upwrap_track(self, track: Track, **__kwargs__):
		out_data = vars(track).copy()

		# Rename fields.
		value = out_data.pop('name')
		out_data['track'] = value

		return out_data

	@post_load
	def make_track(self, in_data: dict[str, Any], **__kwargs__) -> Track:
		out_data = in_data.copy()

		# Rename fields.
		value  = out_data.pop('track')
		out_data['name'] = value
		return Track(**out_data)

class TargetAlbumSchema(Schema):
	album  = fields.String(required=True)
	type   = fields.Enum(AlbumType, required=True)
	year   = fields.Integer(required=True)
	link   = fields.String()
	tracks = fields.List(fields.Nested(TargetTrackSchema(exclude=('album',))))
	artist = fields.Nested(lambda: TargetArtistSchema(exclude=('albums', 'singles', 'eps')))

	@pre_dump
	def upwrap_album(self, album: Album, **__kwargs__):
		out_data = vars(album).copy()

		# Rename fields.
		value = out_data.pop('name')
		out_data['album'] = value

		return out_data

	@post_load
	def make_track(self, in_data: dict[str, Any], **__kwargs__) -> Album:
		out_data = in_data.copy()

		# Rename fields.
		value  = out_data.pop('album')
		out_data['name'] = value
		album = Album(**out_data) 

		# Setup nested references.
		for track in album.tracks:
			track.album = album
		return album

class TargetArtistSchema(Schema):
	artist   = fields.String(required=True)
	albums   = fields.List(fields.Nested(TargetAlbumSchema, exclude=('artist',)))
	eps      = fields.List(fields.Nested(TargetAlbumSchema, exclude=('artist',)))
	singles  = fields.List(fields.Nested(TargetAlbumSchema, exclude=('artist',)))

	@pre_dump
	def upwrap_artist(self, artist: Artist, **__kwargs__):
		out_data = vars(artist).copy()

		# Rename fields.
		value = out_data.pop('name')
		out_data['artist'] = value

		return out_data

	@post_dump
	def remove_empty_fields(self, in_data: dict[str, Any], **__kwargs__):
		out_data = in_data.copy()
		for album_type in AlbumType:
			if len(in_data[album_type.pluralize()]) == 0:
				out_data.pop(album_type.pluralize())
		return out_data

	@pre_load
	def noname(self, in_data: dict[str, Any], **__kwargs__):
		out_data = in_data.copy()

		for album_type in AlbumType:
			for album in in_data.get(album_type.pluralize(), []):
				album['type'] = album_type.value
		return out_data

	@post_load
	def make_artist(self, in_data: dict[str, Any], **__kwargs__) -> Artist:
		out_data = in_data.copy()

		# Rename fields.
		value  = out_data.pop('artist')
		out_data['name'] = value
		artist = Artist(**out_data)

		# Setup fields.
		for album_type in AlbumType:
			albums: list[Album] = getattr(artist, album_type.pluralize())
			for album in albums:
				album.artist = artist
		return artist
