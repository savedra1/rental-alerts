
MONTH_FORMATS = { # can be used to easily reformat date structures returned in HTML
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
}

BAD_STRINGS = [ # Strings to remove from html response to allow json formatting
    '"])</script><script>self.__next_f.push([1,"',
    '1,\n',
    ']")</script><script>self.__next_f.push("['
]

"""
String separators to use for each scraper when extracting 
the property json information from the HTML responses...
"""

RIGHTMOVE_HTML_EXTRACTION = {
    'start': '<script>window.jsonModel = ',
    'end': '</script><script>'
}

ZOOPLA_HTML_EXTRACTION = {
      'start': '"regularListingsFormatted":',
      'end':  ',"transactionType"'
}

OTM_HTML_EXTRACTION = {
    'start': '__OTM__.jsonData = ',
    'end': ' __OTM__.globals = '
}

