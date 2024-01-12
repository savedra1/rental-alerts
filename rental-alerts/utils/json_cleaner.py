from utils.constants import BAD_STRINGS

def clean_json(json_string: str) -> str:
    for string in BAD_STRINGS:
        json_string = json_string.replace(string, '')
    return json_string