# lexer.py

import re

# Definição das regex para identificar tokens na linguagem Perpertuum2024-1
TOKENS = [
    (r'\bprograma\b', 'PROGRAMA'),
    (r'\bdeclaracoes\b', 'DECLARACOES'),
    (r'\bfimDeclaracoes\b', 'FIM_DECLARACOES'),
    (r'\bfuncoes\b', 'FUNCOES'),
    (r'\bfimFuncoes\b', 'FIM_FUNCOES'),
    (r'\bfimPrograma\b', 'FIM_PROGRAMA'),
    (r'\bvariavel\b', 'VARIAVEL'),
    (r'\bconsInteiro\b', 'CONS_INTEIRO'),
    (r'\bconsReal\b', 'CONS_REAL'),
    (r'\bconsCadeia\b', 'CONS_CADEIA'),
    (r'\bconsCaracter\b', 'CONS_CARACTER'),
    (r'\bnomFuncao\b', 'NOM_FUNCAO'),
    (r'\bnomPrograma\b', 'NOM_PROGRAMA'),
    (r'[0-9]+', 'INTEGER'),
    (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
    (r'\s+', None),  # Espaços em branco são ignorados
    (r'.', 'UNKNOWN'),
]

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        while self.position < len(self.source_code):
            match = None
            for token_regex, token_type in TOKENS:
                pattern = re.compile(token_regex)
                match = pattern.match(self.source_code, self.position)
                if match:
                    lexeme = match.group(0)
                    if token_type:
                        self.tokens.append((lexeme, token_type))
                    self.position = match.end(0)
                    break
            if not match:
                raise SyntaxError(f'Unexpected character: {self.source_code[self.position]}')

    def get_tokens(self):
        return self.tokens
