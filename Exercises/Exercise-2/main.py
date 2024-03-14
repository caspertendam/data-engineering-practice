import re
import requests
import pandas as pd
import pathlib
import structlog

logger = structlog.get_logger()

URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
DATE = "2024-01-19 10:19"
COL_NAME = "HourlyDryBulbTemperature"


def get_csv_file_from_line(line: str) -> str:
    return re.search(r'href="(\S+)"', line).group(1)


def find_csv_file(response: requests.Response) -> str | None:
    logger.info("Finding correct csv file")
    for line in response.iter_lines(decode_unicode=True):
        if line.find(DATE) > -1:
            return get_csv_file_from_line(line)
    return None


def get_download_dir() -> pathlib.Path:
    download_dir = pathlib.Path("downloads")
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir


def download_csv_file(csv_file: str) -> None:
    logger.info(f"Donwloading csv file {csv_file}")
    r = requests.get(URL + csv_file, allow_redirects=True)
    if r.ok:
        download_dir = get_download_dir()
        path = download_dir / csv_file
        open(path, "wb").write(r.content)
        return path
    else:
        raise (
            ConnectionError(f"HTTP request failed with status code {r.status_code}.")
        )


def print_records_w_max_hourly_dry_bulb_temperature():
    logger.info(f"Loading HTML page from {URL}")
    response = requests.get(URL)
    csv_file = find_csv_file(response)
    if csv_file is None:
        raise (LookupError(f"No .csv file found with date {DATE}"))
    path = download_csv_file(csv_file)
    # Load the csv as a pandas dataframe
    df = pd.read_csv(path)
    # Get the column of interest: convert to float;
    # some entries are invalid (e.g. '14s') and will be set to None
    series = pd.to_numeric(df[COL_NAME], errors="coerce")
    # Find the max HourlyDryBulbTemperature, filter the rows with that value
    max_temp = series.max()
    df_highest_tmp = df[series == max_temp]
    # Print to stdout
    logger.info(f"The maximum {COL_NAME} is {max_temp}")
    logger.info("These are the records with that temperature:")
    print(df_highest_tmp)


def main():
    # your code here
    print_records_w_max_hourly_dry_bulb_temperature()


if __name__ == "__main__":
    main()
