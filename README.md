# Task 2 - Data Processing Pipeline

## Objective
Build a Python data-processing pipeline that reads raw CSV/JSON data, cleans and transforms it, handles missing values and type-conversion errors, logs events, and writes structured output.

## Project Structure
```text
task2_data_processing_pipeline/
├── data/input.csv
├── output/processed_data.csv
├── logs/pipeline.log
├── config.json
├── pipeline.py
└── README.md
```

## Requirements
- Python 3.x
- No external packages are required.

## How to Run
1. Install Python 3.
2. Open a terminal in this folder.
3. Run:
   `python pipeline.py`
4. The processed file will be created at:
   `output/processed_data.csv`

## Features
- CSV input support
- JSON input support
- Missing-value handling
- Safe integer/float conversion
- Negative-value edge-case handling
- Data transformation
- Logging
- Configuration through `config.json`
- Structured CSV output

## Sample Result
The sample input intentionally contains missing values and an invalid age. The pipeline replaces missing values with configured defaults and safely converts invalid values.

## Submission
Upload this complete folder to a GitHub repository and submit the GitHub repository URL in the internship portal.
