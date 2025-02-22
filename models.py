from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class AlbumType(Enum):
	album  = 'album'
	single = 'single'
	ep     = 'ep'

	def pluralize(self) -> str:
		return f'{self.value}s'

@dataclass
class Track():
	name:        str
	number:      int
	link:        str
	album:       Optional['Album'] = None
	lyrics_file: Optional[str]     = None

	overwrite_embded: Optional[bool] = False

@dataclass
class Album():
	name:   str
	year:   int
	type:   AlbumType
	link:   Optional[str]      = None
	tracks: list[Track]        = field(default_factory=list)
	artist: Optional['Artist'] = None

@dataclass
class Artist():
	name:    str
	albums:  list[Album] = field(default_factory=list)
	eps:     list[Album] = field(default_factory=list)
	singles: list[Album] = field(default_factory=list)
