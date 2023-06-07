"""Stream type classes for tap-magento."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_magento.client import MagentoStream
import requests

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class UsersStream(MagentoStream):
    """Define custom stream."""

    name = "users"
    path = "/users"
    primary_keys = ["id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("id", th.StringType, description="The user's system ID"),
        th.Property("age", th.NumberType, description="The user's age in years"),
        th.Property("email", th.StringType, description="The user's email address"),
        th.Property("street", th.StringType),
        th.Property("city", th.StringType),
        th.Property(
            "state", th.StringType, description="State name in ISO 3166-2 format"
        ),
        th.Property("zip", th.StringType),
    ).to_dict()


class OrdersStream(MagentoStream):
    """Define Order Stream"""

    name = "orders"
    path = "/orders"
    primary_keys = []  # TODO
    replication_key = "updated_at"

    schema = th.PropertiesList(
        th.Property("adjustment_negative", th.NumberType),
        th.Property("adjustment_positive", th.NumberType),
        th.Property("applied_rule_ids", th.StringType),
        th.Property("base_adjustment_negative", th.NumberType),
        th.Property("base_adjustment_positive", th.NumberType),
        th.Property("base_currency_code", th.StringType),
        th.Property("base_discount_amount", th.NumberType),
        th.Property("base_discount_canceled", th.NumberType),
        th.Property("base_discount_invoiced", th.NumberType),
        th.Property("base_discount_refunded", th.NumberType),
        th.Property("base_grand_total", th.NumberType),
        th.Property("base_discount_tax_compensation_amount", th.NumberType),
        th.Property("base_discount_tax_compensation_invoiced", th.NumberType),
        th.Property("base_discount_tax_compensation_refunded", th.NumberType),
        th.Property("base_shipping_amount", th.NumberType),
        th.Property("base_shipping_canceled", th.NumberType),
        th.Property("base_shipping_discount_amount", th.NumberType),
        th.Property("base_shipping_discount_tax_compensation_amnt", th.NumberType),
        th.Property("base_shipping_incl_tax", th.NumberType),
        th.Property("base_shipping_invoiced", th.NumberType),
        th.Property("base_shipping_refunded", th.NumberType),
        th.Property("base_shipping_tax_amount", th.NumberType),
        th.Property("base_shipping_tax_refunded", th.NumberType),
        th.Property("base_subtotal", th.NumberType),
        th.Property("base_subtotal_canceled", th.NumberType),
        th.Property("base_subtotal_incl_tax", th.NumberType),
        th.Property("base_subtotal_invoiced", th.NumberType),
        th.Property("base_subtotal_refunded", th.NumberType),
        th.Property("base_tax_amount", th.NumberType),
        th.Property("base_tax_canceled", th.NumberType),
        th.Property("base_tax_invoiced", th.NumberType),
        th.Property("base_tax_refunded", th.NumberType),
        th.Property("base_total_canceled", th.NumberType),
        th.Property("base_total_due", th.NumberType),
        th.Property("base_total_invoiced", th.NumberType),
        th.Property("base_total_invoiced_cost", th.NumberType),
        th.Property("base_total_offline_refunded", th.NumberType),
        th.Property("base_total_online_refunded", th.NumberType),
        th.Property("base_total_paid", th.NumberType),
        th.Property("base_total_qty_ordered", th.NumberType),
        th.Property("base_total_refunded", th.NumberType),
        th.Property("base_to_global_rate", th.NumberType),
        th.Property("base_to_order_rate", th.NumberType),
        th.Property("billing_address_id", th.NumberType),
        th.Property("can_ship_partially", th.NumberType),
        th.Property("can_ship_partially_item", th.NumberType),
        th.Property("coupon_code", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("customer_dob", th.StringType),
        th.Property("customer_email", th.StringType),
        th.Property("customer_firstname", th.StringType),
        th.Property("customer_gender", th.NumberType),
        th.Property("customer_group_id", th.NumberType),
        th.Property("customer_id", th.NumberType),
        th.Property("customer_is_guest", th.NumberType),
        th.Property("customer_lastname", th.StringType),
        th.Property("customer_middlename", th.StringType),
        th.Property("customer_note", th.StringType),
        th.Property("customer_note_notify", th.NumberType),
        th.Property("customer_prefix", th.StringType),
        th.Property("customer_suffix", th.StringType),
        th.Property("customer_taxvat", th.StringType),
        th.Property("discount_amount", th.NumberType),
        th.Property("discount_canceled", th.NumberType),
        th.Property("discount_description", th.StringType),
        th.Property("discount_invoiced", th.NumberType),
        th.Property("discount_refunded", th.NumberType),
        th.Property("edit_increment", th.NumberType),
        th.Property("email_sent", th.NumberType),
        th.Property("entity_id", th.NumberType),
        th.Property("ext_customer_id", th.StringType),
        th.Property("ext_order_id", th.StringType),
        th.Property("forced_shipment_with_invoice", th.NumberType),
        th.Property("global_currency_code", th.StringType),
        th.Property("grand_total", th.NumberType),
        th.Property("discount_tax_compensation_amount", th.NumberType),
        th.Property("discount_tax_compensation_invoiced", th.NumberType),
        th.Property("discount_tax_compensation_refunded", th.NumberType),
        th.Property("hold_before_state", th.StringType),
        th.Property("hold_before_status", th.StringType),
        th.Property("increment_id", th.StringType),
        th.Property("is_virtual", th.NumberType),
        th.Property("order_currency_code", th.StringType),
        th.Property("original_increment_id", th.StringType),
        th.Property("payment_authorization_amount", th.NumberType),
        th.Property("payment_auth_expiration", th.NumberType),
        th.Property("protect_code", th.StringType),
        th.Property("quote_address_id", th.NumberType),
        th.Property("quote_id", th.NumberType),
        th.Property("relation_child_id", th.StringType),
        th.Property("relation_child_real_id", th.StringType),
        th.Property("relation_parent_id", th.StringType),
        th.Property("relation_parent_real_id", th.StringType),
        th.Property("remote_ip", th.StringType),
        th.Property("shipping_amount", th.NumberType),
        th.Property("shipping_canceled", th.NumberType),
        th.Property("shipping_description", th.StringType),
        th.Property("shipping_discount_amount", th.NumberType),
        th.Property("shipping_discount_tax_compensation_amount", th.NumberType),
        th.Property("shipping_incl_tax", th.NumberType),
        th.Property("shipping_invoiced", th.NumberType),
        th.Property("shipping_refunded", th.NumberType),
        th.Property("shipping_tax_amount", th.NumberType),
        th.Property("shipping_tax_refunded", th.NumberType),
        th.Property("state", th.StringType),
        th.Property("status", th.StringType),
        th.Property("store_currency_code", th.StringType),
        th.Property("store_id", th.NumberType),
        th.Property("store_name", th.StringType),
        th.Property("store_to_base_rate", th.NumberType),
        th.Property("store_to_order_rate", th.NumberType),
        th.Property("subtotal", th.NumberType),
        th.Property("subtotal_canceled", th.NumberType),
        th.Property("subtotal_incl_tax", th.NumberType),
        th.Property("subtotal_invoiced", th.NumberType),
        th.Property("subtotal_refunded", th.NumberType),
        th.Property("tax_amount", th.NumberType),
        th.Property("tax_canceled", th.NumberType),
        th.Property("tax_invoiced", th.NumberType),
        th.Property("tax_refunded", th.NumberType),
        th.Property("total_canceled", th.NumberType),
        th.Property("total_due", th.NumberType),
        th.Property("total_invoiced", th.NumberType),
        th.Property("total_item_count", th.NumberType),
        th.Property("total_offline_refunded", th.NumberType),
        th.Property("total_online_refunded", th.NumberType),
        th.Property("total_paid", th.NumberType),
        th.Property("total_qty_ordered", th.NumberType),
        th.Property("total_refunded", th.NumberType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("weight", th.NumberType),
        th.Property("x_forwarded_for", th.StringType),
        th.Property("items", th.ArrayType(th.CustomType({"type": ["null", "object"]}))),
        th.Property("billing_address", th.CustomType({"type": ["object", "string"]})),
        th.Property("payment", th.CustomType({"type": ["object", "string"]})),
        th.Property(
            "status_histories",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
        th.Property(
            "extension_attributes", th.CustomType({"type": ["object", "string"]})
        ),
    ).to_dict()


class ProductsAttributeStream(MagentoStream):
    name = "products_attribute"
    path = "/products/attributes"
    primary_keys = ["attribute_id"]
    schema = th.PropertiesList(
        th.Property("is_wysiwyg_enabled", th.BooleanType),
        th.Property("is_html_allowed_on_front", th.BooleanType),
        th.Property("used_for_sort_by", th.BooleanType),
        th.Property("is_filterable", th.BooleanType),
        th.Property("is_filterable_in_search", th.BooleanType),
        th.Property("is_used_in_grid", th.BooleanType),
        th.Property("is_visible_in_grid", th.BooleanType),
        th.Property("is_filterable_in_grid", th.BooleanType),
        th.Property("position", th.NumberType),
        th.Property(
            "apply_to",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
        th.Property("is_searchable", th.StringType),
        th.Property("is_visible_in_advanced_search", th.StringType),
        th.Property("is_comparable", th.StringType),
        th.Property("is_used_for_promo_rules", th.StringType),
        th.Property("is_visible_on_front", th.StringType),
        th.Property("used_in_product_listing", th.StringType),
        th.Property("is_visible", th.BooleanType),
        th.Property("scope", th.StringType),
        th.Property("attribute_id", th.NumberType),
        th.Property("attribute_code", th.StringType),
        th.Property("frontend_input", th.StringType),
        th.Property("entity_type_id", th.StringType),
        th.Property("is_required", th.BooleanType),
        th.Property(
            "options",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
        th.Property("is_user_defined", th.BooleanType),
        th.Property("default_frontend_label", th.StringType),
        th.Property(
            "frontend_labels",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
        th.Property("note", th.StringType),
        th.Property("backend_type", th.StringType),
        th.Property("backend_model", th.StringType),
        th.Property("source_model", th.StringType),
        th.Property("default_value", th.StringType),
        th.Property("is_unique", th.StringType),
        th.Property("frontend_class", th.StringType),
        th.Property(
            "validation_rules",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
    ).to_dict()


class ProductsStream(MagentoStream):

    name = "products"
    path = "/products"
    primary_keys = ["id"]
    replication_key = "updated_at"

    schema = th.PropertiesList(
        th.Property("id", th.NumberType),
        th.Property("sku", th.StringType),
        th.Property("name", th.StringType),
        th.Property("attribute_set_id", th.NumberType),
        th.Property("price", th.NumberType),
        th.Property("status", th.NumberType),
        th.Property("visibility", th.NumberType),
        th.Property("type_id", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("weight", th.NumberType),
        th.Property(
            "extension_attributes", th.CustomType({"type": ["object", "string"]})
        ),
        th.Property(
            "product_links",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
        th.Property(
            "options",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
        th.Property(
            "media_gallery_entries",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
        th.Property(
            "tier_prices",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
        th.Property(
            "custom_attributes",
            th.ArrayType(th.CustomType({"type": ["null", "object"]})),
        ),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "product_sku": record["sku"],
        }


class ProductItemStocksStream(MagentoStream):

    name = "product_item_stocks"
    path = "/stockItems/{product_sku}"
    primary_keys = ["item_id"]
    records_jsonpath: str = "$[*]"
    replication_key = None
    parent_stream_type = ProductsStream
    schema = th.PropertiesList(
        th.Property("id", th.NumberType),
        th.Property("item_id", th.NumberType),
        th.Property("product_id", th.NumberType),
        th.Property("stock_id", th.NumberType),
        th.Property("qty", th.NumberType),
        th.Property("is_in_stock", th.BooleanType),
        th.Property("is_qty_decimal", th.BooleanType),
        th.Property("show_default_notification_message", th.BooleanType),
        th.Property("use_config_min_qty", th.BooleanType),
        th.Property("min_qty", th.NumberType),
        th.Property("use_config_min_sale_qty", th.NumberType),
        th.Property("min_sale_qty", th.NumberType),
        th.Property("use_config_max_sale_qty", th.BooleanType),
        th.Property("max_sale_qty", th.NumberType),
        th.Property("use_config_backorders", th.BooleanType),
        th.Property("backorders", th.NumberType),
        th.Property("use_config_notify_stock_qty", th.BooleanType),
        th.Property("notify_stock_qty", th.NumberType),
        th.Property("use_config_qty_increments", th.BooleanType),
        th.Property("qty_increments", th.NumberType),
        th.Property("use_config_enable_qty_inc", th.BooleanType),
        th.Property("enable_qty_increments", th.BooleanType),
        th.Property("use_config_manage_stock", th.BooleanType),
        th.Property("manage_stock", th.BooleanType),
        th.Property("low_stock_date", th.DateTimeType),
        th.Property("is_decimal_divided", th.BooleanType),
        th.Property("stock_status_changed_auto", th.NumberType),
    ).to_dict()


class CategoryStream(MagentoStream):

    name = "categories"
    path = "/categories/list"
    primary_keys = ["id"]
    records_jsonpath: str = "$.items[*]"
    replication_key = "updated_at"
    schema = th.PropertiesList(
        th.Property("id", th.NumberType),
        th.Property("parent_id", th.NumberType),
        th.Property("name", th.StringType),
        th.Property("is_active", th.BooleanType),
        th.Property("position", th.NumberType),
        th.Property("level", th.NumberType),
        th.Property("children", th.StringType),
        th.Property("created_at", th.DateTimeType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("path", th.StringType),
        th.Property("include_in_menu", th.BooleanType),
        th.Property("available_sort_by", th.CustomType({"type": ["array", "string"]})),
        th.Property("custom_attributes", th.CustomType({"type": ["array", "string"]})),
    ).to_dict()


class SaleRulesStream(MagentoStream):

    name = "salerules"
    path = "/salesRules/search"
    primary_keys = ["rule_id"]
    records_jsonpath: str = "$.items[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("rule_id", th.NumberType),
        th.Property("name", th.StringType),
        th.Property("store_labels", th.CustomType({"type": ["array", "string"]})),
        th.Property("description", th.StringType),
        th.Property("website_ids", th.CustomType({"type": ["array", "string"]})),
        th.Property("customer_group_ids", th.CustomType({"type": ["array", "string"]})),
        th.Property("from_date", th.DateTimeType),
        th.Property("uses_per_customer", th.NumberType),
        th.Property("is_active", th.BooleanType),
        th.Property("condition", th.CustomType({"type": ["object", "string"]})),
        th.Property("action_condition", th.CustomType({"type": ["object", "string"]})),
        th.Property("stop_rules_processing", th.BooleanType),
        th.Property("is_advanced", th.BooleanType),
        th.Property("sort_order", th.NumberType),
        th.Property("simple_action", th.StringType),
        th.Property("discount_amount", th.NumberType),
        th.Property("discount_step", th.NumberType),
        th.Property("apply_to_shipping", th.BooleanType),
        th.Property("times_used", th.NumberType),
        th.Property("is_rss", th.BooleanType),
        th.Property("coupon_type", th.StringType),
        th.Property("use_auto_generation", th.BooleanType),
        th.Property("uses_per_coupon", th.NumberType),
        th.Property("simple_free_shipping", th.StringType),
        th.Property(
            "extension_attributes", th.CustomType({"type": ["object", "string"]})
        ),
    ).to_dict()


class CouponsStream(MagentoStream):

    name = "coupons"
    path = "/coupons/search"
    primary_keys = ["coupon_id"]
    records_jsonpath: str = "$.items[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("coupon_id", th.NumberType),
        th.Property("rule_id", th.NumberType),
        th.Property("code", th.StringType),
        th.Property("usage_limit", th.NumberType),
        th.Property("times_used", th.NumberType),
        th.Property("is_primary", th.BooleanType),
        th.Property("type", th.NumberType),
    ).to_dict()


class InvoicesStream(MagentoStream):

    name = "invoices"
    path = "/invoices"
    primary_keys = ["increment_id"]
    records_jsonpath: str = "$.items[*]"
    replication_key = "updated_at"
    schema = th.PropertiesList(
        th.Property("base_currency_code", th.StringType),
        th.Property("base_discount_amount", th.NumberType),
        th.Property("base_grand_total", th.NumberType),
        th.Property("base_discount_tax_compensation_amount", th.NumberType),
        th.Property("base_shipping_amount", th.NumberType),
        th.Property("base_shipping_discount_tax_compensation_amnt", th.NumberType),
        th.Property("base_shipping_incl_tax", th.NumberType),
        th.Property("base_shipping_tax_amount", th.NumberType),
        th.Property("base_subtotal", th.NumberType),
        th.Property("base_subtotal_incl_tax", th.NumberType),
        th.Property("base_tax_amount", th.NumberType),
        th.Property("base_total_refunded", th.NumberType),
        th.Property("base_to_global_rate", th.NumberType),
        th.Property("base_to_order_rate", th.NumberType),
        th.Property("billing_address_id", th.NumberType),
        th.Property("can_void_flag", th.NumberType),
        th.Property("created_at", th.DateTimeType),
        th.Property("discount_amount", th.NumberType),
        th.Property("discount_description", th.StringType),
        th.Property("email_sent", th.NumberType),
        th.Property("entity_id", th.NumberType),
        th.Property("global_currency_code", th.StringType),
        th.Property("grand_total", th.NumberType),
        th.Property("discount_tax_compensation_amount", th.NumberType),
        th.Property("increment_id", th.StringType),
        th.Property("is_used_for_refund", th.NumberType),
        th.Property("order_currency_code", th.StringType),
        th.Property("order_id", th.NumberType),
        th.Property("shipping_address_id", th.NumberType),
        th.Property("shipping_amount", th.NumberType),
        th.Property("shipping_discount_tax_compensation_amount", th.NumberType),
        th.Property("shipping_incl_tax", th.NumberType),
        th.Property("shipping_tax_amount", th.NumberType),
        th.Property("state", th.NumberType),
        th.Property("store_currency_code", th.StringType),
        th.Property("store_id", th.NumberType),
        th.Property("store_to_base_rate", th.NumberType),
        th.Property("store_to_order_rate", th.NumberType),
        th.Property("subtotal", th.NumberType),
        th.Property("subtotal_incl_tax", th.NumberType),
        th.Property("tax_amount", th.NumberType),
        th.Property("total_qty", th.NumberType),
        th.Property("transaction_id", th.StringType),
        th.Property("updated_at", th.DateTimeType),
        th.Property("items", th.CustomType({"type": ["array", "string"]})),
        th.Property("comments", th.CustomType({"type": ["array", "string"]})),
        th.Property("extension_attributes", th.CustomType(
            {"type": ["object", "string"]})),
    ).to_dict()
