from header import header
from tabulate import tabulate
import os
from collections import defaultdict

class Relatorio:
    def __init__(self, tokens, nome_arquivo):
        self.tokens = tokens
        self.nome_arquivo = nome_arquivo

    def path(self, nome_arquivo, extensao):
         # Extrai o nome do arquivo e o diretório (se fornecido)
        diretorio_arquivo = os.path.dirname(nome_arquivo)
        nome_arquivo_sem_extensao = os.path.splitext(os.path.basename(nome_arquivo))[0]

        # Se não houver diretório, usa o diretório da main.py
        if not diretorio_arquivo:
            diretorio_arquivo = os.path.dirname(os.path.abspath(__file__))

        # Caminho completo do arquivo com a extensão especificada
        return os.path.join(diretorio_arquivo, f"{nome_arquivo_sem_extensao}.{extensao}")

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

        TipoSimb = {
            "C01": "STR",
            "C02": "CHC",
            "C03": "INT",
            "C04": "PFO",
            "C05": "STR",
            "C06": "STR",
            "C07": "STR",
            "VOID": "VOI",
        }

        for lexeme, codigo, qtd_antes_truncar, indice, linha in self.tokens:
            if codigo.startswith('C'):
                tabela_simbolos[indice]['Lexeme'] = lexeme
                tabela_simbolos[indice]['Codigo'] = codigo
                tabela_simbolos[indice]['QtdCharAntesTrunc'] = qtd_antes_truncar
                tabela_simbolos[indice]['QtdCharDepoisTrunc'] = len(lexeme)
                tabela_simbolos[indice]['TipoSimb'] = TipoSimb.get(codigo, '-')
                if (TipoSimb.get(codigo, '-') == 'STR') and (len(lexeme) == 1):
                    tabela_simbolos[indice]['TipoSimb'] = "CHC"
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