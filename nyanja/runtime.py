import sys
from nyanja.lexer import tokenize
from nyanja.parser import parse
from nyanja.interpreter import Interpreter, ReturnSignal

def execute_nyanja_code(code: str, output_stream=sys.stdout, error_stream=sys.stderr):
    """
    Executes a string of NyanjaLang code.
    
    Args:
        code (str): The NyanjaLang source code to execute.
        output_stream: A file-like object for standard output (e.g., sys.stdout, or a StringIO).
        error_stream: A file-like object for error output (e.g., sys.stderr, or a StringIO).
        
    Returns:
        Any: The result of the last evaluated statement, or None.
    """
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    # Redirect stdout/stderr to capture or direct output
    sys.stdout = output_stream
    sys.stderr = error_stream

    result = None
    try:
        tokens = tokenize(code)
        ast = parse(tokens)
        
        interpreter = Interpreter()
        result = interpreter.eval(ast) 
    except (SyntaxError, NameError, TypeError, ZeroDivisionError, RuntimeError) as e:
        print(f"💥 Zolakwika: {e}", file=error_stream)
        result = None # Indicate an error occurred
    except ReturnSignal as e:
        print(f"💥 Zolakwika: 'bwezera' (return) statement outside a function context with value: {e.value}", file=error_stream)
        result = None
    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"💥 Zolakwika Zosadziwika (Unknown Error): {e}", file=error_stream)
        import traceback
        traceback.print_exc(file=error_stream)
        result = None
    finally:
        # IMPORTANT: Restore original stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
    return result