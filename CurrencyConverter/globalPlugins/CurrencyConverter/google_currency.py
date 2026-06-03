import threading
import time
import tones
import requests
CODES = {
    "AFN": "Afghan Afghani",
    "ALL": "Albanian Lek",
    "DZD": "Algerian Dinar",
    "AOA": "Angolan Kwanza",
    "ARS": "Argentine Peso",
    "AMD": "Armenian Dram",
    "AWG": "Aruban Florin",
    "AUD": "Australian Dollar",
    "AZN": "Azerbaijani Manat",
    "BSD": "Bahamian Dollar",
    "BHD": "Bahraini Dinar",
    "BBD": "Bajan dollar",
    "BDT": "Bangladeshi Taka",
    "BYR": "Belarusian Ruble",
    "BYN": "Belarusian Ruble",
    "BZD": "Belize Dollar",
    "BMD": "Bermudan Dollar",
    "BTN": "Bhutan currency",
    "BTC": "Bitcoin",
    "BCH": "Bitcoin Cash",
    "BOB": "Bolivian Boliviano",
    "BAM": "Bosnia-Herzegovina Convertible Mark",
    "BWP": "Botswanan Pula",
    "BRL": "Brazilian Real",
    "BND": "Brunei Dollar",
    "BGN": "Bulgarian Lev",
    "BIF": "Burundian Franc",
    "XPF": "CFP Franc",
    "KHR": "Cambodian riel",
    "CAD": "Canadian Dollar",
    "CVE": "Cape Verdean Escudo",
    "KYD": "Cayman Islands Dollar",
    "XAF": "Central African CFA franc",
    "CLP": "Chilean Peso",
    "CLF": "Chilean Unit of Account (UF)",
    "CNY": "Chinese Yuan",
    "CNH": "Chinese Yuan (offshore)",
    "COP": "Colombian Peso",
    "KMF": "Comorian franc",
    "CDF": "Congolese Franc",
    "CRC": "Costa Rican Colón",
    "HRK": "Croatian Kuna",
    "CUP": "Cuban Peso",
    "CZK": "Czech Koruna",
    "DKK": "Danish Krone",
    "DJF": "Djiboutian Franc",
    "DOP": "Dominican Peso",
    "XCD": "East Caribbean Dollar",
    "EGP": "Egyptian Pound",
    "ETH": "Ether",
    "ETB": "Ethiopian Birr",
    "EUR": "Euro",
    "FJD": "Fijian Dollar",
    "GMD": "Gambian dalasi",
    "GEL": "Georgian Lari",
    "GHC": "Ghanaian Cedi",
    "GHS": "Ghanaian Cedi",
    "GIP": "Gibraltar Pound",
    "GTQ": "Guatemalan Quetzal",
    "GNF": "Guinean Franc",
    "GYD": "Guyanaese Dollar",
    "HTG": "Haitian Gourde",
    "HNL": "Honduran Lempira",
    "HKD": "Hong Kong Dollar",
    "HUF": "Hungarian Forint",
    "ISK": "Icelandic Króna",
    "INR": "Indian Rupee",
    "IDR": "Indonesian Rupiah",
    "IRR": "Iranian Rial",
    "IQD": "Iraqi Dinar",
    "ILS": "Israeli New Shekel",
    "JMD": "Jamaican Dollar",
    "JPY": "Japanese Yen",
    "JOD": "Jordanian Dinar",
    "KZT": "Kazakhstani Tenge",
    "KES": "Kenyan Shilling",
    "KWD": "Kuwaiti Dinar",
    "KGS": "Kyrgystani Som",
    "LAK": "Laotian Kip",
    "LBP": "Lebanese pound",
    "LSL": "Lesotho loti",
    "LRD": "Liberian Dollar",
    "LYD": "Libyan Dinar",
    "LTC": "Litecoin",
    "MOP": "Macanese Pataca",
    "MKD": "Macedonian Denar",
    "MGA": "Malagasy Ariary",
    "MWK": "Malawian Kwacha",
    "MYR": "Malaysian Ringgit",
    "MVR": "Maldivian Rufiyaa",
    "MRO": "Mauritanian Ouguiya (1973–2017)",
    "MUR": "Mauritian Rupee",
    "MXN": "Mexican Peso",
    "MDL": "Moldovan Leu",
    "MAD": "Moroccan Dirham",
    "MZM": "Mozambican metical",
    "MZN": "Mozambican metical",
    "MMK": "Myanmar Kyat",
    "TWD": "New Taiwan dollar",
    "NAD": "Namibian dollar",
    "NPR": "Nepalese Rupee",
    "ANG": "Netherlands Antillean Guilder",
    "NZD": "New Zealand Dollar",
    "NIO": "Nicaraguan Córdoba",
    "NGN": "Nigerian Naira",
    "NOK": "Norwegian Krone",
    "OMR": "Omani Rial",
    "PKR": "Pakistani Rupee",
    "PAB": "Panamanian Balboa",
    "PGK": "Papua New Guinean Kina",
    "PYG": "Paraguayan Guarani",
    "PHP": "Philippine Piso",
    "PLN": "Poland złoty",
    "GBP": "Pound sterling",
    "QAR": "Qatari Rial",
    "ROL": "Romanian Leu",
    "RON": "Romanian Leu",
    "RUR": "Russian Ruble",
    "RUB": "Russian Ruble",
    "RWF": "Rwandan franc",
    "SVC": "Salvadoran Colón",
    "SAR": "Saudi Riyal",
    "CSD": "Serbian Dinar",
    "RSD": "Serbian Dinar",
    "SCR": "Seychellois Rupee",
    "SLL": "Sierra Leonean Leone",
    "SGD": "Singapore Dollar",
    "PEN": "Sol",
    "SBD": "Solomon Islands Dollar",
    "SOS": "Somali Shilling",
    "ZAR": "South African Rand",
    "KRW": "South Korean won",
    "VEF": "Sovereign Bolivar",
    "XDR": "Special Drawing Rights",
    "LKR": "Sri Lankan Rupee",
    "SSP": "Sudanese pound",
    "SDG": "Sudanese pound",
    "SRD": "Surinamese Dollar",
    "SZL": "Swazi Lilangeni",
    "SEK": "Swedish Krona",
    "CHF": "Swiss Franc",
    "TJS": "Tajikistani Somoni",
    "TZS": "Tanzanian Shilling",
    "THB": "Thai Baht",
    "TOP": "Tongan Paʻanga",
    "TTD": "Trinidad & Tobago Dollar",
    "TND": "Tunisian Dinar",
    "TRY": "Turkish lira",
    "TMM": "Turkmenistan manat",
    "TMT": "Turkmenistan manat",
    "UGX": "Ugandan Shilling",
    "UAH": "Ukrainian hryvnia",
    "AED": "United Arab Emirates Dirham",
    "USD": "United States Dollar",
    "UYU": "Uruguayan Peso",
    "UZS": "Uzbekistani Som",
    "VND": "Vietnamese dong",
    "XOF": "West African CFA franc",
    "YER": "Yemeni Rial",
    "ZMW": "Zambian Kwacha"
}

baseURL = "https://open.er-api.com/v6/latest/"
def beep_loop(stop_event):
    while not stop_event.is_set():
        tones.beep(500, 100)
        time.sleep(0.5)

def fetch_conversion(From, To, amount, result_container):
    try:
        response = requests.get(baseURL + From.upper())
        if response.status_code != 200:
            result_container.append(_("an Error detected.\nStatus code is ") + str(response.status_code))
            return
        data = response.json()
        if data.get("result") != "success":
            result_container.append(_("An error detected\n"))
            return
        rates = data.get("rates", {})
        if To.upper() not in rates:
            result_container.append(_("An error detected\n"))
            return
        rate = rates[To.upper()]
        RAmount = rate * amount
        result_container.append(str(RAmount))
    except Exception as E:
        result_container.append(_("An error detected\n") + str(E))
def convert(From: str, To: str, amount: int):
    result_container = []
    stop_beep = threading.Event()
    beep_thread = threading.Topic = threading.Thread(target=beep_loop, args=(stop_beep,))
    calc_thread = threading.Thread(target=fetch_conversion, args=(From, To, amount, result_container))
    beep_thread.start()
    calc_thread.start()
    calc_thread.join()
    stop_beep.set()
    beep_thread.join()
    return result_container[0] if result_container else _("An error detected\n")