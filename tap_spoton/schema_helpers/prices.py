from hotglue_tap_sdk import typing as th

prices = (
    th.ObjectType(
        th.Property("amount", th.IntegerType),
        th.Property("pricing_kind", th.StringType)
    )
)
