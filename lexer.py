import re

# Definição das regex para identificar tokens na linguagem Perpertuum2024-1
TOKENS = [
    (r'\bcadeia\b', 'A01'),  # cadeia
    (r'\bcaracter\b', 'A02'),  # caracter
    (r'\bdeclaracoes\b', 'A03'),
    (r'\benquanto\b', 'A04'),
    (r'\bfalse\b', 'A05'),
    (r'\bfimDeclaracoes\b', 'A06'),
    (r'\bfimEnquanto\b', 'A07'),
    (r'\bfimFunc\b', 'A08'),
    (r'\bfimFuncoes\b', 'A09'),
    (r'\bfimPrograma\b', 'A10'),
    (r'\bfimSe\b', 'A11'),
    (r'\bfuncoes\b', 'A12'),
    (r'\bimprime\b', 'A13'),
    (r'\binteiro\b', 'A14'),
    (r'\blogico\b', 'A15'),
    (r'\bpausa\b', 'A16'),
    (r'\bprograma\b', 'A17'),
    (r'\breal\b', 'A18'),
    (r'\bretorna\b', 'A19'),
    (r'\bse\b', 'A20'),
    (r'\bsenao\b', 'A21'),
    (r'\btipoFunc\b', 'A22'),
    (r'\btipoParam\b', 'A23'),
    (r'\btipoVar\b', 'A24'),
    (r'\btrue\b', 'A25'),
    (r'\bvazio\b', 'A26'),
    (r'%', 'B01'),
    (r'\(', 'B02'),
    (r'\)', 'B03'),
    (r',', 'B04'),
    (r':', 'B05'),
    (r':=', 'B06'),
    (r';', 'B07'),
    (r'\?', 'B08'),
    (r'\[', 'B09'),
    (r'\]', 'B10'),
    (r'\{', 'B11'),
    (r'\}', 'B12'),
    (r'\*', 'B14'),
    (r'\+', 'B16'),
    (r'!=', 'B17'),
    (r'#', 'B17'),
    (r'<', 'B18'),
    (r'<=', 'B19'),
    (r'=', 'B20'),
    (r'>', 'B21'),
    (r'>=', 'B22'),
    (r'/', 'B15'),
    (r'"[^"\\]*(\\.[^"\\]*)*"', 'C01'),
    (r'"[a-zA-Z]"', 'C02'),
    (r'\b\d+\b', 'C03'),
    (r'\b\d+(\.\d+)?(e[+-]?\d+)?\b', 'C04'),
    (r'\b[a-zA-Z][a-zA-Z0-9]*\b', 'C05'),
    (r'\b[a-zA-Z][a-zA-Z0-9]*\b', 'C06'),
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'C07'),
]

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_line = 1
        self.tokens = []
        self.lexeme_indices = {}
        self.tokenize()

    def tokenize(self):
        index = 0
        while self.position < len(self.source_code):
            match = None
            for token_regex, token_type in TOKENS:
                pattern = re.compile(token_regex)
                match = pattern.match(self.source_code, self.position)
                if match:
                    lexeme = match.group(0)
                    if token_type:
                        # Verifica se o lexeme e o tipo já existem no dicionário de índices
                        if (lexeme, token_type) not in self.lexeme_indices:
                            self.lexeme_indices[(lexeme, token_type)] = index
                            index += 1
                        # Recupera o índice existente
                        lexeme_index = self.lexeme_indices[(lexeme, token_type)]
                        self.tokens.append((lexeme, token_type, lexeme_index, self.current_line))
                    self.position = match.end(0)
                    break
            if not match:
                if self.source_code[self.position] == '\n':
                    self.current_line += 1
                self.position += 1

    def get_tokens(self):
        return self.tokens