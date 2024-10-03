# --- Token Types ---
INTEGER, FLOAT, STRING, CHAR = "INTEGER", "FLOAT", "STRING", "CHAR"
PLUS, MINUS, MULTIPLY, DIVIDE, MODULO = "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "MODULO"
LPAREN, RPAREN = "LPAREN", "RPAREN"
IDENTIFIER, ASSIGN = "IDENTIFIER", "ASSIGN"
KEYWORD, BOOLEAN =  "KEYWORD", "BOOLEAN"
EOF = "EOF"  # End of File marker
COMMA = "COMMA"

# --- Lexer ---

class Token:
    """Represents a single token in the source code."""
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    """
    The Lexer's job is to break down the source code into a stream of Tokens.
    It does this character by character, recognizing patterns that form valid tokens.
    """

    def __init__(self, text):
        self.text = text  # The entire source code
        self.position = 0  # Current position in the source code
        self.current_char = self.text[self.position] if self.text else None

    def error(self):
        raise Exception("Invalid character")

    def advance(self):
        """Moves the pointer one position ahead in the source code."""
        self.position += 1
        if self.position < len(self.text):
            self.current_char = self.text[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        """Skips over any whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_number(self):
        """Recognizes and constructs integer or float tokens."""
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()

        if '.' in result:
            return Token(FLOAT, float(result))
        else:
            return Token(INTEGER, int(result))

    def get_string(self):
        """Recognizes and constructs string tokens."""
        result = ''
        self.advance()  # Skip opening quote
        while self.current_char is not None and self.current_char != '"':
            # Basic escape sequence handling (could be expanded)
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                else:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()

        self.advance()  # Skip closing quote
        return Token(STRING, result)

    def get_char(self):
        """Recognizes and constructs char tokens."""
        result = ''
        self.advance()  # Skip opening quote
        if self.current_char == '\\':
            self.advance()
            if self.current_char == 'n':
                result = '\n'
            elif self.current_char == 't':
                result = '\t'
            else:
                result = self.current_char
        else:
            result = self.current_char
        self.advance()  # Skip closing quote
        return Token(CHAR, result)

    def get_identifier(self):
        """
        Recognizes identifiers and keywords.
        An identifier can start with a letter or underscore, followed by letters, digits, or underscores.
        """
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # Determine if it's a keyword or a regular identifier
        if result in ("if", "elif", "else", "match", "case", "for", "while", "fun", "var", "const", "bool", "char", "int", "float", "string", "enum", "struct", "list", "array", "True", "False", "return"):  # Add your language's keywords here
            return Token(KEYWORD, result)
        else:
            return Token(IDENTIFIER, result)

    def get_next_token(self):
        """
        This is the main function of the Lexer.
        It's called repeatedly to fetch the next token from the source code.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')

            if self.current_char == '%':
                self.advance()
                return Token(MODULO, '%')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == '"':
                return self.get_string()

            if self.current_char == "'":
                return self.get_char()

            if self.current_char == ",":
                self.advance()
                return Token(COMMA, ",")

            if self.current_char.isalpha() or self.current_char == '_':
                return self.get_identifier()

            self.error()
        return Token(EOF, None)


# --- Abstract Syntax Tree (AST) Nodes ---

class NumberNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"StringNode({self.value})"

class CharNode:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"CharNode({self.value})"

class VariableNode:
    def __init__(self, token):
        self.token = token
        self.name = token.value

    def __repr__(self):
        return f"VariableNode({self.name})"

class AssignNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"AssignNode({self.left}, {self.op}, {self.right})"

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"

class UnaryOpNode:
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOpNode({self.op}, {self.operand})"

class IfNode:
    def __init__(self, condition, body, elif_nodes=None, else_body=None):
        self.condition = condition
        self.body = body
        self.elif_nodes = elif_nodes if elif_nodes else []
        self.else_body = else_body

    def __repr__(self):
        return f"IfNode({self.condition}, {self.body}, {self.elif_nodes}, {self.else_body})"

class ElifNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"ElifNode({self.condition}, {self.body})"

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileNode({self.condition}, {self.body})"

class ForNode:
    def __init__(self, var_name, start, end, step, body):
        self.var_name = var_name
        self.start = start
        self.end = end
        self.step = step
        self.body = body

    def __repr__(self):
        return f"ForNode({self.var_name}, {self.start}, {self.end}, {self.step}, {self.body})"

class FunctionDefNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDefNode({self.name}, {self.params}, {self.body})"

class FunctionCallNode:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCallNode({self.name}, {self.arguments})"

class ReturnNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ReturnNode({self.value})"


# --- Parser ---

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return NumberNode(token)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return NumberNode(token)
        elif token.type == STRING:
            self.eat(STRING)
            return StringNode(token)
        elif token.type == CHAR:
            self.eat(CHAR)
            return CharNode(token)
        elif token.type == IDENTIFIER:
            self.eat(IDENTIFIER)
            return VariableNode(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            self.error()

    def term(self):
        node = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE, MODULO):
            op_token = self.current_token
            if op_token.type == MULTIPLY:
                self.eat(MULTIPLY)
            elif op_token.type == DIVIDE:
                self.eat(DIVIDE)
            elif op_token.type == MODULO:
                self.eat(MODULO)
            node = BinOpNode(left=node, op=op_token, right=self.factor())
        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            op_token = self.current_token
            if op_token.type == PLUS:
                self.eat(PLUS)
            elif op_token.type == MINUS:
                self.eat(MINUS)
            node = BinOpNode(left=node, op=op_token, right=self.term())

        return node

    def variable(self):
        node = VariableNode(self.current_token)
        self.eat(IDENTIFIER)
        return node

    def statement(self):
        if self.current_token.type == KEYWORD:
            if self.current_token.value == "if":
                return self.if_statement()
            elif self.current_token.value == "while":
                return self.while_statement()
            elif self.current_token.value == "for":
                return self.for_statement()
            elif self.current_token.value == "return":
                return self.return_statement()
        elif self.current_token.type == IDENTIFIER:
            if self.lexer.current_char == '(':
                return self.function_call()
            else:
                return self.assignment_statement()
        else:
            self.error()

    def return_statement(self):
        self.eat(KEYWORD)  # Eat the 'return' keyword
        value_node = self.expr()  # Parse the value to be returned
        return ReturnNode(value_node)

    def function_call(self):
        name = self.variable()
        self.eat(LPAREN)
        arguments = self.argument_list()
        self.eat(RPAREN)
        return FunctionCallNode(name, arguments)

    def argument_list(self):
        args = []
        if self.current_token.type != RPAREN:
            args.append(self.expr())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                args.append(self.expr())
        return args

    def if_statement(self):
        elif_nodes = []
        else_body = None

        self.eat(KEYWORD)
        condition = self.expr()
        body = self.block()

        while self.current_token.type == KEYWORD and self.current_token.value == "elif":
            self.eat(KEYWORD)
            elif_condition = self.expr()
            elif_body = self.block()
            elif_nodes.append(ElifNode(elif_condition, elif_body))

        if self.current_token.type == KEYWORD and self.current_token.value == "else":
            self.eat(KEYWORD)
            else_body = self.block()

        return IfNode(condition, body, elif_nodes, else_body)

    def while_statement(self):
        self.eat(KEYWORD)
        condition = self.expr()
        body = self.block()
        return WhileNode(condition, body)

    def for_statement(self):
        self.eat(KEYWORD)
        self.eat(LPAREN)
        var_name = self.variable().name
        self.eat(ASSIGN)
        start = self.expr()
        self.eat(COMMA)
        end = self.expr()
        if self.current_token.type == COMMA:
            self.eat(COMMA)
            step = self.expr()
        else:
            step = None
        self.eat(RPAREN)
        body = self.block()
        return ForNode(var_name, start, end, step, body)

    def function_definition(self):
        self.eat(KEYWORD)
        name = self.variable().name
        self.eat(LPAREN)
        params = self.parameter_list()
        self.eat(RPAREN)
        body = self.block()
        return FunctionDefNode(name, params, body)

    def parameter_list(self):
        params = []
        if self.current_token.type == IDENTIFIER:
            params.append(self.variable().name)
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                params.append(self.variable().name)
        return params

    def assignment_statement(self):
        left = self.variable()
        op = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        return AssignNode(left, op, right)

    def block(self):
        statements = []
        while self.current_token.type != EOF:
            statements.append(self.statement())
        return statements

    def program(self):
        nodes = []
        while self.current_token.type != EOF:
            if self.current_token.type == KEYWORD and self.current_token.value == "fun":
                nodes.append(self.function_definition())
            else:
                nodes.append(self.statement())
        return nodes

# --- Example Usage ---

# Example code:
code = """
var x = 10
if x > 5
    x = x - 1
elif x < 5
    x = x + 1
else
    x = 0

while x > 0
    x = x - 2

for (i = 0, i < 5, i = i + 1)
    # Loop body
    var y = 10

fun add(a, b)
    return a + b

var sum = add(5, 3)
"""

lexer = Lexer(code)
parser = Parser(lexer)
ast = parser.program()

# Print the generated AST (for debugging)
print(ast)
