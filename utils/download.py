from utils.log import log_info, log_error
from utils.path import is_url

import requests
import urllib
from urllib.parse import urljoin
import os
from pathlib import Path


def download(base_url: str, local_dir: Path, dataset: str = None, force_download: bool = False):
    url = base_url
    if dataset is not None:
        url = urljoin(base_url, dataset + ".md")
        
    if not is_url(url):
        log_info(f"Provided url ({url}) is invalid.")
        return
    
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(str(parsed_url))
    local_path = local_dir / filename  
    
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