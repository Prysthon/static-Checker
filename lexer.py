import re

# Definição das regex para identificar tokens na linguagem Perpertuum2024-1
TOKENS = [
    (r'\bcadeia\b', 'A01'),  # cadeia
    (r'\bcaracter\b', 'A02'),  # caracter
    (r'\bdeclaracoes\b', 'A03'),  # declaracoes
    (r'\benquanto\b', 'A04'),  # enquanto
    (r'\bfalse\b', 'A05'),  # false
    (r'\bfimDeclaracoes\b', 'A06'),  # fimDeclaracoes
    (r'\bfimEnquanto\b', 'A07'),  # fimEnquanto
    (r'\bfimFunc\b', 'A08'),  # fimFunc
    (r'\bfimFuncoes\b', 'A09'),  # fimFuncoes
    (r'\bfimPrograma\b', 'A10'),  # fimPrograma
    (r'\bfimSe\b', 'A11'),  # fimSe
    (r'\bfuncoes\b', 'A12'),  # funcoes
    (r'\bimprime\b', 'A13'),  # imprime
    (r'\binteiro\b', 'A14'),  # inteiro
    (r'\blogico\b', 'A15'),  # logico
    (r'\bpausa\b', 'A16'),  # pausa
    (r'\bprograma\b', 'A17'),  # programa
    (r'\breal\b', 'A18'),  # real
    (r'\bretorna\b', 'A19'),  # retorna
    (r'\bse\b', 'A20'),  # se
    (r'\bsenao\b', 'A21'),  # senao
    (r'\btipoFunc\b', 'A22'),  # tipoFunc
    (r'\btipoParam\b', 'A23'),  # tipoParam
    (r'\btipoVar\b', 'A24'),  # tipoVar
    (r'\btrue\b', 'A25'),  # true
    (r'\bvazio\b', 'A26'),  # vazio
    (r'%', 'B01'),  # símbolo %
    (r'\(', 'B02'),  # símbolo (
    (r'\)', 'B03'),  # símbolo )
    (r',', 'B04'),  # símbolo ,
    (r':', 'B05'),  # símbolo :
    (r':=', 'B06'),  # símbolo :=
    (r';', 'B07'),  # símbolo ;
    (r'\?', 'B08'),  # símbolo ?
    (r'\[', 'B09'),  # símbolo [
    (r'\]', 'B10'),  # símbolo ]
    (r'\{', 'B11'),  # símbolo {
    (r'\}', 'B12'),  # símbolo }
    (r'\*', 'B14'),  # símbolo *
    (r'\+', 'B16'),  # símbolo +
    (r'!=', 'B17'),  # símbolo !=
    (r'#', 'B17'),  # símbolo #
    (r'<', 'B18'),  # símbolo <
    (r'<=', 'B19'),  # símbolo <=
    (r'=', 'B20'),  # símbolo =
    (r'>', 'B21'),  # símbolo >
    (r'>=', 'B22'),  # símbolo >=
    (r'/', 'B15'),  # símbolo /
    (r'"[^"\\]*(\\.[^"\\]*)*"', 'C01'),  # consCadeia
    (r'"[a-zA-Z]"', 'C02'),  # consCaracter
    (r'\b\d+\b', 'C03'),  # consInteiro
    (r'\b\d+(\.\d+)?(e[+-]?\d+)?\b', 'C04'),  # consReal
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', 'C07'),  # variavel (default)
]

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code.lower()  # Normaliza para minúsculas
        self.position = 0
        self.current_line = 1
        self.tokens = []
        self.lexeme_indices = {}
        self.tokenize()

    def determine_token_type(self, lexeme, previous_token_type):
        if previous_token_type in {'tipoFunc', 'tipoVar', 'inteiro', 'real', 'logico', 'caracter', 'vazio'}:
            return 'C05'  # nomFuncao
        return 'C07'  # variavel

    def tokenize(self):
        index = 0
        previous_token_type = None
        while self.position < len(self.source_code):
            match = None
            for token_regex, token_type in TOKENS:
                pattern = re.compile(token_regex, re.IGNORECASE)  # Compila regex como case-insensitive
                match = pattern.match(self.source_code, self.position)
                if match:
                    lexeme = match.group(0)
                    if token_type == 'C07':  # Handle context-sensitive case for identifiers
                        token_type = self.determine_token_type(lexeme, previous_token_type)
                    # Verifica se o lexeme e o tipo já existem no dicionário de índices
                    if (lexeme, token_type) not in self.lexeme_indices:
                        self.lexeme_indices[(lexeme, token_type)] = index
                        index += 1
                    # Recupera o índice existente
                    lexeme_index = self.lexeme_indices[(lexeme, token_type)]
                    self.tokens.append((lexeme, token_type, lexeme_index, self.current_line))
                    previous_token_type = token_type
                    self.position = match.end(0)
                    break
            if not match:
                if self.source_code[self.position] == '\n':
                    self.current_line += 1
                self.position += 1

    def get_tokens(self):
        return self.tokens

