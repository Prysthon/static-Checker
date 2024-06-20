1. emitir o relatório .TAB
2. Fazer a análise de escopo funcionar (corrigir o autômato) -> FEITO (funcionando com nomPrograma, não testei com nomFuncao)
4. Fazer o guia de uso para o professor
5. Fazer todos casos funcionarem:
  1- Filtragem correta de:
    1 -> Comentários de linha
    2 -> Comentários de bloco
    3 -> Caracteres fora do alfabeto da linguagem
  2- Átomo que termina com transição não prevista (não necessariamente sendo " ")
  3- Átomo que termina por atingir estado final sem mais transições
  4- Átomo maior que 30 caracteres:
    1 -> Truncar corretamente, filtrando os caracteres depois do limite e antes do próximo delimitador
    2 -> Casos especiais de truncagem:
      1: Float que termina com "." ou "E": reduzir em 1 o tamanho, filtrar esse "." ou "E", mudar o tipo do átomo para Inteiro
      2: Float que passou a não ter mais um ".": transformar em inteiro
      3: String que não termina com '"': transformar o último caracter em uma '"'
  5- Verificar construções não relevantes:
    1 -> String com caracteres inválidos no meio
    2 -> Átomo que foi delimitado num estado não final