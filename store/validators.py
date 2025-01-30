from django.core.exceptions import ValidationError


def validate_product_price(price):
    if price <= 0:
        raise ValidationError({'price' : "The given price is invalid, price must be positive value greater than 0"})