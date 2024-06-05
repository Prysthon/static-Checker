import re
from tokens import TOKENS

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code.upper()  # Normaliza para maiúsculas
        self.tokens_indices = {}
        self.tokens_dados = []
        self.current_line = 1
        self.position = 0
        self.escopo = ''

    def tokenize(self, position, escopo, SymbolTable, WordsTable):
        index = 0
        match = None
        self.position = position
        if escopo in {'CO5', 'C06'}:
            self.escopo = escopo

        for token_regex, token_type in TOKENS:
            pattern = re.compile(token_regex)  # Compila regex
            match = pattern.match(self.source_code, self.position)

            if match:
                lexeme = match.group(0)

                # Determina o tipo de token baseado no contexto
                if token_type in {'C05', 'C06', 'C07'}:  # Handle context-sensitive case for identifiers
                    token_type = self.escopo

                # Verifica se o lexeme e o tipo já existem no dicionário de índices
                if (lexeme, token_type) not in self.tokens_indices:
                    self.tokens_indices[(lexeme, token_type)] = index
                    index += 1

                # Recupera o índice existente
                lexeme_index = self.tokens_indices[(lexeme, token_type)]
                self.tokens_dados.append((lexeme, token_type, lexeme_index, self.current_line))
                self.position = match.end(0)
                self.escopo = 'C07'
                return (token_type, self.position)

        if self.position < len(self.source_code):
            if self.source_code[self.position] == '\n':
                self.current_line += 1
            self.position += 1
    
        return (self.escopo, self.position)

    def get_tokens_dados(self):
        return self.tokens_dados
