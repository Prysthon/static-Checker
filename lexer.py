import re
from padroes import PADROES
from palavras import PALAVRAS
from alfabeto import ALFABETO

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code.upper()  # Normaliza para maiúsculas
        self.simbolos_adcionados = {}
        self.tokens_dados_p_relatorio = []
        self.current_line = 1
        self.fim_lex = 0
        self.index_relatorio = 0

    # Para fazer em formacao_lexeme:
    #
    # identificação do lexeme (acho melhor sem usar regex, ou então podemos melhorar o regex) ->
    #
    # filtro de segundo nivel, ou seja:
    # -> utilizar os caracteres não relevantes (como espaços e quebras de linha) como delimitadores
    # -> remover construções não relevantes (exemplo da string com \ no meio) (?)
    # -> impor o limite de 30 caracteres por átomo, com os caracteres posteriores
    #    sendo considerados inválidos (até que se encontre um delimitador) 
    #
    def formacao_lexeme(self, inicio_lex):
        lexeme = ''
        token_type = ''

        self.pre_lexico()

        return (lexeme, token_type)
    
    def remover_invalidos(self, inicio, fim):
        str = self.source_code[:inicio] + self.source_code[(fim + 1):]
        return str


    def pre_lexico(self):
        posicao = 0
        inicio = 0
        fim = 0

        while posicao < len(self.source_code):
            # remoção de comentários
            if self.source_code[posicao] == '/':
                # comentários de linha
                if self.source_code[posicao + 1] == '/':
                    inicio = posicao
                    fim = posicao
                    while self.source_code[fim] != '\n' and fim < len(self.source_code):
                        fim += 1
                    self.source_code = self.remover_invalidos(inicio, (fim - 1))
                # comentários de bloco
                elif self.source_code[posicao + 1] == '*':
                    inicio = posicao
                    fim = posicao
                    while self.source_code[fim] != '*' and self.source_code[fim + 1] != '/' and fim < len(self.source_code):
                        fim +=1
                    self.remover_invalidos(inicio, (fim - 1))
            # remoção de caracteres não permitidos
            if self.source_code[posicao] not in ALFABETO:
                self.source_code = self.remover_invalidos(posicao, posicao)
            posicao += 1

    def is_reservada(self, lexeme):
        if lexeme in PALAVRAS:
            return True
        return False

    def tratamento_reservada(self, lexeme, inicio_lex, token_type):
        # adciona palavra reservada na lista de dados
        # index (-1) para sinalizar que é palavra reservada
        self.tokens_dados_p_relatorio.append((lexeme, token_type, (-1), self.current_line))
        self.index_relatorio += 1

        # atribui o ponteiro de inicio ao final do ultimo lexeme
        inicio_lex = self.fim_lex

        return inicio_lex

    def tratamento_construcoes(self, lexeme, inicio_lex, token_type, escopo, symbol_table):
        # verifica o escopo
        if token_type in ('C05', 'C06', 'C07'):
            token_type = escopo

        # adciona átomo formado no dicionario de simbolos, se não já estiver
        symbol_table.add(lexeme, token_type)
        
        # adciona palavra reservada na lista de dados
        self.tokens_dados_p_relatorio.append(
            (lexeme, token_type, symbol_table.getIndex(lexeme, token_type), self.current_line)
        )
        self.index_relatorio += 1

        # atribui o ponteiro de inicio ao final do ultimo lexeme
        inicio_lex = self.fim_lex

        return (token_type, inicio_lex)

    def verificar_linha(self): # isso funciona??
        if self.inicio_lex < len(self.source_code):
            if self.source_code[self.inicio_lex] == "\n":
                self.current_line += 1
            self.position += 1

    def formar_atomo(self, inicio_lex, escopo, symbol_table):
        lexeme = ""
        token_type = ""

        lexeme, token_type = self.formacao_lexeme(inicio_lex)

        if self.is_reservada(lexeme):
            inicio_lex = self.tratamento_reservada(lexeme, inicio_lex, token_type)
            self.verificar_linha()
            return (token_type, inicio_lex)
        else:
            token_type, inicio_lex = self.tratamento_construcoes(lexeme, inicio_lex, token_type, escopo, symbol_table)
            self.verificar_linha()
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
