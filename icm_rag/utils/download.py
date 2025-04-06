import os
from pathlib import Path
from typing import Union
from urllib.parse import urljoin, urlparse

import requests  # type: ignore
from utils.log import log_error, log_info
from utils.path import is_url


def download(
    base_url: str,
    local_dir: Path,
    dataset: str,
    force_download: bool = False,  # noqa: E501
) -> Union[Path, None]:
    """
    Download file, given the base url and dataset.
    Is used for corpus downlaod.
    If GitHub link is provided, it must be in RAW format.

    Args:
        base_url (str): Base URL to search for the dataset.
        locaL_dir (Path): Path to local dir, to download the dataset.
        dataset (str): Name of the dataset, e.g. "wikitexts".
        force_download (bool): If True, override downloaded corpus at path.

    Returns:
        Union[Path, None]: If successfully downloaded, return the local path
            of the downloaded dataset.
            Otherwise, return None.
    """
    url = base_url
    if dataset is not None:
        url = urljoin(base_url, dataset + ".md")

    if not is_url(url):
        log_info(f"Provided url ({url}) is invalid.")
        return None

    file_name = os.path.basename(urlparse(url).path)
    local_path = local_dir / file_name

    if os.path.exists(local_path) and not force_download:
        return local_path

    log_info("Downloading from url: " + url)
    response = requests.get(url)
    if response.status_code == 200:
        response = requests.get(url)
        with open(local_path, "wb") as file:
            file.write(response.content)
        log_info("Download complete.")
        return local_path
    else:
        log_error(f"Failed to download file: {response.status_code}")
        return None
