import sys
from nyanja.lexer import tokenize
from nyanja.parser import parse
from nyanja.interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("📘 Gwiritsani ntchito: nyanja <dzina la fayilo>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"💥 Fayilo '{filename}' sinapezeke")
        sys.exit(1)

    try:
        tokens = tokenize(code)
        ast = parse(tokens)
        interpreter = Interpreter()
        interpreter.eval(ast)
    except Exception as e:
        print(f"💥 Zolakwika: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()