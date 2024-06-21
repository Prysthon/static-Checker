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
1. Crie um arquivo com extensão `.241` contendo o código fonte na linguagem Perpertuum2024-1.
2. Execute `main.py` e forneça o nome do arquivo quando solicitado.
3. O compilador gerará os arquivos de relatório `.LEX` e `.TAB` na mesma pasta do código fonte.

## Exemplo de Execução
```sh
$ python main.py
Digite o nome do arquivo: meuTeste
```
