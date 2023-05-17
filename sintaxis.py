import ply.yacc as yacc

from gramatica import tokens

semantic_cube = {
    ('+', 'int', 'int'): 'int',
    ('+', 'int', 'float'): 'float',
    ('+', 'float', 'int'): 'float',
    ('+', 'float', 'float'): 'float',
    ('-', 'int', 'int'): 'int',
    ('-', 'int', 'float'): 'float',
    ('-', 'float', 'int'): 'float',
    ('-', 'float', 'float'): 'float',
    ('*', 'int', 'int'): 'int',
    ('*', 'int', 'float'): 'float',
    ('*', 'float', 'int'): 'float',
    ('*', 'float', 'float'): 'float',
    ('/', 'int', 'int'): 'float',
    ('/', 'int', 'float'): 'float',
    ('/', 'float', 'int'): 'float',
    ('/', 'float', 'float'): 'float',
    ('%', 'int', 'int'): 'int',
    ('%', 'int', 'float'): 'int',
    ('%', 'float', 'int'): 'int',
    ('%', 'float', 'float'): 'int',
    ('==', 'int', 'int'): 'bool',
    ('==', 'float', 'float'): 'bool',
    ('==', 'bool', 'bool'): 'bool',
    ('!=', 'int', 'int'): 'bool',
    ('!=', 'float', 'float'): 'bool',
    ('!=', 'bool', 'bool'): 'bool',
    ('<', 'int', 'int'): 'bool',
    ('<', 'float', 'float'): 'bool',
    ('>', 'int', 'int'): 'bool',
    ('>', 'float', 'float'): 'bool',
    ('<=', 'int', 'int'): 'bool',
    ('<=', 'float', 'float'): 'bool',
    ('>=', 'int', 'int'): 'bool',
    ('>=', 'float', 'float'): 'bool',
    ('&&', 'bool', 'bool'): 'bool',
    ('||', 'bool', 'bool'): 'bool',
    ('!', 'bool', ''): 'bool',
    ('=', 'int', ''): 'int',
    ('=', 'float', ''): 'float',
    ('=', 'bool', ''): 'bool',
    ('=', 'string', ''): 'string',
    ('+', 'string', 'string'): 'string',
}

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'LT', 'GT', 'LTE', 'GTE'),
    ('nonassoc', 'EQ', 'NEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
)

precedence_dict = {op: i for i, ops in enumerate(precedence) for op in ops[1:]}

def lookup_semantic_cube(op, type1, type2):
    key = (op, type1, type2)
    if key in semantic_cube:
        return semantic_cube[key]
    else:
        return f"Error: No matching type for operator '{op}' and operand types '{type1}' and '{type2}'"

def get_expression_type(tokens):
    stack = []
    operators = []
    for token in tokens:
        if token in ('+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!'):
            operators.append(token)
        else:
            stack.append(token)

        while len(operators) > 0 and len(stack) >= 2:
            op = operators[-1]
            a = stack[-2]
            b = stack[-1]
            if (a[1], b[1], op) in semantic_cube:
                result_type = semantic_cube[(a[1], b[1], op)]
                stack = stack[:-2]
                stack.append(('EXPR', result_type))
                operators.pop()
            else:
                raise ValueError(f'Type mismatch for {a} {op} {b}')

    if len(stack) != 1 or len(operators) != 0:
        raise ValueError('Invalid expression')

    return stack[0][1]

def create_temp(temp_counter):
    """
    Generates a temporary variable name and increments the temp counter.
    """
    temp_name = f"t{temp_counter}"
    temp_counter += 1
    return temp_name, temp_counter

# Define grammar rules

# Module
def p_module(p):
    '''module : MODULE ID SEMICOLON module_body'''
    p[0] = ('module', p[2], p[4])

def p_module_body(p):
    '''module_body : LBRACKET declarations statements RBRACKET'''
    p[0] = (p[2], p[3])

# Declarations
def p_declarations(p):
    '''declarations : VAR var_declaration SEMICOLON
                    | function_declaration
                    | empty'''

    if len(p) > 2:
        p[0] = ('declarations', p[1], p[2])
    else:
        p[0] = ('declarations',)

def p_var_declaration(p):
    '''var_declaration : var_type ID
                        | var_type ID ASSIGN expression'''

    if len(p) == 3:
        p[0] = ('var_declaration', p[1], p[2])
    else:
        p[0] = ('var_declaration', p[1], p[2], p[4])

def p_var_type(p):
    '''var_type : INT
                | FLOAT
                | BOOL
                | STRING
                | VECTOR LBRACKET INT_LITERAL RBRACKET
                | MATRIX LBRACKET INT_LITERAL COMMA INT_LITERAL RBRACKET'''

    if len(p) == 2:
        p[0] = ('var_type', p[1])
    elif p[1] == 'vector':
        p[0] = ('var_type', 'vector', p[3])
    else:
        p[0] = ('var_type', 'matrix', p[3], p[5])

# Statements
def p_statements(p):
    '''statements : statement SEMICOLON
                  | statements statement SEMICOLON'''

    if len(p) == 3:
        p[0] = ('statements', p[1], p[2])
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_statement(p):
    '''statement : expression
                 | assignment_statement
                 | conditional_statement
                 | while_loop
                 | for_loop
                 | read_statement
                 | write_statement
                 | return_statement'''

    p[0] = ('statement', p[1])

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression'''

    p[0] = ('assignment_statement', p[1], p[3])
    
def p_conditional_statement(p):
    '''conditional_statement : IF LPAREN expression RPAREN LBRACKET statements RBRACKET 
                             | IF LPAREN expression RPAREN LBRACKET statements RBRACKET ELSE LBRACKET statements RBRACKET'''

    if len(p) == 8:
        p[0] = ('conditional_statement', p[3], p[6])
    else:
        p[0] = ('conditional_statement', p[3], p[6], p[9])

def p_while_loop(p):
    '''while_loop : WHILE LPAREN expression RPAREN LBRACKET statements RBRACKET'''

    p[0] = ('while_loop', p[3], p[6])

def p_for_loop(p):
    '''for_loop : FOR LPAREN assignment_statement SEMICOLON expression SEMICOLON assignment_statement RPAREN LBRACKET statements RBRACKET'''

    p[0] = ('for_loop', p[3], p[5], p[7], p[10])

def p_read_statement(p):
    '''read_statement : READ LPAREN ID RPAREN'''

    p[0] = ('read_statement', p[3])

def p_write_statement(p):
    '''write : WRITE LPAREN expression RPAREN'''

def p_conditional_statement(p):
    '''conditional_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE elif_statement else_statement'''

def p_elif_statement(p):
    '''elif_statement : ELIF LPAREN expression RPAREN LBRACE statement_list RBRACE'''



