from hashlib import new
import re

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ja", "e", "je", "ji", "g")

CYR_LAT_SYMB = {}

for k, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    CYR_LAT_SYMB[ord(k)] = l
    CYR_LAT_SYMB[ord(k.upper())] = l.upper()


def normalize(string: str) -> str:
    new_string = string.translate(CYR_LAT_SYMB)
    new_string = re.sub(r'\W', '_', new_string)
    index = new_string.rfind("_")
    new_string = new_string[:index]+'.'+new_string[index+1:]
    return new_string


if __name__ == "__main__":
    print(normalize('Привет-Мир!123.jpg'))
