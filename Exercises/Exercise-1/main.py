import re 
import requests
import pathlib
import structlog 

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
        download_file(download_uri, target_dir)

def extract_filename(download_uri: str) -> str:
    return download_uri.split("/")[-1]

def download_file(download_uri: str, target_dir: pathlib.Path) -> None: 
    # Extract the filename: 
    filename = extract_filename(download_uri)
    # (Attempt to) download the file
    logger.info(f"Downloading file {filename}")
    r = requests.get(download_uri, allow_redirects=True)
    if r.ok:
        open(target_dir / filename, 'wb').write(r.content)
    else: 
        logger.warning(f"HTTP request for {filename} failed with status code {r.status_code}.")

def main():
    download_files(pathlib.Path("downloads"))


if __name__ == "__main__":
    main()
