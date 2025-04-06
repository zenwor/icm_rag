import os
import urllib
from pathlib import Path


def is_url(url: str) -> bool:
    parsed_url = urllib.parse.urlparse(url)
    return bool(parsed_url.scheme)


def expand_path(path: Path) -> Path:
    return Path(os.path.expandvars(str(path)))


def make_path(dir_path: Path) -> Path:
    dir_path = expand_path(dir_path)

    if os.path.exists(dir_path):
        return dir_path

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return dir_path
