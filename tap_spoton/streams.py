"""Stream type classes for tap-spoton."""

from typing import Iterable, Optional

from hotglue_tap_sdk import typing as th

from tap_spoton.client import SpotOnStream
from tap_spoton.schema_helpers.schedules import (
    apply_schedule_normalization,
    day_times,
    schedule,
    schedule_overrides,
)
from tap_spoton.schema_helpers.prices import prices


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


class LocationsDetailsStream(SpotOnStream):
    """Define custom stream."""

    name = "locations_details"
    path = "business/v1/locations/{location_id}"
    primary_keys = ["id"]
    parent_stream_type = LocationsStream
    records_jsonpath = "$.location"
    pagination = False

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("email", th.StringType),
        th.Property("phone", th.StringType),
        th.Property(
            "address",
            th.ObjectType(
                th.Property("address_line_1", th.StringType),
                th.Property("address_line_2", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
            ),
        ),
        th.Property(
            "geolocation",
            th.ObjectType(
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
            ),
        ),
        th.Property("timezone", th.StringType),
        th.Property(
            "business_hours",
            th.ObjectType(
                th.Property(
                    "day_times",
                    day_times,
                )
            ),
        ),
        th.Property(
            "business_special_hours",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "date",
                        th.ObjectType(
                            th.Property("year", th.IntegerType),
                            th.Property("month", th.IntegerType),
                            th.Property("day", th.IntegerType),
                        ),
                    ),
                    th.Property("is_unavailable", th.BooleanType),
                    th.Property(
                        "schedule",
                        schedule,
                    ),
                )
            ),
        )
    ).to_dict()


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


class MenusStream(SpotOnStream):
    """Define orders stream."""

    name = "menus"
    path = "menu/v1/locations/{location_id}/menus"
    primary_keys = ["id"]
    parent_stream_type = LocationsStream
    records_jsonpath = "$.menus[*]"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("location_id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property(
            "schedule",
            schedule,
        ),
        th.Property(
            "schedule_overrides",
            schedule_overrides,
        ),
        th.Property(
            "categories",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("description", th.StringType),
                    th.Property("active", th.BooleanType),
                    th.Property("sort_order", th.IntegerType),
                )
            ),
        ),
        th.Property("created_at", th.DateTimeType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict] = None) -> dict:
        """Get child context from the API."""
        return {"menu_id": record["id"], "location_id": context["location_id"]}

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        """Normalize menu schedule string times before schema validation."""
        return apply_schedule_normalization(row)


class MenuItemsStream(SpotOnStream):
    """Define menu items stream."""

    name = "menu_items"
    path = "menu/v1/locations/{location_id}/menus/{menu_id}/items"
    primary_keys = ["id", "menu_id", "location_id"]
    parent_stream_type = MenusStream
    records_jsonpath = "$.items[*]"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("location_id", th.StringType),
        th.Property("menu_id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("active", th.BooleanType),
        th.Property("is_available", th.BooleanType),
        th.Property("image_url", th.StringType),
        th.Property(
            "price",
            prices,
        ),
        th.Property("is_alcohol", th.BooleanType),
        th.Property("sort_order", th.IntegerType),
        # schedule can be null
        th.Property(
            "schedule",
            schedule,
        ),
        th.Property(
            "category_references",
            th.ArrayType(th.ObjectType(
                th.Property("category_id", th.StringType),
                th.Property("sort_order", th.IntegerType),
                th.Property("price", prices),
                th.Property("schedule", schedule),
                th.Property("schedule_overrides", schedule_overrides),
            )),
        ),
        th.Property(
            "category_ids",
            th.ArrayType(th.StringType),
        ),
        th.Property(
            "taxes",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("percent_rate", th.IntegerType),
                    th.Property("include_in_price", th.BooleanType),
                )
            ),
        ),
        th.Property(
            "modifier_groups",
            th.ArrayType(th.CustomType({"type": ["object", "string"]})),
        ),
        th.Property(
            "item_groups",
            th.ArrayType(th.CustomType({"type": ["object", "string"]})),
        ),
        th.Property("created_at", th.DateTimeType),
        th.Property("thumbnail_url", th.StringType),
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        """Normalize schedule string times on items and category references."""
        apply_schedule_normalization(row)
        for category_ref in row.get("category_references") or []:
            apply_schedule_normalization(category_ref)
        return row
