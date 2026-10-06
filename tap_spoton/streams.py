"""Stream type classes for tap-spoton."""

from typing import Iterable, Optional

from hotglue_tap_sdk import typing as th

from tap_spoton.client import SpotOnStream
from tap_spoton.schema_helpers.schedules import (
    day_times_object,
    schedule_object,
    schedule_overrides_string,
    schedule_string,
)
from tap_spoton.schema_helpers.prices import prices
from tap_spoton.schema_helpers.orders import taxes_schema, line_items_schema

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
        th.Property("location_id", th.StringType),
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
                    day_times_object,
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
                        schedule_object,
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
                line_items_schema,
            ),
        ),
        th.Property(
            "payments",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("type", th.StringType),
                    th.Property("amount", th.NumberType),
                    th.Property("is_refund", th.BooleanType),
                    th.Property("is_void", th.BooleanType),
                    th.Property("order_payment_id", th.StringType),
                    th.Property("card_type", th.StringType),
                    th.Property("tips_amount", th.NumberType),
                    th.Property("tip_deduction_amount", th.NumberType),
                    th.Property("fees_amount", th.NumberType),
                    th.Property("surcharges", th.ArrayType(th.ObjectType(
                        th.Property("id", th.StringType),
                        th.Property("name", th.StringType),
                        th.Property("amount", th.NumberType),
                    ))),
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
                th.Property("items_discounts_amount", th.NumberType),
                th.Property("liabilities_discounts_amount", th.NumberType),
                th.Property("credit_card_surcharges_amount", th.NumberType),
                th.Property("rounding_amount", th.NumberType),
                th.Property("revenue_amount", th.NumberType),
                th.Property("taxes_collected_amount", th.NumberType),
                th.Property("inclusive_taxes_collected_amount", th.NumberType),
                th.Property("exclusive_taxes_collected_amount", th.NumberType),
                th.Property("facilitator_tax_adjustment_amount", th.NumberType),
                th.Property("payments_collected_amount", th.NumberType),
                th.Property("payments_uncollected_amount", th.NumberType),
            ),
        ),
        th.Property(
            "discounts",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("amount", th.NumberType),
                    th.Property("order_discount_id", th.StringType),
                    th.Property("discount_reason", th.StringType),
                    th.Property("parent_id", th.StringType),
                    th.Property("parent_type", th.StringType),
                )
            ),
        ),
        th.Property("created_at", th.DateTimeType),
        th.Property("last_updated_at", th.DateTimeType),
        th.Property("closed_at", th.DateTimeType),
        th.Property(
            "taxes",
            th.ArrayType(
                taxes_schema,
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
        th.Property("fiscal_date", th.DateType),
        th.Property("order_time_zone", th.StringType),
        th.Property("order_type", th.StringType),
        th.Property("original_order_id", th.StringType),
        th.Property("original_order_number", th.StringType),
        th.Property("open_daypart", th.StringType),
        th.Property("station_id", th.StringType),
        th.Property("released_at", th.DateTimeType),
        th.Property("liabilities", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("amount", th.NumberType),
            th.Property("quantity", th.NumberType),
        ))),
        th.Property("voided_line_items", th.ArrayType(line_items_schema)),
        th.Property("checks", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("payments_uncollected", th.NumberType),
            th.Property("gratuity_amount", th.NumberType),
            th.Property("auto_gratuity_taxes", th.StringType),
            th.Property("guests", th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("check_id", th.StringType),
                    th.Property("items", th.ArrayType(line_items_schema)),
                    th.Property("void_items", th.ArrayType(line_items_schema)),
                )
            )),
        ))),
        th.Property("fees", th.ArrayType(th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("name", th.StringType),
            th.Property("order_fee_id", th.StringType),
        ))),
        th.Property("customer", th.ObjectType(
            th.Property("id", th.StringType),
            th.Property("first_name", th.StringType),
            th.Property("last_name", th.StringType),
            th.Property("email", th.StringType),
            th.Property("phone", th.StringType),
            th.Property("address", th.StringType),
            th.Property("city", th.StringType),
            th.Property("state", th.StringType),
            th.Property("zip", th.StringType),
        )),
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
            schedule_string,
        ),
        th.Property(
            "schedule_overrides",
            schedule_overrides_string,
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
            schedule_string,
        ),
        th.Property(
            "category_references",
            th.ArrayType(th.ObjectType(
                th.Property("category_id", th.StringType),
                th.Property("sort_order", th.IntegerType),
                th.Property("price", prices),
                th.Property("schedule", schedule_string),
                th.Property("schedule_overrides", schedule_overrides_string),
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
