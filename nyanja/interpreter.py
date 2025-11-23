from nyanja.parser import (
    Number, String, Variable, BinaryOp,
    Assignment, Print, Return, If,
    While, Function, Call
)

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' sinapezeke (not found)")

    def set(self, name, value):
        self.vars[name] = value

class ReturnSignal(Exception):
    """Internal signal used to finish a function call early."""
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.functions = {}

    def eval(self, node, env=None):
        if env is None:
            env = self.global_env

        # Handle a block of statements (list)
        if isinstance(node, list):
            result = None
            for stmt in node:
                result = self.eval(stmt, env)
                if isinstance(result, ReturnSignal):
                    return result
            return result

        # Basic types
        if isinstance(node, Number):
            return node.value

        if isinstance(node, String):
            return node.value

        if isinstance(node, Variable):
            return env.get(node.name)

        # Statements
        if isinstance(node, Assignment):
            value = self.eval(node.value, env)
            env.set(node.name, value)
            return value

        if isinstance(node, BinaryOp):
            left = self.eval(node.left, env)
            right = self.eval(node.right, env)

            # Math
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                if right == 0:
                     raise ZeroDivisionError("Kugawa ndi ziro sikutheka (Division by zero)")
                return left / right
            # Comparisons
            elif node.op == '>':
                return left > right
            elif node.op == '<':
                return left < right
            elif node.op == '>=':
                return left >= right
            elif node.op == '<=':
                return left <= right
            elif node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            else:
                 raise RuntimeError(f"Operator yosadziwika: {node.op}")

        if isinstance(node, Print):
            value = self.eval(node.expression, env)
            if isinstance(value, float) and value.is_integer():
                 print(int(value))
            else:
                 print(value)
            return value

        if isinstance(node, Return):
            value = self.eval(node.expression, env)
            raise ReturnSignal(value)

        # Control Flow
        if isinstance(node, If):
            condition = self.eval(node.condition, env)
            if condition:
                return self.eval(node.body, Environment(env))
            elif node.else_body:
                return self.eval(node.else_body, Environment(env))

        if isinstance(node, While):
            while self.eval(node.condition, env):
                try:
                    self.eval(node.body, Environment(env))
                except ReturnSignal as e:
                    raise e
            return None

        # Functions
        if isinstance(node, Function):
            # Store the function node for later use
            self.functions[node.name] = node
            return None
        
        if isinstance(node, Call):
            func_def = self.functions.get(node.name)
            if not func_def:
                raise RuntimeError(f"Nchito '{node.name}' sinapezeke (Function not found)")
            if len(node.args) != len(func_def.params):
                raise RuntimeError(f"Nchito '{node.name}' ikuyembekezera ma arg {len(func_def.params)}, mwapereka {len(node.args)}")

            # 1. Create new environment parented to GLOBAL scope (static scoping)
            func_env = Environment(self.global_env)

            # 2. Evaluate arguments in current scope and bind to parameters in new scope
            for param, arg_node in zip(func_def.params, node.args):
                arg_value = self.eval(arg_node, env)
                func_env.set(param, arg_value)

            # 3. Execute body and catch return signal
            try:
                result = self.eval(func_def.body, func_env)
                return result
            except ReturnSignal as e:
                return e.value

        raise Exception(f"Unknown node identifier: {type(node).__name__}")