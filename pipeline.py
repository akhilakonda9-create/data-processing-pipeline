import csv
import json
import logging
from pathlib import Path

CONFIG_FILE = "config.json"

def setup_logging(log_file):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def read_csv(file_path):
    logging.info("Reading CSV: %s", file_path)
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def read_json(file_path):
    logging.info("Reading JSON: %s", file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_data(rows, missing_values):
    cleaned = []

    for row in rows:
        # Trim spaces and convert empty strings to None
        row = {k.strip(): (v.strip() if isinstance(v, str) else v)
               for k, v in row.items()}

        for key, default in missing_values.items():
            if row.get(key) in ("", None):
                row[key] = default

        # Safe integer conversion
        try:
            row["age"] = int(row.get("age", 0))
        except (ValueError, TypeError):
            logging.warning("Invalid age '%s'; using 0", row.get("age"))
            row["age"] = 0

        # Safe float conversion
        try:
            row["salary"] = float(row.get("salary", 0))
        except (ValueError, TypeError):
            logging.warning("Invalid salary '%s'; using 0", row.get("salary"))
            row["salary"] = 0.0

        # Edge-case handling
        if row["age"] < 0:
            logging.warning("Negative age found; using 0")
            row["age"] = 0
        if row["salary"] < 0:
            logging.warning("Negative salary found; using 0")
            row["salary"] = 0.0

        cleaned.append(row)

    return cleaned

def transform_data(rows):
    for row in rows:
        row["salary"] = round(row["salary"], 2)
        row["name"] = row.get("name", "Unknown").title()
        row["city"] = row.get("city", "Unknown").title()
    return rows

def write_csv(rows, output_file):
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        logging.warning("No rows to write")
        return

    fields = ["name", "age", "salary", "city"]
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def main():
    config = load_config()
    setup_logging(config["log_file"])

    input_file = config["input_file"]
    if not Path(input_file).exists():
        logging.error("Input file does not exist: %s", input_file)
        print("ERROR: Input file not found.")
        return

    try:
        if input_file.lower().endswith(".csv"):
            rows = read_csv(input_file)
        elif input_file.lower().endswith(".json"):
            rows = read_json(input_file)
        else:
            raise ValueError("Only CSV and JSON input files are supported.")

        rows = clean_data(rows, config["missing_values"])
        rows = transform_data(rows)
        write_csv(rows, config["output_file"])

        logging.info("Pipeline completed successfully. Rows: %d", len(rows))
        print(f"Pipeline completed successfully. Output: {config['output_file']}")

    except Exception as exc:
        logging.exception("Pipeline failed: %s", exc)
        print("ERROR: Pipeline failed. Check the log file.")

if __name__ == "__main__":
    main()
