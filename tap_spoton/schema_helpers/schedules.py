from hotglue_tap_sdk import typing as th

# Business API (locations) — protobuf-style times
time_object = th.ObjectType(
    th.Property("hours", th.IntegerType),
    th.Property("minutes", th.IntegerType),
    th.Property("seconds", th.IntegerType),
    th.Property("nanos", th.IntegerType),
)

day_times_object = th.ArrayType(
    th.ObjectType(
        th.Property("day_index", th.StringType),
        th.Property("start_time", time_object),
        th.Property("end_time", time_object),
    )
)

schedule_object = th.ObjectType(
    th.Property("day_times", day_times_object),
)

# Menu API — HH:MM strings
day_times_string = th.ArrayType(
    th.ObjectType(
        th.Property("day_index", th.StringType),
        th.Property("start_time", th.StringType),
        th.Property("end_time", th.StringType),
    )
)

schedule_string = th.ObjectType(
    th.Property("day_times", day_times_string),
)

schedule_overrides_string = th.ArrayType(
    th.ObjectType(
        th.Property("date", th.DateType),
        th.Property("is_unavailable", th.BooleanType),
        th.Property("schedule", schedule_string),
    )
)
