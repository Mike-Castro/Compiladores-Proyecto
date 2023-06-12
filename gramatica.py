import os
import codecs
import re
import ply.lex as lex

# Palabras reservadas # 
reserved = {
    'int' : 'INT',
    'float' : 'FLOAT',
    'string' : 'STRING',
    'bool' : 'BOOL',
    'func': 'FUNC',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do' : 'DO',
    'for': 'FOR',
    'to' : 'TO',
    'main': 'MAIN',
    'return': 'RETURN',
    'read': 'READ',
    'write': 'WRITE',
    'program' : 'PROGRAM',
    'forward' : 'FORWARD',
    'backward' : 'BACKWARD',
    'penup' : 'PENUP',
    'pendown' : 'PENDOWN',
    'pensize' : 'PENSIZE',
    'left' : 'LEFT',
    'right' : 'RIGHT',
    'cricle' : 'CIRCLE',
    'speed' : 'SPEED',
    'open' : 'OPEN',
    'end' : 'END'
}

# Tokens #
tokens = [
    'ID',
    'CTEI',
    'CTEF',
    'CTESTRING',

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
    'NOT',

    'MOD',
    'AND',
    'OR',
    'COMMA',
    'SEMICOLON',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET'
]

# Palabras reservadas mas tokens #
tokens = tokens + list(reserved.values())

# Definicion de tokens # 
t_PLUS = r'\+'
t_DIVIDE = r'/'
t_MINUS = r'\-'
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
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_ignore = ' \t'

# Expresion detecta valor flotante # 
def t_CTEF(t):
    r'[+-]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

# Expresion detecta valor id # 
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Expresion detecta valor entero # 
def t_CTEI(t):
    r'[-]?[0-9]+'
    t.value = int(t.value)
    return t

# Expresion detecta valor string # 
def t_CTESTRING(t):
    r'\".*\"'
    return t

# Expresion detecta valor booleano # 
def t_BOOL(t):
    r'true|false'
    t.value = t.value.lower()
    return t

# Detecta una nueva linea # 
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Detecta caracter no definido en la gramatica # 
def t_error(t):
    print(f"Error: Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Creacion de lexer # 
lexer = lex.lex()