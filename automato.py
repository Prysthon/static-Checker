# automato.py
from alfabeto import ALFABETO
from alfabeto import ALFABETO_STRING
from utils import remover_invalidos
from utils import get_codigo


class AutomatoLex:

    def __init__(self, source_code):
        # valores padrão
        self.estado_inicial = "Q0"
        self.funcoes = {}
        self.estados_finais = []
        # valores resetados a cada vez que o automato rodar
        self.source_code = source_code
        self.inicio_lex = 0
        self.fim_lex = 0
        self.prox_char = 0
        self.tamanho = 0
        self.posicao_limite = 0
        self.is_aceitacao = False
        # valores para serem retornardos
        self.lexeme = ""
        self.token_type = ""
        self.qtd_antes_truncar = 0
        # função de inicialização
        self.add_estados_base()

    def reset_automato(self, source_code, inicio_lex):
        self.source_code = source_code
        self.inicio_lex = inicio_lex
        self.fim_lex = inicio_lex
        self.prox_char = inicio_lex
        self.tamanho = 0
        self.posicao_limite = 0
        self.is_aceitacao = False
        self.lexeme = ""
        self.token_type = ""
        self.qtd_antes_truncar = 0

    def add_estado(self, nome, funcao, is_estado_final=0):
        nome = nome.upper()
        if funcao != None:
            self.funcoes[nome] = funcao
        if is_estado_final:
            self.estados_finais.append(nome)

    def delimitar(self, inicio_lex, fim_lex):
        return self.source_code[inicio_lex : fim_lex + 1]

    def run(self, source_code, inicio_lex, escopo):
        self.reset_automato(source_code, inicio_lex)

        novo_estado = self.estado_inicial
        funcao = self.funcoes[self.estado_inicial]

        while True:
            velho_estado = novo_estado  # velho_estado tem que ser salvo para caso de transição não prevista
            if velho_estado == "Q0":
                novo_estado = funcao(self.source_code[self.prox_char], escopo)
            else:
                novo_estado = funcao(self.source_code[self.prox_char])
            self.prox_char += 1
            self.tamanho += 1

            if self.tamanho == 30:
                self.posicao_limite = self.prox_char - 1

            # primeiro caso de conclusão, transição não prevista
            if novo_estado == "erro":
                # transição não prevista, átomo deve ser delimitado na posição anterior
                self.fim_lex = self.prox_char - 2
                self.tamanho -= 1

                if velho_estado in self.estados_finais:
                    self.is_aceitacao = True
                else:
                    self.is_aceitacao = False

                if self.tamanho > 30:
                    self.lexeme = self.delimitar(self.inicio_lex, self.posicao_limite)
                else:
                    self.lexeme = self.delimitar(self.inicio_lex, self.fim_lex)

                self.token_type = self.get_token_type(velho_estado, self.lexeme, escopo)

                self.qtd_antes_truncar = self.fim_lex - self.inicio_lex + 1

                # tamanho máximo permitido para átomos é 30
                if self.tamanho > 30:
                    self.truncar()

                # testar para construção não relevante
                if self.is_relevante() == False:
                    return (
                        "erro",
                        "erro",
                        self.inicio_lex,
                        self.source_code,
                        self.qtd_antes_truncar,
                    )

                return (
                    self.lexeme,
                    self.token_type,
                    self.fim_lex + 1,
                    self.source_code,
                    self.qtd_antes_truncar,
                )

            # segundo caso de conclusão, estado final sem mais transições, delimitação ocorre na posição atual
            if novo_estado in self.estados_finais:
                if novo_estado not in self.funcoes:

                    if novo_estado in self.estados_finais:
                        self.is_aceitacao = True
                    else:
                        self.is_aceitacao = False

                    self.fim_lex = self.prox_char - 1

                    if self.tamanho > 30:
                        self.lexeme = self.delimitar(
                            self.inicio_lex, self.posicao_limite - 1
                        )
                    else:
                        self.lexeme = self.delimitar(self.inicio_lex, self.fim_lex)

                    self.token_type = self.get_token_type(novo_estado, self.lexeme, escopo)

                    self.qtd_antes_truncar = self.fim_lex - self.inicio_lex - 1

                    # tamanho máximo permitido para átomos é 30
                    if self.tamanho > 30:
                        self.truncar()

                    # testar para construção não relevante
                    if self.is_relevante() == False:
                        return (
                            "erro",
                            "erro",
                            self.inicio_lex,
                            self.source_code,
                            self.qtd_antes_truncar,
                        )

                    return (
                        self.lexeme,
                        self.token_type,
                        self.fim_lex + 1,
                        self.source_code,
                        self.qtd_antes_truncar,
                    )
            funcao = self.funcoes[novo_estado]

    def is_relevante(self):
        if self.is_aceitacao == False:
            self.source_code = remover_invalidos(
                self.source_code, self.inicio_lex, self.fim_lex
            )
            self.fim_lex = self.inicio_lex
            self.prox_char = self.inicio_lex
            return False

        if self.token_type == "C01":
            for caracter in self.lexeme:
                if caracter not in ALFABETO_STRING:
                    self.source_code = remover_invalidos(
                        self.source_code, self.inicio_lex, self.fim_lex
                    )
                    self.fim_lex = self.inicio_lex
                    self.prox_char = self.inicio_lex
                    return False
        return True

    def truncar(self):
        self.source_code = remover_invalidos(
            self.source_code, self.posicao_limite + 1, self.fim_lex
        )
        self.fim_lex = self.posicao_limite
        # verificação de casos especiais:
        if self.token_type == "C04":
            if self.source_code[self.fim_lex] in (".", "E"):
                self.fim_lex -= 1
                self.source_code = remover_invalidos(
                    self.source_code, self.fim_lex + 1, self.fim_lex + 1
                )
                self.token_type = "C03"
                self.lexeme = self.delimitar(self.inicio_lex, self.fim_lex)

            else:
                str = self.source_code[self.inicio_lex : self.fim_lex + 1]
                if "." not in str:
                    self.token_type = "C03"
                    self.lexeme = self.delimitar(self.inicio_lex, self.fim_lex)

        if self.token_type == "C01":
            if self.source_code[self.fim_lex] != '"':
                self.source_code = (
                    self.source_code[: self.fim_lex]
                    + '"'
                    + self.source_code[(self.fim_lex + 1) :]
                )
                self.lexeme = self.delimitar(self.inicio_lex, self.fim_lex)

    def get_token_type(self, estado, lexeme, escopo):
        if estado == "Q5":
            return "C03"
        if estado in ("Q7", "Q10"):
            return "C04"
        if estado == "Q11":
            cod = get_codigo(lexeme)
            if cod != None:
                return cod
            return escopo
        if estado == "Q12":
            cod = get_codigo(lexeme)
            if cod != None:
                return cod
            return "C07"
        if estado == "Q15":
            return "C02"
        if estado == "Q18":
            return "C01"

        return get_codigo(self.lexeme)

    def add_estados_base(self):
        self.add_estado("Q0", self.q0, 0)
        self.add_estado("Q1", None, is_estado_final=1)
        self.add_estado("Q2", self.q2, is_estado_final=1)
        self.add_estado("Q3", self.q3)
        self.add_estado("Q4", None, is_estado_final=1)
        self.add_estado("Q5", self.q5, is_estado_final=1)
        self.add_estado("Q6", self.q6)
        self.add_estado("Q7", self.q7, is_estado_final=1)
        self.add_estado("Q8", self.q8)
        self.add_estado("Q9", self.q9)
        self.add_estado("Q10", self.q10, is_estado_final=1)
        self.add_estado("Q11", self.q11, is_estado_final=1)
        self.add_estado("Q12", self.q12, is_estado_final=1)
        self.add_estado("Q13", self.q13)
        self.add_estado("Q14", self.q14)
        self.add_estado("Q15", None, is_estado_final=1)
        self.add_estado("Q16", self.q16)
        self.add_estado("Q17", self.q17)
        self.add_estado("Q18", None, is_estado_final=1)

    def q0(self, caracter, escopo):
        if caracter in (
            "%",
            "(",
            ")",
            ",",
            ";",
            "?",
            "[",
            "]",
            "{",
            "}",
            "+",
            "-",
            "*",
            "/",
            "#",
        ):
            return "Q1"
        if caracter in (":", "<", ">"):
            return "Q2"
        if caracter in ("!", "="):
            return "Q3"
        if caracter in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return "Q5"
        if caracter in (
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ):
            if escopo in ("C05", "C06"):
                return "Q11"
            else:
                return "Q12"
        if caracter == "_":
            return "Q12"
        if caracter == "'":
            return "Q13"
        if caracter == '"':
            return "Q16"
        else:
            return "erro"

    def q2(self, caracter):
        if caracter == "=":
            return "Q4"
        else:
            return "erro"

    def q3(self, caracter):
        if caracter == "=":
            return "Q4"
        else:
            return "erro"

    def q5(self, caracter):
        if caracter in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return "Q5"
        if caracter == ".":
            return "Q6"
        else:
            return "erro"

    def q6(self, caracter):
        if caracter in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return "Q7"
        else:
            return "erro"

    def q7(self, caracter):
        if caracter in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return "Q7"
        if caracter == "E":
            return "Q8"
        else:
            return "erro"

    def q8(self, caracter):
        if caracter in ("+", "-"):
            return "Q9"
        if caracter in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return "Q10"
        else:
            return "erro"

    def q9(self, caracter):
        if caracter in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return "Q10"
        else:
            return "erro"

    def q10(self, caracter):
        if caracter in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return "Q10"
        else:
            return "erro"

    def q11(self, caracter):
        if caracter in (
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ):
            return "Q11"
        else:
            return "erro"

    def q12(self, caracter):
        if caracter in (
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "_",
        ):
            return "Q12"
        else:
            return "erro"

    def q13(self, caracter):
        if caracter in (
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ):
            return "Q14"
        else:
            return "erro"

    def q14(self, caracter):
        if caracter in (
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ):
            return "Q14"
        if caracter == "'":
            return "Q15"
        else:
            return "erro"

    def q16(self, caracter):
        if caracter in ALFABETO:
            return "Q17"
        else:
            return "erro"

    def q17(self, caracter):
        if caracter == '"':
            return "Q18"
        if caracter in ALFABETO:
            return "Q17"
        else:
            return "erro"
