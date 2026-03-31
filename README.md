# Animating the T
This project looks at MBTA Orange Line performance during February 2026 using MBTA LAMP data. We focused on the February 23–24 storm and built two animations to show how travel times changed across the month.

## Project Overview
We used the Orange Line data and split the project into layers:
- **`acquire.py`**: downloads the MBTA parquet files for February 2026, filters to the Orange Line, cleans the data, removes duplicate stop records, and prepares the data for the rest of the project
- **`model.py`**: builds the `SubwayLine` model and computes the values needed for the animations
- **`animate_a.py`**: creates Animation A, a line chart showing average actual vs. scheduled travel time by day
- **`animate_b.py`**: creates Animation B, a heatmap showing average stop-level travel times across stations and days

## Files
- `acquire.py`
- `model.py`
- `animate_a.py`
- `animate_b.py`
- `reflection.md`
- `.gitignore`

## Data source
The data comes from the MBTA LAMP public dataset, specifically the subway on-time performance parquet files.

## Packages used
Some packages needed for this project are:
- pandas
- matplotlib
- pydantic
- pyarrow
- ffmpeg

## How to run
```bash
python acquire.py
python model.py
python animate_a.py
python animate_b.py
