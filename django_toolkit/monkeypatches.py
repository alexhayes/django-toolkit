try:
    import moneyed as money
    from moneyed.localization import format_money
except ImportError:
    try:
        import money
        from money.localization import format_money
    except ImportError:
        money = None


def format_money_remove_aud(self, **kwargs):
    """
    Monkey patch money.Money.format so that the default currency (AUD) isn't displayed
    when calling Money.format()

    @author: Alex Hayes <alex.hayes@roi.com.au>
    """
    return format_money(self, **kwargs).replace('A$', '$')

if money:
    money.Money.format = format_money_remove_aud
