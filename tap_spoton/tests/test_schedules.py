"""Tests for schedule schema time fields."""

import jsonschema

from tap_spoton.streams import MenusStream


def test_schedule_schema_accepts_string_times():
    schema = MenusStream.schema["properties"]["schedule"]
    jsonschema.validate(
        {
            "day_times": [
                {
                    "day_index": "DAY_INDEX_MON",
                    "start_time": "00:00",
                    "end_time": "23:59",
                }
            ]
        },
        schema,
    )


def test_schedule_schema_accepts_object_times():
    schema = MenusStream.schema["properties"]["schedule"]
    jsonschema.validate(
        {
            "day_times": [
                {
                    "day_index": "DAY_INDEX_MON",
                    "start_time": {
                        "hours": 0,
                        "minutes": 0,
                        "seconds": 0,
                        "nanos": 0,
                    },
                    "end_time": {
                        "hours": 23,
                        "minutes": 59,
                        "seconds": 0,
                        "nanos": 0,
                    },
                }
            ]
        },
        schema,
    )
