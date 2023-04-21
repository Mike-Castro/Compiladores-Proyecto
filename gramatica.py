import ply.lex as lex

tokes = (
    'DECLARE',
    'WRITE',
    'READ',
    'IF',
    'ELSE',
    'WHILE',
    'FOR',
    'STEP',
    'TO',
    'AND',
    'OR',
    'RETURN',
    'FUNCTION',

    'PLUS',
    'DIVIDE',
    'MINUS',
    'TIMES',
    'LESSTHAN',
    'GREATERTHAN',
    'LESSTHAN_E',
    'GREATERTHAN_E',
    'EQUAL',
    'NOTEQUAL',
    'ASSIGN',
    'MODULO',

    'COMMA',
    'COLON',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    
    'ID',
    'INT',
    'FLOAT',
    'STRING',
    'BOOLEAN'
)

t_PLUS = 'r\+'
t_DIVIDE = r'/'
t_MINUS = r'-'
t_TIMES = r'\*'

t_LESSTHAN = r'<'
t_GREATERTHAN = r'>' 
t_LESSTHAN_ = r'<=' 
t_GREATERTHAN_E = r'>='
t_EQUAL = r'==' 
t_NOTEQUAL = r'!=' 
t_ASSING = r'=' 
t_MODULO = r'%'

t_COMMA= r','
t_COLON = r':'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'


