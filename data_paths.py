from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CSV_DIR = BASE_DIR / "csv"

RAW_DATA_FILE = CSV_DIR / "raw_data.csv"
AVAILABILITY_FILE = CSV_DIR / "availability.csv"
POST_MATCH_FILE = CSV_DIR / "post_match.csv"


def csv_repo_path(path):
    return Path(path).as_posix()
