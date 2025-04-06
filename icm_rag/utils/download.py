import os
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests  # type: ignore
from utils.log import log_error, log_info
from utils.path import is_url


def download(
    base_url: str,
    local_dir: Path,
    dataset: str,
    force_download: bool = False,  # noqa: E501
):
    url = base_url
    if dataset is not None:
        url = urljoin(base_url, dataset + ".md")

    if not is_url(url):
        log_info(f"Provided url ({url}) is invalid.")
        return

    file_name = os.path.basename(urlparse(url).path)
    local_path = local_dir / file_name

    if os.path.exists(local_path) and not force_download:
        return

    log_info("Downloading from url: " + url)
    response = requests.get(url)
    if response.status_code == 200:
        response = requests.get(url)
        with open(local_path, "wb") as file:
            file.write(response.content)
        log_info("Download complete.")
    else:
        log_error(f"Failed to download file: {response.status_code}")
