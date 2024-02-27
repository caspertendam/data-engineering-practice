import re 
import requests
import pathlib
import structlog 
from zipfile import ZipFile 
  
logger = structlog.get_logger()

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


def download_files(target_dir: str | pathlib.Path = pathlib.Path("downloads")):
    logger.info(f"Downloading {len(download_uris)} files")
    if isinstance(target_dir, str):
        target_dir = pathlib.Path(target_dir)
    # Check if the target directory exists, else, create it
    if not target_dir.exists():
        target_dir.mkdir()
    for download_uri in download_uris:
        zip_file = download_file(download_uri, target_dir)
        if zip_file is None: 
            continue 
        extract_and_delete_zip_file(zip_file, target_dir) 


def extract_filename(download_uri: str) -> str:
    return download_uri.split("/")[-1]

def download_file(download_uri: str, target_dir: pathlib.Path) -> pathlib.Path | None: 
    # Extract the filename: 
    filename = extract_filename(download_uri)
    # (Attempt to) download the file
    logger.info(f"Downloading file {filename}")
    r = requests.get(download_uri, allow_redirects=True)
    if r.ok:
        zip_file = target_dir / filename
        open(zip_file, 'wb').write(r.content)
        return zip_file
    else: 
        logger.warning(f"HTTP request for {filename} failed with status code {r.status_code}.")
        return None

def extract_and_delete_zip_file(zip_file: pathlib.Path, target_dir: pathlib.Path) -> None: 
    logger.info(f"Extracting and deleting {zip_file}.")
    with ZipFile(zip_file, 'r') as zObject:
        zObject.extractall(path=target_dir)
    zip_file.unlink() # remove the zip file

def main():
    download_files(pathlib.Path("downloads"))


if __name__ == "__main__":
    main()
