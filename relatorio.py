from header import header
from tabulate import tabulate
import os
from collections import defaultdict

class Relatorio:
    def __init__(self, tokens, nome_arquivo):
        self.tokens = tokens
        self.nome_arquivo = nome_arquivo

    def path(self, nome_arquivo, extensao):
        # Diretório da main.py
        diretorio_main = os.path.dirname(os.path.abspath(__file__))
        # Extrai o nome do arquivo sem o diretório e extensão
        nome_arquivo = os.path.splitext(os.path.basename(nome_arquivo))[0]
        # Caminho completo do arquivo com a extensão especificada (junto da main.py)
        return os.path.join(diretorio_main, f"{nome_arquivo}.{extensao}")

    def gerar_lex(self):
        tabela = tabulate(
            self.tokens,
            headers=["Lexeme", "Código", "índiceTabSimb", "Linha"],
            tablefmt="grid",
        )

        caminho_arquivo = self.path(self.nome_arquivo, "LEX")
        with open(caminho_arquivo, "w") as file:
            file.write(header)
            file.write(
                f"RELATÓRIO DA ANÁLISE LÉXICA. Texto fonte analisado: {self.nome_arquivo}.241\n"
            )
            file.write(tabela)

    def gerar_tab(self):
        # Processar tokens para formar a tabela
        tabela_simbolos = defaultdict(lambda: {
            'Codigo': 'C07', 
            'QtdCharAntesTrunc': 0, 
            'QtdCharDepoisTrunc': 0, 
            'TipoSimb': '-', 
            'Linhas': set()
        })

        for lexeme, codigo, indice, linha in self.tokens:
            tabela_simbolos[indice]['Lexeme'] = lexeme
            tabela_simbolos[indice]['Codigo'] = codigo
            tabela_simbolos[indice]['QtdCharDepoisTrunc'] = len(lexeme)
            tabela_simbolos[indice]['Linhas'].add(linha)

        linhas_relatorio = []
        for indice, dados in tabela_simbolos.items():
            linhas_relatorio.append(f"Entrada: {indice}, Codigo: {dados['Codigo']}, Lexeme: {dados['Lexeme']},\nQtdCharAntesTrunc: {dados['QtdCharAntesTrunc']}, QtdCharDepoisTrunc: {dados['QtdCharDepoisTrunc']},\nTipoSimb: {dados['TipoSimb']}, Linhas: {sorted(dados['Linhas'])}.")
            linhas_relatorio.append("-" * 80)

        caminho_arquivo = self.path(self.nome_arquivo, "TAB")
        with open(caminho_arquivo, "w") as file:
            file.write(header)
            file.write(
                f"RELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: {self.nome_arquivo}.241\n"
            )
            file.write("\n".join(linhas_relatorio))