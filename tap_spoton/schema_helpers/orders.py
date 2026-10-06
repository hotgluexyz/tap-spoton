from hotglue_tap_sdk import typing as th

applicable_taxes_schema =  th.ObjectType(
    th.Property("tax_id", th.StringType),
    th.Property("tax_amount", th.NumberType),
    th.Property("is_inclusive", th.BooleanType),
    th.Property("parent_id", th.StringType),
    th.Property("parent_type", th.StringType),
)

taxes_schema = th.ObjectType(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("amount", th.NumberType),
    th.Property("percentage", th.NumberType),
    th.Property("is_inclusive", th.BooleanType),
    th.Property("parent_id", th.StringType),
    th.Property("parent_type", th.StringType),
)

line_items_schema = th.ObjectType(
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
                th.Property("order_modifier_id", th.StringType),
                th.Property("net_sales_amount", th.NumberType),
                th.Property("inclusive_taxes_amount", th.NumberType),
                th.Property("exclusive_taxes_amount", th.NumberType),
                th.Property("discounts_amount", th.NumberType),
            )
        ),
    ),
    th.Property(
        "applicable_taxes",
        th.ArrayType(applicable_taxes_schema),
    ),
    th.Property("order_item_id", th.StringType),
    th.Property("gross_sales_amount", th.NumberType),
    th.Property("net_sales_amount", th.NumberType),
    th.Property("inclusive_taxes_amount", th.NumberType),
    th.Property("exclusive_taxes_amount", th.NumberType),
    th.Property("void", th.CustomType({"type": ["object", "boolean"]})),
)
