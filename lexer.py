from palavras import PALAVRAS
from alfabeto import ALFABETO
from utils import uppercase_menos_sequencias
from utils import remover_invalidos
from automato import AutomatoLex

class Lexer:
    def __init__(self, source_code):
        self.source_code = uppercase_menos_sequencias(source_code)
        self.tokens_dados_p_relatorio = []
        self.current_line = 1
        self.inicio_lex = 0
        self.especial = 0
        self.automato = AutomatoLex(self.source_code)
        self.lexeme_ids = {}  # Dicionário para armazenar IDs dos lexemes
        self.next_id = 1      # Inicializa o próximo ID
        

    def formacao_lexeme(self, inicio_lex, escopo):
        self.inicio_lex = inicio_lex
        lexeme = ""
        token_type = ""
        qtd_antes_truncar = 0

        lexeme, token_type, self.inicio_lex, self.source_code, qtd_antes_truncar = (
            self.automato.run(self.source_code, self.inicio_lex, escopo)
        )
        while lexeme == "erro" and token_type == "erro":
            while self.source_code[self.inicio_lex] in (" ", "\n", "\t", "\r"):
                if self.inicio_lex >= len(self.source_code) - 1:
                    return (token_type, self.inicio_lex, self.source_code)
                if self.source_code[self.inicio_lex] in ("\n", "\r"):
                    self.current_line += 1
                self.inicio_lex += 1

            lexeme, token_type, self.inicio_lex, self.source_code, qtd_antes_truncar = (
                self.automato.run(self.source_code, self.inicio_lex, escopo)
            )

        return (lexeme, token_type, qtd_antes_truncar)

    def filtro(self):
        posicao = 0
        inicio = 0
        fim = 0

        while posicao < len(self.source_code):
            # remoção de comentários
            if self.source_code[posicao] == "/":
                # comentários de linha
                if self.source_code[posicao + 1] == "/":
                    inicio = posicao
                    fim = posicao
                    while fim < len(self.source_code) - 1:
                        if self.source_code[fim] == "\n" or self.source_code[fim] == "\r":
                            break
                        fim += 1
                    self.source_code = remover_invalidos(self.source_code, inicio, fim)
                # comentários de bloco
                elif self.source_code[posicao + 1] == "*":
                    inicio = posicao
                    fim = posicao
                    while fim < len(self.source_code) - 1:
                        if self.source_code[fim] == "*" and self.source_code[fim + 1] == "/":
                            break
                        fim += 1
                    self.source_code = remover_invalidos(
                        self.source_code, inicio, fim + 1
                    )
            # remoção de caracteres não permitidos
            if self.source_code[posicao] not in ALFABETO:
                self.source_code = remover_invalidos(self.source_code, posicao, posicao)
                posicao -= 1
            posicao += 1
        self.source_code = self.source_code + "\n"
        return self.source_code

    def is_reservada(self, lexeme):
        for palavra, _ in PALAVRAS:
            if lexeme == palavra:
                return True
        return False

    def tratamento_reservada(self, lexeme, token_type):
        # Adiciona palavra reservada na lista de dados
        # Index (-1) para sinalizar que é uma palavra reservada
        lexeme_id = self.get_lexeme_id(lexeme)
        self.tokens_dados_p_relatorio.append(
            (lexeme, token_type, lexeme_id, self.current_line)
        )

    def get_lexeme_id(self, lexeme):
        if lexeme not in self.lexeme_ids:
            self.lexeme_ids[lexeme] = self.next_id
            self.next_id += 1
        return self.lexeme_ids[lexeme]

    def tratamento_construcoes(
        self, lexeme, token_type, symbol_table, qtd_antes_truncar
    ):
        # Adiciona átomo formado na tabela de símbolos
        # symbol_table.add(lexeme, token_type, qtd_antes_truncar, self.current_line)

        # Adiciona construção na lista de dados
        lexeme_id = self.get_lexeme_id(lexeme)
        self.tokens_dados_p_relatorio.append(
            (
                lexeme,
                token_type,
                lexeme_id,
                self.current_line,
            )
        )

        return token_type

    def formar_atomo(self, inicio_lex, escopo, symbol_table):
        self.inicio_lex = inicio_lex
        lexeme = ""
        token_type = ""
        qtd_antes_truncar = 0

        while self.source_code[self.inicio_lex] in (" ", "\n", "\t", "\r"):
            if self.inicio_lex >= len(self.source_code) - 1:
                return (token_type, self.inicio_lex, self.source_code)
            if self.source_code[self.inicio_lex] in ("\n", "\r"):
                self.current_line += 1
            self.inicio_lex += 1

        lexeme, token_type, qtd_antes_truncar = self.formacao_lexeme(
            self.inicio_lex, escopo
        )

        if self.is_reservada(lexeme):
            self.tratamento_reservada(lexeme, token_type)
            return (token_type, self.inicio_lex, self.source_code)
        else:
            token_type = self.tratamento_construcoes(
                lexeme, token_type, symbol_table, qtd_antes_truncar
            )
            return (token_type, self.inicio_lex, self.source_code)

    def get_tokens_dados_p_relatorio(self):
        return self.tokens_dados_p_relatorio
