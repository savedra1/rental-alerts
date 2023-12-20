
from utils.constants import MONTH_FORMATS
from datetime import datetime

def zoopla_date_convert(date_str: str): # -> str | None:
    # takes str for date in format "15th Dec 2023" and returns yyyy-mm-dd
    try:
        date_str = date_str.replace(' ', '')
        year = datetime.now().strftime('20%y')
        try:
            day = str(int(date_str[0:2]))
            double_digit_day = True
        except ValueError:
            day = str(int(date_str[0:1]))
            double_digit_day = False
        
        if double_digit_day:
            alpha_month = date_str[4:7]
        else:
            alpha_month = date_str[3:6]
            day = '0' + day
        
        numeric_month = MONTH_FORMATS[alpha_month]

        return f'{year}-{numeric_month}-{str(day)}'
    
    except Exception:
        return None
    
