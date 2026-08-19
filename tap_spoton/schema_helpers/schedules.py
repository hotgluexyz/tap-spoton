from typing import Any, Optional

from hotglue_tap_sdk import typing as th

time = th.ObjectType(
    th.Property("hours", th.IntegerType),
    th.Property("minutes", th.IntegerType),
    th.Property("seconds", th.IntegerType),
    th.Property("nanos", th.IntegerType),
)

day_times = th.ArrayType(
    th.ObjectType(
        th.Property("day_index", th.StringType),
        th.Property("start_time", time),
        th.Property("end_time", time),
    )
)

schedule = th.ObjectType(
    th.Property("day_times", day_times),
)

schedule_overrides = th.ArrayType(
    th.ObjectType(
        th.Property("date", th.DateType),
        th.Property("is_unavailable", th.BooleanType),
        th.Property("schedule", schedule),
    )
)


def parse_time_string(value: Any) -> Any:
    """Convert HH:MM schedule strings to SpotOn protobuf-style time objects."""
    if not isinstance(value, str):
        return value
    parts = value.split(":")
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    return {"hours": hours, "minutes": minutes, "seconds": 0, "nanos": 0}


def normalize_day_times(day_times_list: list) -> None:
    """Normalize start_time and end_time entries in place."""
    for entry in day_times_list:
        if "start_time" in entry:
            entry["start_time"] = parse_time_string(entry["start_time"])
        if "end_time" in entry:
            entry["end_time"] = parse_time_string(entry["end_time"])


def normalize_schedule(schedule_value: Optional[dict]) -> Optional[dict]:
    """Normalize string schedule times to object form in place."""
    if not schedule_value or not schedule_value.get("day_times"):
        return schedule_value
    normalize_day_times(schedule_value["day_times"])
    return schedule_value


def normalize_schedule_overrides(overrides: Optional[list]) -> Optional[list]:
    """Normalize nested schedules inside schedule_overrides in place."""
    if not overrides:
        return overrides
    for override in overrides:
        normalize_schedule(override.get("schedule"))
    return overrides


def apply_schedule_normalization(record: dict) -> dict:
    """Normalize schedule fields on a record dict in place."""
    normalize_schedule(record.get("schedule"))
    normalize_schedule_overrides(record.get("schedule_overrides"))
    return record
