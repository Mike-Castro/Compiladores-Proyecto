import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'module': 'MODULE',
    'return': 'RETURN',
    'read': 'READ',
    'write': 'WRITE',
    'list': 'LIST',
    'matrix': 'MATRIX',
    'int': 'INT',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'string': 'STRING',
}

tokens = [
    'PLUS',
    'DIVIDE',
    'MINUS',
    'TIMES',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'EQ',
    'NEQ',
    'ASSIGN',

    'MOD',
    'AND',
    'OR',
    'COMMA',
    'COLON',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    
    'ID',
    'CTEI',
    'CTEF',
    'CTESTRING'
] + list(reserved.values())

t_PLUS = 'r\+'
t_DIVIDE = r'/'
t_MINUS = r'-'
t_TIMES = r'\*'

t_AND = r'&&'
t_OR = r'\|\|'
t_LT = r'<'
t_GT = r'>' 
t_LTE = r'<=' 
t_GTE = r'>='
t_EQ = r'==' 
t_NEQ = r'!=' 
t_ASSIGN = r'=' 
t_MOD = r'%'

t_COMMA= r','
t_COLON = r':'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'

# Expresiones regulares

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTEF(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTESTRING(t):
    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()