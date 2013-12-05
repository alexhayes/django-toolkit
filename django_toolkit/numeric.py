from decimal import Decimal

def zero_if_none(value):
    if not value:
        return Decimal('0')
    return value

def percentage_change(first, second):
    if first in [None, 0] or second in [None, 0]:
        return None
    else:
        return ((Decimal(second) - Decimal(first)) / Decimal(first)) * 100