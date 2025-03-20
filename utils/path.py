import os
from pathlib import Path
import urllib

def is_url(url: str) -> bool:
    parsed_url = urllib.parse.urlparse(url)
    return bool(parsed_url.scheme)


def expand_path(path: Path) -> Path:
    return Path(os.path.expandvars(str(path)))


def make_path(path: Path) -> None:
    path = expand_path(path)
    
    if os.path.exists(path):
        return path
    
    print(path)
    local_dir = os.path.dirname(str(path))
    if not os.path.exists(local_dir):
        os.makedirs(dir)
    
    return path