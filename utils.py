# utils.py

import re
from palavras import PALAVRAS

def read_file(file_path):
    with open(f'{file_path}.241', 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def uppercase_menos_sequencias(string):
    # Function to convert match to uppercase if it's not an escape sequence
    def to_upper_except_escapes(match):
        if match.group() in ['\\n', '\\t', '\\r']:
            return match.group()
        return match.group().upper()

    # Replace each match using the custom function
    return re.sub(r'\\[ntr]|.', to_upper_except_escapes, string)

def determinar_escopo(previous_token):
    # : -> nomFuncao
    if previous_token == 'B05':
        return 'C05'
    
    # programa -> nomPrograma
    elif previous_token == 'A17':
        return 'C06'
    
    # variavel
    else:
        return 'C07'
    
def get_codigo(lexeme):
    for padrao, codigo in PALAVRAS:
        if re.fullmatch(padrao, lexeme):
            return codigo
    return None