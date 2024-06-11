# main.py

from lexer import Lexer
from symbol_table import SymbolTable
from relatorio import Relatorio
from utils import read_file, write_file, determinar_escopo
from header import header


def main():
    # 1º: abrir o arquivo e salvar o endereço

    # file = input('Digite o nome do arquivo: ')
    file = "meuTeste"
    source_code = read_file(file)

    # 2º: inicializar variaveis e objetos
    symbol_table = SymbolTable()
    lexer = Lexer(source_code)

    inicio_lex = 0
    tokens_dados_p_relatorio = []
    escopo = ""
    previous_token = ""

    # 3º: loop analisador lexico
    while inicio_lex < len(source_code):
        escopo = determinar_escopo(previous_token)
        previous_token, inicio_lex = lexer.formar_atomo(inicio_lex, escopo, symbol_table)

    tokens_dados_p_relatorio = lexer.get_tokens_dados()

    # 4º: gerar relatorios .LEX e .TAB
    relatorio = Relatorio(tokens_dados_p_relatorio)
    relatorio.gerar_lex(file)


#     symbol_table = SymbolTable()

#     for token in tokens:
#         lexeme, token_type = token
#         if token_type == 'IDENTIFIER':
#             symbol_table.add_symbol(lexeme, 'IDENTIFIER')
#         # Adicione outros tipos de tokens à tabela de símbolos conforme necessário
#     # Gerar relatório da tabela de símbolos
#     tab_content = f'''{header}
# TABELA DE SÍMBOLOS. Texto fonte analisado: {file}.241
# '''

#     symbols = symbol_table.get_symbols()
#     for lexeme, info in symbols.items():
#         tab_content += f'{lexeme}: {info}\n'
#     write_file(f'{file}.TAB', tab_content)

if __name__ == "__main__":
    main()
