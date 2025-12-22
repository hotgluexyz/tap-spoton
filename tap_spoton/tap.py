"""SpotOn tap class."""

from typing import List

from hotglue_tap_sdk import Stream, Tap
from hotglue_tap_sdk import typing as th

from tap_spoton.streams import LocationsStream, LocationsDetailsStream, OrdersStream

STREAM_TYPES = [
    LocationsStream,
    LocationsDetailsStream,
    OrdersStream,
]


class TapSpotOn(Tap):
    """SpotOn tap class."""

    name = "tap-spoton"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "locations",
            th.ArrayType(th.StringType),
            required=True,
            description="The locations to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapSpotOn.cli()
