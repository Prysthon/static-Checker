# Static Checker para Perpertuum2024-1

## Descrição
Este projeto implementa um Static Checker para a linguagem Perpertuum2024-1, criado como parte da disciplina de Compiladores no primeiro semestre de 2024 no Senai Cimatec.

## Estrutura do Projeto
- `alfabeto.py`: Define os caracteres válidos na linguagem.
- `automato.py`: Implementa o autômato léxico.
- `header.py`: Contém informações sobre a equipe.
- `lexer.py`: Implementa o analisador léxico.
- `main.py`: Programa principal do compilador.
- `palavras.py`: Define palavras reservadas e símbolos.
- `relatorio.py`: Gera os relatórios de análise léxica e da tabela de símbolos.
- `symbol_table.py`: Implementa a tabela de símbolos.
- `utils.py`: Funções utilitárias.

## Utilização
1. Crie um arquivo com extensão .241 contendo o código na linguagem Perpertuum2024-1.
2. Para executar o programa, é necessário possuir o Python instalado (recomenda-se a versão mais recente, 3.12.4), e utilizar o sistema operacional Windows (recomenda-se a versão mais recente, Windows 11 ou Windows 10).
3. Para executar o programa, é necessário instalar a biblioteca para Python tabulate, que é utilizada para formatação dos relatórios .LEX e .TAB. Para instalar a biblioteca, digite na linha de comando:
```sh
$ pip install tabulate
```
4. Execute o script `main.py` através da linha de comando, passando como parâmetro o nome, caso o arquivo fonte esteja no mesmo diretório do script, ou endereço completo do arquivo fonte, sem a extensão .241.
5. O compilador gerará os arquivos de relatório `.LEX` e `.TAB` na mesma pasta do código fonte.

## Exemplos de Execução
```sh
$ python main.py meuTeste
$ python main.py C:\codigos\meuTeste
```