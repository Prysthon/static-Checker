# main.py

from lexer import Lexer
from symbol_table import SymbolTable
from relatorio import Relatorio
from utils import read_file, write_file
from header import header

def main():
    # file = input('Digite o nome do arquivo: ')
    file = 'meuTeste'
    source_code = read_file(file)

    lexer = Lexer(source_code)
    tokens = lexer.get_tokens()

    # Gerar relatório de análise léxica
    relatorio = Relatorio(tokens)
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
