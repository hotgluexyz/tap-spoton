"""Stream type classes for tap-spoton."""

from typing import Iterable, Optional

from hotglue_tap_sdk import typing as th

from tap_spoton.client import SpotOnStream


class LocationsStream(SpotOnStream):
    """Define custom stream."""

    name = "locations"
    path = "/locations"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
    ).to_dict()

    def get_records(self, context: Optional[dict] = None) -> Iterable[dict]:
        """Get records from the API."""
        locations = self.config.get("locations", [])
        for location in locations:
            yield {"id": location}

    def get_child_context(self, record: dict, context: Optional[dict] = None) -> dict:
        """Get child context from the API."""
        return {"location_id": record["id"]}


class OrdersStream(SpotOnStream):
    """Define orders stream."""

    name = "orders"
    path = "reporting/v1/locations/{location_id}/orders"
    primary_keys = ["id"]
    replication_key = "last_updated_at"
    parent_stream_type = LocationsStream
    records_jsonpath = "$.orders[*]"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("location_id", th.StringType),
        th.Property("source", th.StringType),
        th.Property("fulfillment_type", th.StringType),
        th.Property(
            "line_items",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("quantity", th.NumberType),
                    th.Property("price", th.NumberType),
                    th.Property(
                        "modifiers",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("id", th.StringType),
                                th.Property("name", th.StringType),
                                th.Property("quantity", th.NumberType),
                                th.Property("price", th.NumberType),
                                th.Property("prefix", th.StringType),
                            )
                        ),
                    ),
                    th.Property(
                        "applicable_taxes",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("tax_id", th.StringType),
                                th.Property("tax_amount", th.NumberType),
                            )
                        ),
                    ),
                    th.Property("order_item_id", th.StringType),
                )
            ),
        ),
        th.Property(
            "payments",
            th.ArrayType(
                th.ObjectType(
                    th.Property("type", th.StringType),
                    th.Property("amount", th.NumberType),
                    th.Property("is_refund", th.BooleanType),
                    th.Property("is_void", th.BooleanType),
                )
            ),
        ),
        th.Property(
            "totals",
            th.ObjectType(
                th.Property("subtotal", th.NumberType),
                th.Property("tip_total", th.NumberType),
                th.Property("discounts_total", th.NumberType),
                th.Property("tax_total", th.NumberType),
                th.Property("grand_total", th.NumberType),
                th.Property("modifiers_amount", th.NumberType),
                th.Property("autogratuity_amount", th.NumberType),
                th.Property("fees_revenue_amount", th.NumberType),
                th.Property("payments_amount", th.NumberType),
                th.Property("liabilities_amount", th.NumberType),
                th.Property("voids_amount", th.NumberType),
                th.Property("gross_sales_amount", th.NumberType),
                th.Property("net_sales_amount", th.NumberType),
                th.Property("inclusive_taxes_amount", th.NumberType),
                th.Property("exclusive_taxes_amount", th.NumberType),
                th.Property("has_returns", th.BooleanType),
            ),
        ),
        th.Property(
            "discounts",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("amount", th.NumberType),
                )
            ),
        ),
        th.Property("created_at", th.DateTimeType),
        th.Property("last_updated_at", th.DateTimeType),
        th.Property("closed_at", th.DateTimeType),
        th.Property(
            "taxes",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("amount", th.NumberType),
                    th.Property("percentage", th.NumberType),
                )
            ),
        ),
        th.Property(
            "employee",
            th.ObjectType(
                th.Property(
                    "owned_by",
                    th.ObjectType(
                        th.Property("id", th.StringType),
                        th.Property("name", th.StringType),
                    ),
                )
            ),
        ),
        th.Property("table_number", th.StringType),
        th.Property("guest_count", th.IntegerType),
    ).to_dict()
