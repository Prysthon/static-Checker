import re
from padroes import PADROES
from palavras import PALAVRAS

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code.upper()  # Normaliza para maiúsculas
        self.simbolos_adcionados = {}
        self.tokens_dados_p_relatorio = []
        self.current_line = 1
        self.fim_lex = 0
        self.index_relatorio = 0
        self.index_tabela = 0

    def formacao_lexeme(self, inicio_lex):
        lexeme = ''
        # Para fazer:
        #
        # identificação do lexeme (acho melhor sem usar regex, ou então podemos melhorar o regex) ->
        #
        # filtro de primeiro nivel, ou seja:
        # ignorar/remover os caracteres invalidos sem os considerar como delimitadores;
        # impor o limite de 30 caracteres por átomo, com os caracteres posteriores
        # sendo considerados inválidos (até que se encontre um delimitador)
        #
        # filtro de segundo nivel, ou seja:
        # utilizar os caracteres não relevantes (como espaços, quebra de linha e comentarios)
        # como delimitadores, e *remover construções não relevantes* (exemplo da string com \ no meio)
        #
        return lexeme

    def is_reservada(self, lexeme):
        if lexeme in PALAVRAS:
            return True
        return False

    def tratamento_reservada(self, lexeme, inicio_lex):
        # adciona palavra reservada na lista de dados
        self.tokens_dados_p_relatorio.append(
            (lexeme, "palavraReservada", self.index_relatorio, self.current_line)
        )

        self.index_relatorio += 1

        # atribui o ponteiro de inicio ao final do ultimo lexeme
        inicio_lex = self.fim_lex

        return ("palavraReservada", inicio_lex)

    def tratamento_construcoes(self, lexeme, inicio_lex, escopo):
        # Para fazer:
        # utilizar o escopo, se necessario, para reconhecer se o
        # lexeme é: variavel, nomFuncao ou nomPrograma,
        # e identificar o tipo do token (token_type)

        # adciona palavra reservada na lista de dados
        self.tokens_dados_p_relatorio.append(
            (lexeme, token_type, self.index_tabela, self.current_line)
        )
        self.index_relatorio += 1

        # adciona átomo formado no dicionario de simbolos
        self.tokens_indices[(lexeme, token_type)] = self.index_tabela
        self.index_tabela += 1

        # Para fazer:
        # adcionar o átomo formado na tabela de simbolos

        # atribui o ponteiro de inicio ao final do ultimo lexeme
        inicio_lex = self.fim_lex

        return (token_type, inicio_lex)

    def formar_atomo(self, inicio_lex, escopo, SymbolTable):
        lexeme = ""
        token_type = ""

        lexeme = self.formacao_lexeme(inicio_lex)

        if self.is_reservada(lexeme):
            token_type, inicio_lex = self.tratamento_reservada(lexeme, inicio_lex)
            return (token_type, inicio_lex)

        token_type, inicio_lex = self.tratamento_construcoes(lexeme, inicio_lex, escopo)
        
        if self.inicio_lex < len(self.source_code):
            if self.source_code[self.inicio_lex] == "\n":
                self.current_line += 1
            self.position += 1
        
        return (token_type, inicio_lex)

    # codigo antigo
    #
    #        match = None
    #
    #        self.inicio_lex = inicio_lex
    #        if escopo in {"CO5", "C06"}:
    #            self.escopo = escopo
    #
    #        for token_regex, token_type in PADROES:
    #            pattern = re.compile(token_regex)  # Compila regex
    #            match = pattern.match(self.source_code, self.position)
    #
    #            if match:
    #                lexeme = match.group(0)
    #
    #                # Determina o tipo de token baseado no contexto
    #                if token_type in {
    #                    "C05",
    #                    "C06",
    #                    "C07",
    #                }:  # Handle context-sensitive case for identifiers
    #                    token_type = self.escopo
    #
    #                # Verifica se o lexeme e o tipo já existem no dicionário de índices
    #                if (lexeme, token_type) not in self.tokens_indices:
    #                    self.tokens_indices[(lexeme, token_type)] = index
    #                    index += 1
    #
    #                # Recupera o índice existente
    #                lexeme_index = self.tokens_indices[(lexeme, token_type)]
    #                self.tokens_dados_p_relatorio.append(
    #                    (lexeme, token_type, lexeme_index, self.current_line)
    #                )
    #                self.position = match.end(0)
    #                self.escopo = "C07"
    #                return (token_type, self.position)
    #
    #        if self.position < len(self.source_code):
    #            if self.source_code[self.position] == "\n":
    #                self.current_line += 1
    #            self.position += 1
    #
    #        return (self.escopo, self.position)

    def get_tokens_dados_p_relatorio(self):
        return self.tokens_dados_p_relatorio
