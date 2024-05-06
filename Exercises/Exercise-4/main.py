import json
import glob
import csv
from pathlib import Path


def main():
    json_files = find_all_json_files()
    for json_file in json_files:
        # Create the path
        path = Path(json_file)
        # Load the JSON file
        with open(path) as f:
            json_obj = json.load(f)
        # Flatten the JSON file
        json_obj = flatten_dict(json_obj)
        # Create a csv file with the same name
        csv_path = Path("result") / (path.with_suffix(".csv")).name
        with open(csv_path, "w") as f:
            writer = csv.DictWriter(f=f, fieldnames=json_obj.keys())
            writer.writeheader()
            writer.writerow(json_obj)


def find_all_json_files():
    return glob.glob("**/*.json", recursive=True)


def flatten_dict(dict_: dict) -> dict:
    for key in dict_.keys():
        if type(dict_) in [dict, list]:
            dict_[key] = str(dict_[key])
    return dict_


if __name__ == "__main__":
    main()
