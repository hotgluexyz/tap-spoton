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