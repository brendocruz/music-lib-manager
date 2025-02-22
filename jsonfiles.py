import json
from typing import Any

def dump_json(filename: str, data: Any) -> None:
	try:
		file = open(filename, 'w', encoding="utf-8")
		json.dump(data, file, indent=2, ensure_ascii=False)
		file.close()
	except Exception as error:
		print(error)

def load_json(filename: str) -> Any:
	data: Any = []
	try:
		file = open(filename, 'r', encoding="utf-8")
		data = json.load(file)
		file.close()
	except Exception as error:
		raise error
	return data
