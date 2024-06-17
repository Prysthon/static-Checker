# lexer.py

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

    def formacao_lexeme(self, inicio_lex):
        self.inicio_lex = inicio_lex
        automato = AutomatoLex(self.source_code)
        lexeme = ""
        token_type = ""
        qtd_antes_truncar = 0

        automato.add_estados_base()
        self.filtro()

        lexeme, token_type, self.inicio_lex, self.source_code, qtd_antes_truncar = automato.run(self.source_code, self.inicio_lex)
        while lexeme == 'ERRO' and token_type == 'ERRO':
            lexeme, token_type, self.inicio_lex, self.source_code, qtd_antes_truncar = automato.run(self.source_code, self.inicio_lex)

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
                    while self.source_code[fim] != "\n" and fim < len(self.source_code):
                        if fim == len(self.source_code) - 1:
                            break
                        fim += 1
                    self.source_code = remover_invalidos(self.source_code, inicio, fim)
                # comentários de bloco
                elif self.source_code[posicao + 1] == "*":
                    inicio = posicao
                    fim = posicao
                    while (
                        self.source_code[fim] != "*"
                        and self.source_code[fim + 1] != "/"
                        and fim < len(self.source_code)
                    ):
                        if fim == len(self.source_code) - 1:
                            break
                        fim += 1
                    remover_invalidos(self.source_code, inicio, fim + 1)
            # remoção de caracteres não permitidos
            if self.source_code[posicao] not in ALFABETO:
                self.source_code = remover_invalidos(self.source_code, posicao, posicao)
            posicao += 1

    def is_reservada(self, lexeme):
        if lexeme in PALAVRAS:
            return True
        return False

    def tratamento_reservada(self, lexeme, token_type):
        # adciona palavra reservada na lista de dados
        # index (-1) para sinalizar que é uma palavra reservada
        self.tokens_dados_p_relatorio.append(
            (
                lexeme,
                token_type,
                (-1),
                self.current_line
            )
        )

    def tratamento_construcoes(
        self, lexeme, token_type, escopo, symbol_table, qtd_antes_truncar
    ):
        # caso especial da variavel com '_'
        # if token_type == '000':
        #   self.especial = 1

        # verifica o escopo

        # if self.especial == 0
        if token_type in ("C05", "C06", "C07"):
            token_type = escopo
        # else self.especial = 0

        # adciona átomo formado na tabela de símbolos
        symbol_table.add(lexeme, token_type, qtd_antes_truncar, self.current_line)

        # adciona construção na lista de dados
        self.tokens_dados_p_relatorio.append(
            (
                lexeme,
                token_type,
                symbol_table.getIndex(lexeme, token_type),
                self.current_line,
            )
        )

        return token_type

    def formar_atomo(self, inicio_lex, escopo, symbol_table):
        self.inicio_lex = inicio_lex
        lexeme = ""
        token_type = ""
        qtd_antes_truncar = 0

        while self.inicio_lex in (" ", "\n", "\t", "\r"):
            if self.inicio_lex == "\n":
                self.current_line += 1
            self.inicio_lex += 1

        if self.inicio_lex == "EOF":
            return (token_type, self.inicio_lex)

        lexeme, token_type, qtd_antes_truncar = self.formacao_lexeme(inicio_lex)

        if self.is_reservada(lexeme):
            self.tratamento_reservada(lexeme, token_type)
            return (token_type, self.inicio_lex)
        else:
            token_type = self.tratamento_construcoes(
                lexeme, token_type, escopo, symbol_table, qtd_antes_truncar
            )
            return (token_type, self.inicio_lex)

    def get_tokens_dados_p_relatorio(self):
        return self.tokens_dados_p_relatorio
