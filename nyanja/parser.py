class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = float(value) if '.' in value else int(value)
    def __repr__(self): return f"Number({self.value})"

class String(ASTNode):
    def __init__(self, value):
        self.value = value.strip('"')
    def __repr__(self): return f"String('{self.value}')"

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self): return f"Variable('{self.name}')"

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self): return f"BinaryOp({self.left}, '{self.op}', {self.right})"

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self): return f"Assignment('{self.name}', {self.value})"

class Print(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self): return f"Print({self.expression})"

class Return(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    def __repr__(self): return f"Return({self.expression})"

class If(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
    def __repr__(self): return f"If({self.condition}, body={self.body}, else={self.else_body})"

class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self): return f"While({self.condition}, body={self.body})"

class Function(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    def __repr__(self): return f"Function('{self.name}', params={self.params}, body={self.body})"

class Call(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self): return f"Call('{self.name}', args={self.args})"

def parse(tokens):
    i = 0

    def peek(offset=0):
        if i + offset >= len(tokens):
            return (None, None)
        return tokens[i + offset]

    def match(expected_type):
        nonlocal i
        if i < len(tokens) and tokens[i][0] == expected_type:
            tok = tokens[i]
            i += 1
            return tok
        cur_type, cur_val = peek()
        raise SyntaxError(f"Zolakwika: Expected {expected_type}, got {cur_type} ('{cur_val}') at index {i}")

    # --- Expression Logic ---
    def parse_expression():
        left = parse_term()
        while peek()[0] == 'OP':
            op = match('OP')[1]
            right = parse_term()
            left = BinaryOp(left, op, right)
        return left

    def parse_term():
        tok_type, tok_val = peek()
        if tok_type == 'NUMBER':
            match('NUMBER')
            return Number(tok_val)
        elif tok_type == 'STRING':
            match('STRING')
            return String(tok_val)
        elif tok_type == 'ID':
            name = match('ID')[1]
            if peek()[0] == 'LPAREN':
                match('LPAREN')
                args = []
                if peek()[0] != 'RPAREN':
                    while True:
                        args.append(parse_expression())
                        if peek()[0] == 'COMMA':
                            match('COMMA')
                        else:
                            break
                match('RPAREN')
                return Call(name, args)
            return Variable(name)
        elif tok_type == 'LPAREN':
            match('LPAREN')
            expr = parse_expression()
            match('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {tok_type} {tok_val}")

    # --- Helper to parse { ... } blocks ---
    def parse_block():
        match('LBRACE')
        block_body = []
        while peek()[0] != 'RBRACE' and peek()[0] is not None:
            block_body.append(parse_statement())
        match('RBRACE')
        return block_body

    # --- Statement Logic ---
    def parse_statement():
        tok_type, tok_val = peek()

        if tok_type == 'ID' and peek(1)[0] == 'ASSIGN':
            var_name = match('ID')[1]
            match('ASSIGN')
            expr = parse_expression()
            match('END')
            return Assignment(var_name, expr)
        
        elif tok_type == 'ID' or tok_type == 'NUMBER' or tok_type == 'STRING' or tok_type == 'LPAREN':
            expr = parse_expression()
            match('END') 
            return expr 

        elif tok_type == 'PRINT': # lembani
            match('PRINT')
            expr = parse_expression()
            match('END')
            return Print(expr)

        elif tok_type == 'RETURN': 
            match('RETURN')
            expr = parse_expression()
            match('END')
            return Return(expr)

        elif tok_type == 'FUNCTION': # nchito
            match('FUNCTION')
            func_name = match('ID')[1]
            match('LPAREN')
            params = []
            if peek()[0] != 'RPAREN':
                while True:
                    params.append(match('ID')[1])
                    if peek()[0] == 'COMMA':
                        match('COMMA')
                    else:
                        break
            match('RPAREN')
            body = parse_block() # Use block helper
            return Function(func_name, params, body)

        elif tok_type == 'IF': # ngati
            match('IF')
            condition = parse_expression()
            body = parse_block() # Use block helper
            else_body = None
            if peek()[0] == 'ELSE': # zina
                match('ELSE')
                else_body = parse_block() # Use block helper
            return If(condition, body, else_body)

        elif tok_type == 'WHILE': # pamene
            match('WHILE')
            condition = parse_expression()
            body = parse_block()
            return While(condition, body)

        else:
            # Skip empty/unexpected tokens
            raise SyntaxError(f"Unknown statement starting with: {tok_type} {tok_val}")

    # --- Main Loop ---
    ast = []
    while peek()[0] is not None:
        ast.append(parse_statement())
    
    return ast