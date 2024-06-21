# main.py
from lexer import Lexer
from symbol_table import SymbolTable
from relatorio import Relatorio
from utils import read_file, analise_escopo


def main():
    # 1º: abrir o arquivo e salvar o endereço
    file = input("Digite o nome do arquivo: ")
    # file = "meuTeste"
    source_code = read_file(file)

    # 2º: inicializar objetos e variaveis
    symbol_table = SymbolTable()
    lexer = Lexer(source_code)
    source_code = lexer.filtro()

    inicio_lex = 0
    tokens_dados_p_relatorio = []
    escopo = "C07"  # escopo padrão: variavel
    previous_token = ""
    escopo_ja_usado = True

    # 3º: loop analisador lexico
    while inicio_lex < len(source_code) - 1:
        escopo, escopo_ja_usado = analise_escopo(previous_token, escopo_ja_usado)
        previous_token, inicio_lex, source_code = lexer.formar_atomo(
            inicio_lex, escopo, symbol_table
        )

    # 4º: gerar relatorios .LEX e .TAB
    tokens_dados_p_relatorio = lexer.get_tokens_dados_p_relatorio()
    relatorio = Relatorio(tokens_dados_p_relatorio, file)
    relatorio.gerar_lex()
    relatorio.gerar_tab()


if __name__ == "__main__":
    main()
