import datetime
from django.core.serializers.json import DjangoJSONEncoder
from money.Money import Money as OldMoney
from moneyed import Money
from django.utils.timezone import is_aware
import decimal


class JSONEncoder(DjangoJSONEncoder):

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, datetime.timedelta):
            value = abs(o)  # all durations are positive
            return (
                value.days * 24 * 3600 * 1000000
                + value.seconds * 1000000
                + value.microseconds
            )
        elif isinstance(o, Money) or isinstance(o, OldMoney):
            return '%s' % o
        else:
            return super(DjangoJSONEncoder, self).default(o)