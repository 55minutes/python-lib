from fiftyfive.metaclass import PluginMount

__all__ = ('CreditCardValidators',)

class CreditCardValidationError(Exception):
    pass

class CreditCardValidators(object):
    """
    Plugins extending this class will be used to verify credit card
    numbers.

    Valid plugins must provide the following **cls** method:

    verify(cc_number):
        Either finishes silently or raises a CreditCardValidationError error.
    """
    __metaclass__ = PluginMount

    error = CreditCardValidationError

class Luhn(CreditCardValidators):
    "See http://en.wikipedia.org/wiki/Luhn_algorithm for more info."
    def verify(cls, ccn):
        digits = [int(i) for i in list(str(ccn))]
        _sum = 0
        alt = False
        for d in reversed(digits):
            if alt:
                d *= 2
                if d > 9:
                    d -= 9
            _sum += d
            alt = not alt
        if not (_sum % 10) == 0:
            raise cls.error("Invalid credit card number")

# TODO: http://en.wikipedia.org/wiki/Credit_card_numbers
