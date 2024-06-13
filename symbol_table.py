# symbol_table.py

from utils import get_codigo

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.index = 0

    def add(self, lexeme, token_type, qtd_antes_truncar, current_line):
        if lexeme not in self.symbols:

            self.symbols[lexeme] = {
                'Index': self.index,
                'Codigo': token_type,
                'Lexeme': lexeme,
                'QtdAntesTruncar': qtd_antes_truncar,
                'QtdCharDpsTruncar': len(lexeme),
                'Qtd': 1,
                'Tipo': get_codigo(lexeme),
                'Linhas': [current_line],
            }
            self.index += 1
        else:
            self.add_line(current_line)
            self.symbols[lexeme]['Qtd'] += 1

    def add_line(self, lexeme, current_line):
        self.symbols[lexeme]['Linhas'].append(current_line)

    def get_symbols(self):
        return self.symbols