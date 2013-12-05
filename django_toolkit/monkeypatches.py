import money
import django

def format_money_remove_aud(self, **kwargs):
    """
    Monkey patch money.Money.format so that the default currency (AUD) isn't displayed
    when calling Money.format()
    
    @author: Alex Hayes <alex.hayes@roi.com.au>
    """
    from money.localization import format_money
    return format_money(self, **kwargs).replace('A$', '$')

money.Money.format = format_money_remove_aud
