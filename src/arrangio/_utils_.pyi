from typing import Final


REGXPR: Final[str]
TIMEFMT: Final[str]

def get_songs(songs: list) -> tuple: ...
def get_subsets(songs: list, num: int) -> tuple: ...
def to_json(result: tuple) -> str: ...
def to_text(result: tuple) -> str: ...
