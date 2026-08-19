"""Tests for schedule time normalization."""

from tap_spoton.schema_helpers.schedules import (
    apply_schedule_normalization,
    normalize_schedule,
    parse_time_string,
)


def test_parse_time_string_converts_hh_mm():
    assert parse_time_string("00:00") == {
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "nanos": 0,
    }
    assert parse_time_string("23:59") == {
        "hours": 23,
        "minutes": 59,
        "seconds": 0,
        "nanos": 0,
    }


def test_parse_time_string_preserves_objects():
    value = {"hours": 9, "minutes": 30, "seconds": 0, "nanos": 0}
    assert parse_time_string(value) == value


def test_normalize_schedule_converts_menu_schedule():
    schedule_value = {
        "day_times": [
            {
                "day_index": "DAY_INDEX_MON",
                "start_time": "00:00",
                "end_time": "23:59",
            }
        ]
    }
    normalize_schedule(schedule_value)
    assert schedule_value["day_times"][0]["start_time"] == {
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "nanos": 0,
    }
    assert schedule_value["day_times"][0]["end_time"] == {
        "hours": 23,
        "minutes": 59,
        "seconds": 0,
        "nanos": 0,
    }


def test_apply_schedule_normalization_on_record_with_overrides():
    record = {
        "schedule": {
            "day_times": [
                {
                    "day_index": "DAY_INDEX_MON",
                    "start_time": "08:00",
                    "end_time": "17:00",
                }
            ]
        },
        "schedule_overrides": [
            {
                "date": "2026-09-07",
                "is_unavailable": False,
                "schedule": {
                    "day_times": [
                        {
                            "day_index": "DAY_INDEX_MON",
                            "start_time": "10:00",
                            "end_time": "14:00",
                        }
                    ]
                },
            }
        ],
    }
    apply_schedule_normalization(record)
    assert record["schedule"]["day_times"][0]["start_time"]["hours"] == 8
    assert record["schedule_overrides"][0]["schedule"]["day_times"][0]["start_time"][
        "hours"
    ] == 10
