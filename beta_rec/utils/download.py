import requests
from tqdm import tqdm
from beta_rec.utils.onedrive import OneDrive


def download_file(url, store_file_path):
    """Download the raw dataset file

    Download the dataset with the given url and save to the store_path
    Args:
        url: the url that can be downloaded the dataset file.
        store_file_path: the path that stores the downloaded file
    Return:
        the archive format of the suffix
    """
    filename = url.split("/")[-1]
    print(f"Start downloading file {filename}...")
    r = requests.get(url, allow_redirects=True, stream=True)
    # Total size in bytes
    total_size = int(r.headers.get("content-length", 0))
    block_size = 1024
    t = tqdm(total=total_size, unit="iB", unit_scale=True)

    with open(store_file_path, "wb") as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)

    t.close()
    if total_size != 0 and t.n != total_size:
        print(f"ERROR, download fail")
    else:
        print(f"Success loading file {filename} to {store_file_path}")


def get_format(suffix):
    """ Get the archive format

    Get the archive format of the archive file with its suffix
    Args:
        suffix: suffix of the archive file
    Return:
        the archive format of the suffix
    """
    format_map = {
        "bz2": "bztar",
        "gz": "gztar",
    }
    if suffix not in format_map:
        return suffix
    return format_map[suffix]


def download_file_from_onedrive(url, path):
    """Download processed file from OneDrive

    Download file from Onedrive with the give url and save to the given path

    Args:
        url: the shared link generated by Onedrive
        path: the path supposed to store the file
    """
    folder = OneDrive(url=url, path=path)
    folder.download()
