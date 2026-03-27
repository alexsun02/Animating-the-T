import os
import pandas as pd

# create the base url with a placeholder for the date string in the format YYYY-MM-DD
BASE_URL = (
    "https://performancedata.mbta.com/lamp/"
    "subway-on-time-performance-v1/"
    "{date}-subway-on-time-performance-v1.parquet"
)

# map the parent_station ID with the station name in geographic order along the orange line
ORANGE_STOPS = [
    ("place-ogmnl", "Oak Grove"),
    ("place-mlmnl", "Malden Center"),
    ("place-welln", "Wellington"),
    ("place-astao", "Assembly"),
    ("place-sull", "Sullivan Square"),
    ("place-ccmnl", "Community College"),
    ("place-north", "North Station"),
    ("place-haecl", "Haymarket"),
    ("place-state", "State"),
    ("place-dwnxg", "Downtown Crossing"),
    ("place-chncl", "Chinatown"),
    ("place-tumnl", "Tufts Medical Center"),
    ("place-bbsta", "Back Bay"),
    ("place-masta", "Massachusetts Avenue"),
    ("place-rugg", "Ruggles"),
    ("place-rcmnl", "Roxbury Crossing"),
    ("place-jaksn", "Jackson Square"),
    ("place-sbmnl", "Stony Brook"),
    ("place-grnst", "Green Street"),
    ("place-forhl", "Forest Hills")
]

def get_station_names(route_id="Orange"):
    """Return ordered station names for the chosen line"""
    if route_id == "Orange":
        return [station_name for station_id, station_name in ORANGE_STOPS]
    raise ValueError(f"No station names saved for {route_id}")

def get_station_ids(route_id="Orange"):
    """Internal helper: Return ordered parent_station IDs for the chosen line"""
    if route_id == "Orange":
        return [station_id for station_id, station_name in ORANGE_STOPS]
    raise ValueError(f"No station ids saved for {route_id}")

def build_url(date_str):
    """Build the parquet URL for one date string in the format YYYY-MM-DD"""
    return BASE_URL.format(date=date_str)

def fetch_february_data(route_id="Orange", use_cache=True):
    """
    Fetch all February 2026 parquet files and combine them into one dataframe
    Filters to the chosen line as early as possible.
    """
    # Load cached Parquet file to prevent re-downloading multiple files
    cache_file = f"february_{route_id.lower()}_2026.parquet"
    if use_cache and os.path.exists(cache_file):
        print(f"Loading cached data from {cache_file}")
        return pd.read_parquet(cache_file)

    ### If no cache ###
    # Create a range of dates
    dates = pd.date_range("2026-02-01", "2026-02-28", freq="D")
    # Create empty list to hold each day's filtered DataFrame
    all_days = []
    # Loop through each date from the range of dates
    for day in dates:
        # Convert datetime to string
        date_str = day.strftime("%Y-%m-%d")
        # Build the URL for the parquet file for that date
        url = build_url(date_str)
        df_day = pd.read_parquet(url)
        # Filter to the chosen line
        df_day = df_day[df_day["trunk_route_id"] == route_id].copy()
        # Append each date's data to the empty list
        all_days.append(df_day)
        print(f"{date_str}: {df_day.shape}")
    # Concatenate into one DataFrame
    feb_df = pd.concat(all_days, ignore_index=True)
    # Cache concatenated DataFrame to a local Parquet file after the first fetch
    if use_cache:
        feb_df.to_parquet(cache_file, index=False)
        print(f"Saved cache to {cache_file}")
    return feb_df

def clean_line_data(df):
    """Clean the line data and remove duplicate stop records"""
    cleaned = df.copy()
    # Covert from int64 to datetime and mark invalid dates
    cleaned["service_date"] = pd.to_datetime(
        cleaned["service_date"],
        format="%Y%m%d",
        errors="coerce"
    )
    # Drop invalid dates
    cleaned = cleaned.dropna(subset=["service_date"])
    # Convert from datetime to string
    cleaned["service_date"] = cleaned["service_date"].dt.strftime("%Y-%m-%d")
    # Drop rows with missing values
    cleaned = cleaned.dropna(subset=[
        "trip_id",
        "stop_id",
        "parent_station",
        "stop_sequence",
        "stop_timestamp",
        "travel_time_seconds"
    ])
    # Sort columns by ascending order
    cleaned = cleaned.sort_values(
        ["service_date", "trip_id", "stop_id", "stop_timestamp"]
    )
    # Drop duplicate trip_id–stop_id pairs, keeping the earliest unique combination by sorting on stop_timestamp
    cleaned = cleaned.drop_duplicates(
        subset=["service_date", "trip_id", "stop_id"],
        keep="first"
    )
    # Remove rows with non-positive travel times
    cleaned = cleaned[cleaned["travel_time_seconds"] > 0].copy()
    # Reorder columns and reset index
    cleaned = cleaned.sort_values(
        ["service_date", "trip_id", "stop_sequence", "stop_timestamp"]
    ).reset_index(drop=True)
    return cleaned

def get_clean_data(route_id="Orange", use_cache=True):
    """Return the cleaned February dataframe for one line."""
    raw_df = fetch_february_data(route_id=route_id, use_cache=use_cache)
    return clean_line_data(raw_df)

def get_trip_totals(df):
    """Sum actual travel times across each trip"""
    trips = (
        df.groupby(["service_date", "trip_id"], as_index=False)
        .agg({
            "travel_time_seconds": "sum"
        })
        .rename(columns={"travel_time_seconds": "actual_travel_time"})
    )
    return trips

def get_scheduled_trip_totals(df):
    """Sum scheduled travel times across each trip, after removing missing values"""
    # Drop rows with null scheduled_travel_time
    scheduled_df = df.dropna(subset=["scheduled_travel_time"]).copy()
    # Aggregate scheduled_travel_time across each trip
    trips = (
        scheduled_df.groupby(["service_date", "trip_id"], as_index=False)
        .agg({
            "scheduled_travel_time": "sum"
        })
        .rename(columns={"scheduled_travel_time": "scheduled_travel_time_total"})
    )
    return trips

if __name__ == "__main__":
    cleaned_df = get_clean_data("Orange", use_cache=True)
    trip_totals = get_trip_totals(cleaned_df)
    scheduled_trip_totals = get_scheduled_trip_totals(cleaned_df)
    station_names = get_station_names("Orange")

    print("\nCleaned dataframe shape:")
    print(cleaned_df.shape)

    print("\nTrip totals:")
    print(trip_totals.head())

    print("\nScheduled trip totals:")
    print(scheduled_trip_totals.head())

    print("\nStation names:")
    print(station_names)