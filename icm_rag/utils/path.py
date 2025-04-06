import os
import urllib
from pathlib import Path


def is_url(url: str) -> bool:
    """
    Check whether the given potential URL is indeed an URL.

    Args:
        url (str): URL to check.

    Returns:
        bool: True, if given URL is indeed URL. Otherwise, return False.
    """
    parsed_url = urllib.parse.urlparse(url)
    return bool(parsed_url.scheme)


def expand_path(path: Path) -> Path:
    """
    Expand environment variables in given path.

    Args:
        path (Path): Path to expand.

    Returns:
        Path: Starting path, but with expanded environment variables.
    """
    return Path(os.path.expandvars(str(path)))


def make_path(dir_path: Path) -> Path:
    """
    Assure the path exists, and, if not, create the directory of it.

    Args:
        dir_path (Path): Directory to create.

    Returns:
        dir_path (Path): Directory path, with expanded variables.
    """
    dir_path = expand_path(dir_path)

    if os.path.exists(dir_path):
        return dir_path

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return dir_path
