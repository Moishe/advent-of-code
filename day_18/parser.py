import enum
import pathlib
import re

class TokenType(enum.Enum):
    TOKEN_NUM = 0
    TOKEN_PLUS = 1
    TOKEN_MULT = 2
    TOKEN_OPEN_PAREN = 3
    TOKEN_CLOSE_PAREN = 4

token_map = {
    '+': TokenType.TOKEN_PLUS,
    '*': TokenType.TOKEN_MULT,
    '(': TokenType.TOKEN_OPEN_PAREN,
    ')': TokenType.TOKEN_CLOSE_PAREN
}

def add_values(a, b):
    print("Adding %d plus %d" % (a, b))
    return a + b

def mult_values(a, b):
    print("Multiplying %d times %d" % (a, b))
    return a * b

fn_map = {
    TokenType.TOKEN_PLUS: add_values,
    TokenType.TOKEN_MULT: mult_values,
}

token_operators = [TokenType.TOKEN_PLUS, TokenType.TOKEN_MULT]

class Node():
    def __init__(self, token, val):
        self.token = token
        self.value = val
        self.children = None
        self.parens = False

    def __str__(self):
        return "%s: %s" % (self.token, self.value)

def lex(expr):
    tokens = []
    for c in expr:
        if c in token_map:
            token = Node(token_map[c], c)
        elif re.match(r'\d', c):
            token = Node(TokenType.TOKEN_NUM, int(c))
        elif c == ' ':
            continue
        else:
            print("Bad character %s in %s" % (c, expr))
            exit(1)
        tokens.append(token)

    return tokens

def token_values(tokens):
    return [str(x.value) for x in tokens]

def dump_tokens(tokens, msg='', depth=0):
    print("%s %s: %s" % (' ' * depth, msg, token_values(tokens)))

def subexpr(tokens, depth=0):
    dump_tokens(tokens, "subexpr", depth)
    # if a sub expression's first element is just a number, return that and then the rest of the elements
    if tokens[0].token == TokenType.TOKEN_NUM:
        print("Subexpression is just a number")
        return (tokens[0], tokens[1:])

    # if a sub expression's first element is a paren
    if tokens[0].token == TokenType.TOKEN_OPEN_PAREN:
        print("Parsing up to closeparen")
        up_to_close = []
        paren_depth = 1
        for (i, token) in enumerate(tokens[1:]):
            if token.token == TokenType.TOKEN_OPEN_PAREN:
                paren_depth += 1
            if token.token == TokenType.TOKEN_CLOSE_PAREN:
                paren_depth -= 1

            if paren_depth == 0:
                break

            up_to_close.append(token)
        
        left = parse(up_to_close)
        left.parens = True

        i += 2
        remaining = tokens[i:]
        return (left, remaining)

    print ("I don't know what to do with this.")
    exit(1)


def parse(tokens, depth=0):
    dump_tokens(tokens, "Parsing", depth)
    if len(tokens) == 1:
        return tokens[0]

    if tokens[1].token in token_operators:
        # the two clauses here are very close to being duplicated and could certainly
        # be compressed. :shrug:
        if tokens[1].token == TokenType.TOKEN_PLUS and tokens[0].token in token_operators and not tokens[0].parens:
            if tokens[0].parens:
                print("This token has parens")
            (prevleft, prevright) = tokens[0].children
            tokens[0].children = (prevleft, tokens[1])
            (right, remaining) = subexpr(tokens[2:])
            tokens[1].children = (prevright, right)
            if remaining:
                remaining.insert(0, tokens[0])
                return parse(remaining, depth+1)
            else:
                return tokens[0]
        else:
            left = tokens[0]
            (right, remaining) = subexpr(tokens[2:])
            print("Adding L %s and R %s (%s)" % (left, right, token_values(remaining)))
            tokens[1].children = (left, right)
            if remaining:
                remaining.insert(0, tokens[1])
                return parse(remaining, depth+1)
            else:
                return tokens[1]

    elif tokens[0].token == TokenType.TOKEN_OPEN_PAREN:
        (left, remaining) = subexpr(tokens)
        remaining.insert(0, left)
        return parse(remaining, depth+1)

    print("Aw hell, I dunno what to do :shrug:")
    exit(1)

def print_indent(msg, depth):
    print("%s %s" % (' ' * depth, msg))

def print_ast(ast, depth = 0):
    print_indent("Operator: %s" % ast.value, depth)
    if ast.children:
        print_indent("Left:", depth)
        print_ast(ast.children[0], depth + 1)

        print_indent("Right:", depth)
        print_ast(ast.children[1], depth + 1)

def compute(ast):
    if not ast.children:
        return ast.value
    
    return fn_map[ast.token](compute(ast.children[0]), compute(ast.children[1]))

inputs = [
    '(3 * 2) + 5'
    '2 * 3 + (4 * 5)',
    '5 + (8 * 3 + 9 + 3 * 4 * 3)',
    '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))',
    '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2',
]

f = open(pathlib.Path(__file__).parent.absolute() / 'input.txt')
inputs = [x.rstrip() for x in f.readlines()]

sum = 0
for input in inputs:
    print ("EVALUATING: %s" % input)
    tokens = lex(input)
    print("\n".join([str(x) for x in tokens]))

    ast = parse(tokens)

    print_ast(ast)

    result = compute(ast)
    print("  Result: %d" % result)
    sum += result

print("Final sum: %d" % sum)