# padroes.py

PADROES = [
    (r'"[^"\\]*(\\.[^"\\]*)*"', "C01"),  # consCadeia
    (r"'[A-Z]'", "C02"),  # consCaracter
    (r"\b\d+\b", "C03"),  # consInteiro
    (r"\b\d+(\.\d+)?(E[+-]?\d+)?\b", "C04"),  # consReal
    (r"\b[A-Z_][A-Z0-9_]*\b", "C05"),  # nomFuncao
    (r"\b[A-Z_][A-Z0-9_]*\b", "C06"),  # nomPrograma
    (r"\b[A-Z_][A-Z0-9_]*\b", "C07"),  # variavel
]