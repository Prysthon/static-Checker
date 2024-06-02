# symbol_table.py

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.index = 0

    def add_symbol(self, lexeme, symbol_type):
        if lexeme not in self.symbols:
            self.symbols[lexeme] = {
                'index': self.index,
                'type': symbol_type,
                'count': 1,
                'lines': []
            }
            self.index += 1
        else:
            self.symbols[lexeme]['count'] += 1

    def add_line(self, lexeme, line):
        if lexeme in self.symbols:
            if len(self.symbols[lexeme]['lines']) < 5:
                self.symbols[lexeme]['lines'].append(line)

    def get_symbol(self, lexeme):
        return self.symbols.get(lexeme, None)

    def get_symbols(self):
        return self.symbols