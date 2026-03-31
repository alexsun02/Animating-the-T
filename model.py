"""
model.py

Pydantic model layer for MBTA subway line analysis.

This file defines the SubwayLine model which accepts cleaned data from the
acquisition layer and exposes all aggregated data as computed fields.
The animation layers consume only fields from this model — they never
access the raw DataFrame directly.
"""

import pandas as pd
from pydantic import BaseModel, computed_field


class SubwayLine(BaseModel):
    """Pydantic model representing one MBTA subway line across February 2026."""

    model_config = {"arbitrary_types_allowed": True}

    route_name: str  # e.g. "Orange Line"
    route_id: str  # e.g. "Orange"
    station_names: list[str]  # ordered list of station names (geographic order)
    cleaned_df: pd.DataFrame  # cleaned stop-level data from acquire.py
    trip_totals: pd.DataFrame  # output of get_trip_totals()
    scheduled_trip_totals: pd.DataFrame  # output of get_scheduled_trip_totals()

    @computed_field
    @property
    def stops(self) -> list[str]:
        """Ordered list of station names along the line."""
        return self.station_names

    @computed_field
    @property
    def dates(self) -> list[str]:
        """Sorted list of service dates in February as strings."""
        return sorted(self.cleaned_df["service_date"].unique().tolist())

    @computed_field
    @property
    def daily_avg_travel(self) -> dict[str, float]:
        """Date string -> mean actual travel time (seconds) across all trips."""
        agg = (
            self.trip_totals
            .groupby("service_date")["actual_travel_time"]
            .mean()
        )
        return {date: round(val, 2) for date, val in agg.items()}

    @computed_field
    @property
    def daily_avg_scheduled(self) -> dict[str, float]:
        """Date string -> mean scheduled travel time (seconds) across all trips."""
        agg = (
            self.scheduled_trip_totals
            .groupby("service_date")["scheduled_travel_time_total"]
            .mean()
        )
        return {date: round(val, 2) for date, val in agg.items()}

    @computed_field
    @property
    def travel_by_stop_and_day(self) -> pd.DataFrame:
        """
        Pivot table: rows = stations (geographic order), columns = dates,
        values = mean travel_time_seconds at that stop on that day.

        This is the 2D array the heatmap animation calls set_array() on.
        """
        # map parent_station IDs to station names using the acquire layer's
        # ORANGE_STOPS ordering - need to import the ID list for the merge
        from acquire import get_station_ids

        station_ids = get_station_ids(self.route_id)
        id_to_name = dict(zip(station_ids, self.station_names))

        # filter to only stops on our line and map to station names
        df = self.cleaned_df[
            self.cleaned_df["parent_station"].isin(station_ids)
        ].copy()
        df["station_name"] = df["parent_station"].map(id_to_name)

        # pivot: rows = station, columns = date, values = mean travel time
        pivot = df.pivot_table(
            index="station_name",
            columns="service_date",
            values="travel_time_seconds",
            aggfunc="mean"
        )

        # reorder rows to geographic order, columns to date order
        pivot = pivot.reindex(index=self.station_names, columns=sorted(pivot.columns))

        return pivot


def build_model(route_id="Orange", route_name="Orange Line") -> SubwayLine:
    """Convenience function: fetch data from acquire layer and build the model."""
    from acquire import get_clean_data, get_trip_totals, get_scheduled_trip_totals, get_station_names

    cleaned = get_clean_data(route_id)
    trips = get_trip_totals(cleaned)
    scheduled = get_scheduled_trip_totals(cleaned)
    stations = get_station_names(route_id)

    return SubwayLine(
        route_name=route_name,
        route_id=route_id,
        station_names=stations,
        cleaned_df=cleaned,
        trip_totals=trips,
        scheduled_trip_totals=scheduled,
    )


if __name__ == "__main__":
    model = build_model("Orange", "Orange Line")

    print(f"Route: {model.route_name}")
    print(f"Stops ({len(model.stops)}): {model.stops}")
    print(f"Dates ({len(model.dates)}): {model.dates[0]} to {model.dates[-1]}")

    print("\nDaily avg actual travel time (first 5 days):")
    for date in model.dates[:5]:
        print(f"  {date}: {model.daily_avg_travel.get(date, 'N/A')}s")

    print("\nDaily avg scheduled travel time (first 5 days):")
    for date in model.dates[:5]:
        print(f"  {date}: {model.daily_avg_scheduled.get(date, 'N/A')}s")

    print("\nHeatmap pivot shape:", model.travel_by_stop_and_day.shape)
    print(model.travel_by_stop_and_day.head())