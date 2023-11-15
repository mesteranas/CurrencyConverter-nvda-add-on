#!/usr/bin/env python
import logging
import json
import re
import requests
from . import codes

__author__ = "Hariom"

logger = logging.getLogger(__name__)

CODES = codes.CODES

def convert(currency_from, currency_to, amnt, replace_commas=True):
    """
    Used to convert amount from one currency to another
    :param currency_from: Currency code from which amount needs to be converted
    :param currency_to: Currency code in which amount needs to be converted to
    :param amnt: Amount which needs to be converted
    :param replace_commas: If True than the commas will be removed from converted amount and the converted amount will
        be like 70000 otherwise it will return with comma like 70,000
    :return: Json
    """
    # Validate the parameters
    if not isinstance(currency_from, str):
        raise TypeError("currency_from should be of type str, passed %s" % type(currency_from))

    if not isinstance(currency_to, str):
        raise TypeError("currency_to should be of type str, passed %s" % type(currency_to))

    if not isinstance(amnt, float) and not isinstance(amnt, int):
        raise TypeError("amount should be either int or float, passed %s" % type(amnt))

    url = "http://216.58.221.46/search?q=convert+{amount}+{frm}+to+{to}&hl=en&lr=lang_en".format(amount = str(amnt),
                                                                                                 frm    = currency_from,
                                                                                                 to     = currency_to)

    currency_from = currency_from.upper()
    currency_to   = currency_to.upper()

    # This will be returned as default if the given code are not present in our database
    default_response = {
        "from"     : currency_from,  # From currency code
        "to"       : currency_to,    # To currency code
        "amount"   : 0,              # Amount of currency to be returned
        "converted": False           # Flag indicating whether the currency is converted or not
    }

    try:
        currency_to_name   = CODES[currency_to]

        # Just to check whether this currency exists in out currency code base or not
        currency_from_name = CODES[currency_from]

        # If currency_to_name and currency_from_name is same then user is just trying to convert the same currency and
        # we need to return the same value

        if currency_to_name == currency_from_name:
            default_response["converted"] = True
            default_response["amount"]    = float(amnt)
            return json.dumps(default_response)

        # response = requests.get(url)
        response = requests.get(url, headers={"Range": "bytes=0-1"})

        html = response.text

        results = re.findall("[\d*\,]*\.\d* {currency_to_name}".format(currency_to_name=currency_to_name), html)

        # converted_amount_str = "0.0 {to}".format(to=currency_to)
        if results.__len__() > 0:
            converted_amount_str = results[0]
            converted_currency = re.findall('[\d*\,]*\.\d*', converted_amount_str)[0]

            if replace_commas:
                converted_currency = converted_currency.replace(',', '')

            default_response["amount"]    = converted_currency
            default_response["converted"] = True
            return json.dumps(default_response)
        else:
            raise Exception("Unable to convert currency, failed to fetch results from Google")

    except KeyError as error:
        logger.error("Invalid currency codes passed in parameters, original exception message is -> %s" % error)

    except TypeError as error:
        logger.error(error)

    except Exception as error:
        logger.error(error)

    finally:
        return json.dumps(default_response)
