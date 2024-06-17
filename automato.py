# automato.py
from alfabeto import ALFABETO
from utils import remover_invalidos
from utils import get_codigo

"""
        Implementar o autômato:
            # FEITO # - O autômato deve receber a posição atual no texto-fonte, processar o caracter nessa posição e avançar seu estado, avançando também uma posição no texto-fonte;

            - O token_type é definido por qual foi o estado de aceitação em que o átomo foi delimitado;
                - Caso especial -> variavel, nomFuncao e nomPrograma:
                  * variavel, nomFuncao e nomPrograma tem a mesma lei de formação; no entanto, variavel é o único tipo entre esses três que permite "_";
                  * sendo assim, caso seja formada uma variavel com um "_", deve-se retornar um token_type diferente para que a análise de escopo seja ignorada
                  * somente para essa variavel especificamente.

            # FEITO # - Ao chegar em um estado de aceitação que não possua transições, o átomo é delimitado naquele ponto e o autômato se encerra;

            # FEITO # - Se ocorrer uma transição não prevista, o átomo é delimitado na posição anterior do texto fonte e o autômato se encerra;

            # FEITO # - Se o tamanho do átomo se tornar maior que 30, ele salva a posição do caracter número 30 e continua lendo os caracteres seguintes até encontrar um caracter delimitador.
            
            # FEITO # - Ao encontrar, ele salva numa variável o tamanho do átomo antes de truncar e a posição do caracter delimitador. Depois, ele trunca o átomo;
            
            # FEITO # Ao truncar o átomo, todos caracteres que estiverem entre a posição 30 deste átomo e o próximo delimitador são filtrados, como se fossem
              caracteres inválidos, com a função remover_invalidos(posicao_do_fim_do_atomo + 1, posicao_do_delimitador - 1);
            
            # FEITO # - Após truncar, ele verifica se precisa modificar de alguma maneira o átomo resultante. Casos:
                1. Ao truncar um átomo consReal, caso o átomo que resulte possua um "." no final ou um "E" no final, deve-se encurtar ainda mais o átomo para impedir isso,
                   e definir o token_type como consInteiro
                2. Ao truncar um átomo consReal, caso o átomo que resulte não possua mais um ".", deve-se definir o token_type como consInteiro.
                3. Ao truncar um átomo consCadeia, caso ele não termine com um ' " ', deve-se substituir o último caracter por um ' " '.

            # FEITO # - Após truncar (se tiver sido necessário), verificar se a construção é relevante, ou seja, verificar um dos seguintes casos:
                1. String com caracteres internos não permitidos: consCadeia pode possuir apenas os caracteres [A - Z] | [0 - 9] | "$" | "_" | ".";
                2. Caso o autômato termine num estado de não aceitação
            
            # FEITO # - Caso a construção seja não relevante, o átomo inteiro deve ser filtrado e removido com remover_invalidos(posicao_do_inicio_do_atomo, posicao_do_fim_do_atomo)
            # FEITO # - Caso a construção seja não relevante, tentar novamente formar outro átomo (até conseguir formar um átomo e o retornar, ou até EOF)

            - Após tudo isso, modificar self.inicio_lex para ser igual a self.fim_lex + 1 (para que se continue o processo)

            - Após tudo isso, retorna (lexeme, token_type, qtd_antes_truncar)
    """

class AutomatoLex:
    
    def __init__(self, texto_fonte):
        self.estado_inicial = 'Q0'
        self.funcoes = {}
        self.estados_finais = []
        self.texto_fonte = texto_fonte
        self.inicio_lex = 0
        self.fim_lex = 0
        self.tamanho = 1
        self.tamanho_antes_truncar = 0
        self.posicao_limite = 0
        self.is_aceitacao = 0
        self.lexeme = ''
        self.token_type = ''

    def add_estado(self, nome, funcao, is_estado_final = 0):
        nome = nome.upper()
        self.funcoes[nome] = funcao
        if is_estado_final:
            self.estados_finais.append(nome)

    def run(self, texto_fonte, inicio_lex):
        self.texto_fonte = texto_fonte
        self.inicio_lex = inicio_lex
        self.fim_lex = inicio_lex
        novo_estado = self.estado_inicial

        funcao = self.funcoes[self.estado_inicial]

        while True:
            velho_estado = novo_estado
            novo_estado = funcao(self.texto_fonte[self.fim_lex])
            if novo_estado in self.estados_finais:
                self.is_aceitacao = 1
            else:
                self.is_aceitacao = 0

            if novo_estado == 'erro': # transição não prevista, delimitação ocorre na posição anterior
                self.fim_lex -= 1
                self.lexeme = texto_fonte[self.inicio_lex:self.fim_lex + 1]
                self.token_type = self.get_token_type(velho_estado)
                self.truncar()

                if self.is_relevante() == False:
                    return ('ERRO', 'ERRO', self.inicio_lex, self.texto_fonte, 0)
                
                self.tamanho_antes_truncar = self.fim_lex - self.posicao_limite

                return (self.lexeme, self.token_type, self.fim_lex + 1, self.texto_fonte, self.tamanho_antes_truncar)
                # ele retorna: o lexeme, o token_type, a proxima posicao, o texto_fonte modificado, e o tamanho antes de truncar
            
            if novo_estado in self.estados_finais:
                if novo_estado not in self.funcoes: # estado final sem mais transições, delimitação ocorre na posiução atual
                    self.lexeme = texto_fonte[self.inicio_lex:self.fim_lex + 1]
                    self.token_type = self.get_token_type(novo_estado)
                    self.truncar()

                if self.is_relevante() == False:
                    return ('ERRO', 'ERRO', self.inicio_lex, self.texto_fonte, 0)
                
                self.tamanho_antes_truncar = self.fim_lex - self.posicao_limite

                return (self.lexeme, self.token_type, self.fim_lex + 1, self.texto_fonte, self.tamanho_antes_truncar)
                # ele retorna: o lexeme, o token_type, a proxima posicao, o texto_fonte modificado, e o tamanho antes de truncar
                
            else:
                funcao = self.funcoes[novo_estado]
                if self.tamanho == 30:
                    self.posicao_limite = self.fim_lex
                self.fim_lex += 1
                self.tamanho += 1

    def is_relevante(self):
        if self.is_aceitacao == 0:
            remover_invalidos(self.texto_fonte, self.inicio_lex, self.fim_lex)
            return False
        
        if self.token_type == 'C01':
            allowed_chars = set(c for c, *_ in ALFABETO)
            if any(char not in allowed_chars for char in self.lexeme):
                remover_invalidos(self.texto_fonte, self.inicio_lex, self.fim_lex)
                return False
        return True

    def truncar(self):
        if self.tamanho > 30:
            self.texto_fonte = remover_invalidos(self.texto_fonte, self.posicao_limite + 1, self.fim_lex)
            # verificação de casos especiais:
            if self.token_type == 'C04':
                if self.texto_fonte[self.posicao_limite] in ('.', 'E'):
                    self.posicao_limite -= 1
                    self.token_type = 'C03'

            if self.token_type == 'C04':
                str = self.texto_fonte[self.inicio_lex:self.tamanho_limite + 1]
                if '.' not in str:
                    self.token_type = 'C03'

            if self.token_type == 'C01':
                if self.texto_fonte[self.tamanho_limite] != '"':
                    self.texto_fonte[self.tamanho_limite] = '"'

    def get_token_type(self, estado):
        if estado == 'Q5':
            return 'C03'
        if estado in ('Q7', 'Q10'):
            return 'C04'
        if estado == 'Q11':
            return 'C07'
        if estado == 'Q12':
            return 'C00'
        if estado == 'Q15':
            return 'C02'
        if estado == 'Q18':
            return 'C01'
        
        return get_codigo(self.lexeme)

        

    def add_estados_base(self):
        self.add_estado('Q0', self.q0, 0)
        self.add_estado('Q1', None, is_estado_final = 1)
        self.add_estado('Q2', self.q2, is_estado_final = 1)
        self.add_estado('Q3', self.q3)
        self.add_estado('Q4', None, is_estado_final = 1)
        self.add_estado('Q5', self.q5, is_estado_final = 1)
        self.add_estado('Q6', self.q6)
        self.add_estado('Q7', self.q7, is_estado_final = 1)
        self.add_estado('Q8', self.q8)
        self.add_estado('Q9', self.q9)
        self.add_estado('Q10', self.q10, is_estado_final = 1)
        self.add_estado('Q11', self.q11, is_estado_final = 1)
        self.add_estado('Q12', self.q12, is_estado_final = 1)
        self.add_estado('Q13', self.q13)
        self.add_estado('Q14', self.q14)
        self.add_estado('Q15', None, is_estado_final = 1)
        self.add_estado('Q16', self.q16)
        self.add_estado('Q17', self.q17)
        self.add_estado('Q18', None, is_estado_final = 1)

    def q0(self, caracter):
        if caracter in ('%', '(', ')', ',', ';', '?', '[', ']', '{', '}', '+', '-', '*', '/', '#'):
            return 'Q1'
        if caracter in (':', '<', '>'):
            return 'Q2'
        if caracter in ('!', '='):
            return 'Q3'
        if caracter in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return 'Q5'
        if caracter in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'):
            return 'Q11'
        if caracter == '_':
            return 'Q12'
        if caracter == "'":
            return 'Q13'
        if caracter == '"':
            return 'Q16'
        else:
            return 'erro'
        
    def q2(self, caracter):
        if caracter == '=':
            return 'Q4'
        else:
            return 'erro'
        
    def q3(self, caracter):
        if caracter == '=':
            return 'Q4'
        else:
            return 'erro'
        
    def q5(self, caracter):
        if caracter in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return 'Q5'
        if caracter == '.':
            return 'Q6'
        else:
            return 'erro'
        
    def q6(self, caracter):
        if caracter in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return 'Q7'
        else:
            return 'erro'
        
    def q7(self, caracter):
        if caracter == 'E':
            return 'Q8'
        else:
            return 'erro'
        
    def q8(self, caracter):
        if caracter in ('+', '-'):
            return 'Q9'
        if caracter in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return 'Q10'
        else:
            return 'erro'
        
    def q9(self, caracter):
        if caracter in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return 'Q10'
        else:
            return 'erro'
        
    def q10(self, caracter):
        if caracter in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return 'Q10'
        else:
            return 'erro'
        
    def q11(self, caracter):
        if caracter in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            return 'Q11'
        if caracter in ('_'):
            return 'Q12'
        else:
            return 'erro'
        
    def q12(self, caracter):
        if caracter in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'):
            return 'Q12'
        else:
            return 'erro'
        
    def q13(self, caracter):
        if caracter in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'):
            return 'Q14'
        else:
            return 'erro'
        
    def q14(self, caracter):
        if caracter == "'":
            return 'Q15'
        else:
            return 'erro'
    
    def q16(self, caracter):
        if caracter in ALFABETO:
            return 'Q17'
        else:
            return 'erro'
        
    def q17(self, caracter):
        if caracter == '"':
            return 'Q18'
        else:
            return 'erro'