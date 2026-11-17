import json
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "gradebook.json"
LOG_FILE = BASE_DIR / "logs" / "app.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True,
)


def _empty_data():
    return {
        "students": [],
        "courses": [],
        "enrollments": [],
    }


def load_data():
    """Load the gradebook JSON data, falling back to an empty structure."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("Data file does not contain a JSON object")
            logging.info("Data loaded successfully")
            return data

    except FileNotFoundError:
        logging.info("No data file found. Starting empty.")
        return _empty_data()

    except json.JSONDecodeError:
        logging.error("Invalid JSON format.")
        print("Warning: data file corrupted. Starting empty.")
        return _empty_data()

    except (OSError, ValueError) as exc:
        logging.error("Unable to load data: %s", exc)
        print(f"Warning: unable to load data ({exc}). Starting empty.")
        return _empty_data()


def save_data(data):
    """Persist the gradebook data to disk."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    logging.info("Data saved successfully")