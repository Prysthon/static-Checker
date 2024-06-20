from header import header
from tabulate import tabulate
import os

class Relatorio:
    def __init__(self, tokens):
        self.tokens = tokens

    def gerar_lex(self, nome_arquivo):
        tabela = tabulate(
            self.tokens,
            headers=["Lexeme", "Código", "índiceTabSimb", "Linha"],
            tablefmt="grid",
        )

        # Diretório da main.py
        diretorio_main = os.path.dirname(os.path.abspath(__file__))

        # Extrai o nome do arquivo sem o diretório e extensão
        nome_arquivo = os.path.splitext(os.path.basename(nome_arquivo))[0]
        
        # Caminho completo do arquivo .LEX (junto da main.py)
        caminho_arquivo = os.path.join(diretorio_main, f"{nome_arquivo}.LEX")

        with open(caminho_arquivo, "w") as file:
            file.write(header)
            file.write(
                f"RELATÓRIO DA ANÁLISE LÉXICA. Texto fonte analisado: {nome_arquivo}.241\n"
            )
            file.write(tabela)

    # def gerar_tab(self, nome_arquivo):
    #     simbolos = {}
    #     for token in self.tokens:
    #         if token[0] == 'IDENTIFIER':
    #             if token[1] not in simbolos:
    #                 simbolos[token[1]] = {'tipo': token[0], 'linhas': [token[2]]}
    #             else:
    #                 simbolos[token[1]]['linhas'].append(token[2])

    #     with open(nome_arquivo, 'w') as file:
    #         file.write("Tabela de Símbolos\n")
    #         file.write(f"Código da Equipe: {self.equipe_info['codigo']}\n")
    #         for simbolo, info in simbolos.items():
    #             file.write(f"Símbolo: {simbolo}, Tipo: {info['tipo']}, Linhas: {info['linhas'][:5]}\n")
