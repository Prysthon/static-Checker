# lexer.py

from palavras import PALAVRAS
from alfabeto import ALFABETO
from utils import uppercase_menos_sequencias

class Lexer:
    def __init__(self, source_code):
        self.source_code = uppercase_menos_sequencias(self.source_code)
        self.tokens_dados_p_relatorio = []
        self.current_line = 1
        self.inicio_lex = 0
        self.fim_lex = 0
        self.especial = 0
        

    def formacao_lexeme(self, inicio_lex):
        lexeme = ''
        token_type = ''
        qtd_antes_truncar = 0

        self.filtro()
        lexeme, token_type, qtd_antes_truncar = self.formacao()
        return (lexeme, token_type)

    '''
        Como fazer formacao():
        1. Implementar o autômato:
            - O autômato deve receber a posição atual no texto-fonte, processar o caracter nessa posição e avançar seu estado, avançando também uma posição no texto-fonte;

            - O token_type é definido por qual foi o estado de aceitação em que o átomo foi delimitado;
                - Caso especial -> variavel, nomFuncao e nomPrograma:
                  * variavel, nomFuncao e nomPrograma tem a mesma lei de formação; no entanto, variavel é o único tipo entre esses três que permite "_";
                  * sendo assim, caso seja formada uma variavel com um "_", deve-se retornar um token_type diferente para que a análise de escopo seja ignorada
                  * somente para essa variavel especificamente.

            - Ao chegar em um estado de aceitação que não possua transições, o átomo é delimitado naquele ponto e o autômato se encerra;

            - Se ocorrer uma transição não prevista, o átomo é delimitado na posição anterior do texto fonte e o autômato se encerra;

            - Se o tamanho do átomo se tornar maior que 30, ele salva a posição do caracter número 30 e continua lendo os caracteres seguintes até encontrar um caracter delimitador.
            
            - Ao encontrar, ele salva numa variável o tamanho do átomo antes de truncar e a posição do caracter delimitador. Depois, ele trunca o átomo;
            
            - Ao truncar o átomo, todos caracteres que estiverem entre a posição 30 deste átomo e o próximo delimitador são filtrados, como se fossem
              caracteres inválidos, com a função remover_invalidos(posicao_do_fim_do_atomo + 1, posicao_do_delimitador - 1);
            
            - Após truncar, ele verifica se precisa modificar de alguma maneira o átomo resultante. Casos:
                1. Ao truncar um átomo consReal, caso o átomo que resulte possua um "." no final ou um "E" no final, deve-se encurtar ainda mais o átomo para impedir isso,
                   e definir o token_type como consInteiro
                2. Ao truncar um átomo consReal, caso o átomo que resulte não possua mais um ".", deve-se definir o token_type como consInteiro.
                3. Ao truncar um átomo consCadeia, caso ele não termine com um ' " ', deve-se substituir o último caracter por um ' " '.

            - Após truncar (se tiver sido necessário), verificar se a construção é relevante, ou seja, verificar um dos seguintes casos:
                1. String com caracteres internos não permitidos: consCadeia pode possuir apenas os caracteres [A - Z] | [0 - 9] | "$" | "_" | ".";
                2. Caso o autômato termine num estado de não aceitação
            
            - Caso a construção seja não relevante, o átomo inteiro deve ser filtrado e removido com remover_invalidos(posicao_do_inicio_do_atomo, posicao_do_fim_do_atomo)

            - Caso a construção seja não relevante, tentar novamente formar outro átomo (até conseguir formar um átomo e o retornar, ou até EOF)

            - Após tudo isso, modificar self.inicio_lex para ser igual a self.fim_lex + 1 (para que se continue o processo)

            - Após tudo isso, retorna (lexeme, token_type, qtd_antes_truncar)
                        
    '''
    
    def formacao(self):
        # fazer
        self.truncagem()
    
    def truncagem(self):
        # fazer
        return

    def remover_invalidos(self, inicio, fim):
        str = self.source_code[:inicio] + self.source_code[(fim + 1):]
        return str

    def filtro(self):
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

    def tratamento_reservada(self, lexeme, token_type):
        # adciona palavra reservada na lista de dados
        # index (-1) para sinalizar que é uma palavra reservada
        self.tokens_dados_p_relatorio.append((lexeme, token_type, (-1), self.current_line))

    def tratamento_construcoes(self, lexeme, token_type, escopo, symbol_table, qtd_antes_truncar):
        # caso especial da variavel com '_'
        # if token_type == '000':
        #   self.especial = 1

        # verifica o escopo

        # if self.especial == 0
        if token_type in ('C05', 'C06', 'C07'):
            token_type = escopo
        # else self.especial = 0

        # adciona átomo formado na tabela de símbolos
        symbol_table.add(lexeme, token_type, qtd_antes_truncar)
        
        # adciona construção na lista de dados
        self.tokens_dados_p_relatorio.append(
            (lexeme, token_type, symbol_table.getIndex(lexeme, token_type), self.current_line)
        )

        return token_type

    def formar_atomo(self, inicio_lex, escopo, symbol_table):
        self.inicio_lex = inicio_lex
        lexeme = ""
        token_type = ""
        
        while self.inicio_lex in (' ', '\n', '\t', '\r'):
            if self.inicio_lex == '\n':
                self.current_line += 1
            self.inicio_lex += 1

        if self.inicio_lex == 'EOF':
            return (token_type, self.inicio_lex)

        lexeme, token_type, qtd_antes_truncar = self.formacao_lexeme(inicio_lex)

        if self.is_reservada(lexeme):
            self.tratamento_reservada(lexeme, token_type)
            return (token_type, self.inicio_lex)
        else:
            token_type = self.tratamento_construcoes(lexeme, token_type, escopo, symbol_table, qtd_antes_truncar)
            return (token_type, self.inicio_lex)

    def get_tokens_dados_p_relatorio(self):
        return self.tokens_dados_p_relatorio
