import re

#NyanjaLang keywords
KEYWORDS = {
    "nchito": "FUNCTION",
    "kalasi": "CLASS",
    "ngati": "IF",
    "zina": "ELSE",
    "pamene": "WHILE",
    "chita": "DO",
    "bwezera": "RETURN",
    "lembani": "PRINT",
    "choonadi": "TRUE",
    "boza": "FALSE",
    "pitirizani": "CONTINUE",
    "chokani": "BREAK",
    "kapena": "OR",
    "ndi": "AND",
    "ayi": "NOT",
    "mtundu": "TYPE",
    "konza": "MAKE",
    "tenga": "GET",
    "kuchokamu": "FROM"
}

# Token specification using regex
TOKEN_SPEC = [
    ("PLUS_ASSIGN", r"\+="),
    ("MINUS_ASSIGN", r"-="),
    ("MULT_ASSIGN", r"\*="),
    ("DIV_ASSIGN", r"/="),
    ("NUMBER",   r"\d+(\.\d+)?"),
    ("STRING",   r'"[^"]*"'),
    ("ID",       r"[a-zA-Z_]\w*"),
    ("ASSIGN",   r"="),
    ("END",      r";"),
    ("OP",       r"[+\-*/<>=!]+"),
    ("LPAREN",   r"\("),
    ("RPAREN",   r"\)"),
    ("LBRACE",   r"\{"),
    ("RBRACE",   r"\}"),
    ("COMMA",    r","),
    ("SKIP",     r"[ \t]+"),
    ("NEWLINE",  r"\n"),
    ("COMMENT",  r"//.*"),
]

# Combine into one regex
TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)

def tokenize(code):
    tokens = []
    for match in re.finditer(TOKEN_REGEX, code):
        kind = match.lastgroup
        value = match.group()

        if kind == "SKIP" or kind == "COMMENT" or kind == "NEWLINE":
            continue

        if kind == "ID" and value in KEYWORDS:
            kind = KEYWORDS[value]

        tokens.append((kind, value))
    return tokens