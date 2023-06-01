import os
import codecs
import re
import turtle
import ply.yacc as yacc
from gramatica import tokens
import numpy as np

class Memory():
    def __init__(self):
        self.memory_spaces = {
            'LocalesInt': (1000, 3000),
            'LocalesFloat': (3000, 5000),
            'LocalesString': (5000, 7000),
            'LocalesBool': (7000, 9000),
            'GlobalesInt': (10000, 13000),
            'GlobalesFloat': (13000, 15000),
            'GlobalesString': (15000, 17000),
            'GlobalesBool': (17000, 19000),
            'TemporalesInt': (20000, 23000),
            'TemporalesFloat': (23000, 25000),
            'TemporalesString': (25000, 27000),
            'TemporalesBool': (27000, 29000),
            'TemporalesPointers': (30000, 33000),
            'ConstantesInt': (33000, 35000),
            'ConstantesFloat': (35000, 37000),
            'ConstantesString': (37000, 40000),
            'ConstantesBool': (40000, 43000)
        }
        self.memory = {
            'LocalesInt': [],
            'LocalesFloat': [],
            'LocalesString': [],
            'LocalesBool': [],
            'GlobalesInt': [],
            'GlobalesFloat': [],
            'GlobalesString': [],
            'GlobalesBool': [],
            'TemporalesInt': [],
            'TemporalesFloat': [],
            'TemporalesPointers': [],
            'TemporalesString': [],
            'TemporalesBool': [],
            'ConstantesInt': [],
            'ConstantesFloat': [],
            'ConstantesString': [],
            'ConstantesBool': []
        }

    def addMemory(self, isGlobal, isTemp, isConst, type, size):
        type = type.upper()
        memory_space = None
        if isGlobal:
            if type == 'INT':
                memory_space = 'GlobalesInt'
            elif type == 'FLOAT':
                memory_space = 'GlobalesFloat'
            elif type == 'BOOL':
                memory_space = 'GlobalesBool'
            elif type == 'STRING':
                memory_space = 'GlobalesString'
        elif isTemp:
            if type == 'INT':
                memory_space = 'TemporalesInt'
            elif type == 'FLOAT':
                memory_space = 'TemporalesFloat'
            elif type == 'POINTER':
                memory_space = 'TemporalesPointers'
            elif type == 'BOOL':
                memory_space = 'TemporalesBool'
            elif type == 'STRING':
                memory_space = 'TemporalesString'
        elif isConst:
            if type == 'INT':
                memory_space = 'ConstantesInt'
            elif type == 'FLOAT':
                memory_space = 'ConstantesFloat'
            elif type == 'STRING':
                memory_space = 'ConstantesString'
            elif type == 'BOOL':
                memory_space = 'ConstantesBool'
        else:
            if type == 'INT':
                memory_space = 'LocalesInt'
            elif type == 'FLOAT':
                memory_space = 'LocalesFloat'
            elif type == 'STRING':
                memory_space = 'LocalesString'
            elif type == 'BOOL':
                memory_space = 'LocalesBool'

        if memory_space is not None:
            start_address, end_address = self.memory_spaces[memory_space]  # Unpack the tuple
            self.memory_spaces[memory_space] = (start_address + size, end_address)  # Concatenate size as a tuple
            self.memory[memory_space] = [0] * size
            return start_address
        else:
            raise ValueError(f"Invalid memory type: {type}")
    
  #  def getTypeFromAddress(self, memory_address):
   #     for memory_space, address_range in self.memory_spaces.items():
    #        print(address_range[0], memory_address, address_range[1])
    #        if address_range[0] <= memory_address < address_range[1]:
     #           return memory_space.split('s')[1].upper()  # Extract the type from the memory space name
     #   raise ValueError(f'Invalid memory address: {memory_address}')
    
    def getTypeFromAddress(self, address):
        if (1000 <= address < 3000) or (10000 <= address < 13000) or (20000 <= address < 23000) or (33000 <= address < 35000):
            return "INT"
        elif (3000 <= address < 5000) or (13000 <= address < 15000) or (23000 <= address < 25000) or (35000 <= address < 37000):
            return "FLOAT"
        elif (5000 <= address < 7000) or (15000 <= address < 17000) or (25000 <= address < 27000) or (37000 <= address < 40000):
            return "STRING"
        elif (7000 <= address < 9000) or (17000 <= address < 19000) or (27000 <= address < 29000) or (40000 <= address < 43000):
            return "BOOL"
        elif 30000 <= address < 33000:
            return "POINTER"
        else:
            return "Unknown type"



pilaOpe = []
pilaTypes = []
pilaOperator = []
quads = []
mem = Memory()
is_global = True
class VariablesTable():
    def __init__(self):
        self.memoryTable = {}
    
    def addVarTable(self, variable_id, memory_address):
        if variable_id in self.memoryTable:
            raise ValueError(f'The variable {variable_id} already exists')
        else:
            self.memoryTable[variable_id] = memory_address
    
    def getVarAddress(self, variable_id):
        if variable_id not in self.memoryTable:
            raise ValueError(f'The variable {variable_id} does not exists')
        else:
            return self.memoryTable.get(variable_id)

    def getTypeFromMemory(self, memory_address):
        return mem.getTypeFromAddress(memory_address)
    
    def printVarTable(self):
        print(self.memoryTable)

varTable = VariablesTable()

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
    ('left', 'OR','AND'),
    ('nonassoc', 'LT', 'GT', 'LTE', 'GTE','EQ', 'NEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
)


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

# Como debe de estar la sintaxis del programa #
def p_program(p):
    '''program : PROGRAM ID SEMICOLON declaration_list function MAIN LPAREN RPAREN bloque END SEMICOLON'''

# Tipo de variable #
def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | STRING'''
    tipo = p[1]
    p[0] = tipo
    pilaTypes.append(tipo)

# Bloque # 
def p_bloque(p):
    '''bloque : LBRACE bloqueB RBRACE'''

def p_bloqueB(p):
    '''bloqueB : statement bloqueB
                | empty'''
    global is_global
    is_global = False
    pass

# Funciones
def p_function(p): 
    '''function : functionF
                | empty'''

def p_functionF(p):
    '''functionF : FUNC idFunc LPAREN RPAREN LBRACE statement_list RBRACE function
                 | FUNC idFunc LPAREN parameter_list RPAREN LBRACE statement_list RBRACE function'''
    
def p_idFunc(p):
    '''
    idFunc : ID
    '''

    global is_global 
    is_global = False
    id = p[1]
    if id not in varTable.memoryTable:
        addrs = mem.addMemory(is_global, False, False, 'POINTER', 1)
        varTable.addVarTable(id, addrs)
    else:
        print(f"Error: Function with ID: '{id}' is already declared")
        

def p_parameter_list(p):
    '''parameter_list : ID
                      | parameter_list COMMA ID'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration_list
                 | assignment_statement
                 | read_statement
                 | write_statement
                 | if_statement
                 | for_statement
                 | while_statement
                 | do_while_statement
                 | return_statement'''
    pass

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_expression(p):
    '''expression : exp1
                    | exp1 AND exp1
                    | exp1 OR exp1'''

    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '&&':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("&&", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1
    elif p[2] == '||':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("||", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1


def p_exp1(p):
    '''exp1 : exp
            | exp LT exp
            | exp GT exp
            | exp EQ exp
            | exp NEQ exp'''
    
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '<':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("LT", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1

    elif p[2] == '>':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("GT", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1
    
    elif p[2] == '==':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("EQ", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1

    elif p[2] == '!=':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("NEQ", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1


def p_exp(p):
    '''exp : term 
             | term PLUS exp
             | term MINUS exp'''

    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        print(op1, op2)
        varTable.printVarTable()
        a = varTable.getVarAddress(op1)
        b = varTable.getVarAddress(op2)
        op1type = varTable.getTypeFromMemory(a).lower()
        op2type = varTable.getTypeFromMemory(b).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("PLUS", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1

    elif p[2] == '-':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("MINUS", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1

def p_term(p):
    '''term : fact
         | fact TIMES term
         | fact DIVIDE term'''
    
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getVarAddress()
        op2type = varTable.getVarAddress()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("TIMES", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1

    elif p[2] == '/':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("DIVIDE", varTable.getVarAddress(op1), varTable.getVarAddress(op2), temp_address))
        temp_address += 1

def p_fact(p):
    '''fact : ID addOp
            | CTEI addConst
            | CTEF addConst
            | CTESTRING addConst'''
    p[0] = p[1]

# Añade el operador y el tipo a la pila
def p_addOp(p):
    '''addOp : 
    '''
  # addrs = mem.addMemory(is_global, False, False, tipo, 1)
  #  varTable.addVarTable(p[2], addrs)
    id = p[-1]
    if id not in varTable.memoryTable:
        print("no existe en la tabla")
    print(id)
    a = varTable.getVarAddress(id)
    print(a)
    b = varTable.getTypeFromMemory(a)
    if a != 'ERROR':
        pilaOpe.append(p[-1])
        pilaTypes.append(b)
    

# Añade el tipo de la constante a la pila
def p_addConst(p):
    '''addConst : 
    '''
    if isinstance(p[-1], int):
        t = mem.addMemory(False, False, True, 'INT', 1)
        varTable.addVarTable(p[-1], t)
        print(t)
        pilaOpe.append(t)
        pilaTypes.append("INT")
    elif isinstance(p[-1], float):
        t = mem.addMemory(False, False, True, 'FLOAT', 1)
        varTable.addVarTable(p[-1], t)
        pilaOpe.append(t)
        pilaTypes.append("FLOAT")
    elif isinstance(p[-1], str):
        t = mem.addMemory(False, False, True, 'STRING', 1)
        varTable.addVarTable(p[-1], t)
        pilaOpe.append(t)
        pilaTypes.append("STRING")

# Declarations
def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration'''

def p_declaration(p):
    '''declaration : tipo ID SEMICOLON
                    | tipo ID COMMA declarationD'''
    tipo = p[1]
    addrs = mem.addMemory(is_global, False, False, tipo, 1)
    varTable.addVarTable(p[2], addrs)

def p_declarationD(p):
    '''declarationD : ID COMMA declarationD
                    | ID SEMICOLON'''
    if len(p) > 4:
        print(len(pilaTypes))
        tipo = pilaTypes.pop()
    else:
        tipo = pilaTypes[-1]

    addrs = mem.addMemory(is_global, False, False, tipo, 1)
    varTable.addVarTable(p[1], addrs)


def p_list_declaration(p):
    '''list_declaration : tipo ID LBRACKET var RBRACKET SEMICOLON'''
    tipo = p[1]
    size = p[4]
    if p[2] not in varTable.memoryTable:
        addrs = mem.addMemory(is_global, False, False, tipo, size)
        varTable.addVarTable(p[2], addrs)
    else:
        print(f"Error: '{p[2]}' is already declared")

def p_var(p):
    '''var : CTEI
            | CTEF'''
    p[0] = p[1]

def p_matrix_declaration(p):
    '''matrix_declaration : tipo ID LBRACKET var RBRACKET LBRACKET var RBRACKET SEMICOLON'''
    tipo = p[1]
    size = p[4] * p[7]
    if p[2] not in varTable.memoryTable:
        addrs = mem.addMemory(is_global, False, False, tipo, size)
        varTable.addVarTable(p[2], addrs)
    else:
        print(f"Error: '{p[2]}' is already declared")

# Statements

def p_assignment_statement(p):
    '''assignment_statement : tipo ID ASSIGN exp SEMICOLON
                            | ID ASSIGN exp SEMICOLON
                            | list_declaration
                            | matrix_declaration'''
    if len(p) == 5:
        print(p[1],p[2],p[3])
        if p[1] in varTable.memoryTable:
            addrs = varTable.getVarAddress(p[1])
            a = varTable.getTypeFromMemory(addrs)
            addrs2 = varTable.getVarAddress(p[3])
            b = varTable.getTypeFromMemory(addrs2)
            temp = mem.addMemory(is_global, False, False, a, 1)
            if a == b:
                quads.append(("ASSIGN", p[3], p[1], temp))
            else:
                print(f"Error: Can't assign two different types '{p[1]}' , '{p[3]}'")
        else: 
            print(f"Error: ID isn't declared '{p[1]}'")
    
    elif len(p) == 6:
        tipo = p[1]
        print(p[1], p[2])
        if p[2] not in varTable.memoryTable:
            temp = mem.addMemory(is_global, False, False, tipo, 1)
            varTable.addVarTable(p[2], temp)
            addrs = varTable.getVarAddress(p[2])
            a = varTable.getTypeFromMemory(addrs)
            addrs2 = varTable.getVarAddress(p[4])
            b = varTable.getTypeFromMemory(addrs2)
 
            if a == b:
                quads.append(("ASSIGN", p[4], p[2], None))
            else:
                print(f"Error: Can't assign two different types '{p[1]}' , '{p[3]}'")
        else: 
            print(f"Error: Variable is already declared '{p[2]}'")


# Leer dato 
def p_read_statement(p):
    '''read_statement : READ LPAREN ID RPAREN SEMICOLON'''
    if p[3] not in varTable.memoryTable:
        print("Error: Variable not declared")
    else:
        quads.append(("READ", None, None, p[3]))

# Imprimir dato
def p_write_statement(p):
    '''write_statement : WRITE LPAREN writeW RPAREN SEMICOLON'''
    p[0] = p[3]
    if isinstance(p[3], str):
        quads.append(("WRITE", p[3], None, None))
    else:
        for item in p[3]:
            quads.append(("WRITE", item, None, None))

def p_writeW(p):
    '''writeW : write_item
              | writeW COMMA write_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_write_item(p):
    '''write_item : CTESTRING
                  | expression'''
    p[0] = p[1]


# Condicion if y if-else # 
def p_if_statement(p):
    '''
    if_statement : IF LPAREN expression_list RPAREN LBRACE statement_list RBRACE
                | IF LPAREN expression_list RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
    '''
    if len(p) == 9:
        condition_quads = p[3]
        statement_quads = p[6]
        for quad in condition_quads:
            quads.append(quad)
        quads.append(("GOTOF", condition_quads[-1][3], None, None))
        # Save the index of the conditional jump quad
        jump_index = len(quads)
        for quad in statement_quads:
            quads.append(quad)
        quads[jump_index][3] = len(quads) + 1
    else:
        condition_quads = p[3]
        if_statement_quads = p[6]
        else_statement_quads = p[10]
        for quad in condition_quads:
            quads.append(quad)
        # Generate quad for conditional jump
        quads.append(("GOTOF", condition_quads[-1][3], None, None))
        jump_index = len(quads)
        # Generate quads for the statements inside the if block
        for quad in if_statement_quads:
            quads.append(quad)
        quads.append(("GOTO", None, None, None))
        skip_else_index = len(quads)
        quads[jump_index][3] = len(quads) + 1
        for quad in else_statement_quads:
            quads.append(quad)
        # Update the jump destination of the unconditional jump quad
        quads[skip_else_index][3] = len(quads) + 1


def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression_list RPAREN LBRACE statement_list RBRACE'''
    start_quad = len(quads)  # Get the index of the current quad
    # Generate quad for the condition
    quads.append(("GOTOF", p[3][-1], None, None))  # Append the quad with the condition
    # Store the index of the condition quad for the jump
    jump_quad_index = len(quads)
    # Generate quads for the statements inside the while loop
    for statement in p[6]:
        quads.append(statement) # Generate quads for the statement_list
    # Generate quad for the jump back to the condition
    quads.append(("GOTO", None, None, start_quad))  # Append the quad for the jump back
    # Update the jump destination in the condition quad
    quads[jump_quad_index][3] = len(quads) # Update the jump destination to the next quad

    pass

def p_do_while_statement(p):
    '''do_while_statement : DO LBRACE statement_list RBRACE WHILE LPAREN expression_list RPAREN'''
    start_quad = len(quads)  # Get the index of the current quad
    # Generate quads for the statements inside the do-while loop
    for statement in p[3]:
        quads.append(statement) # Generate quads for the statement_list
    # Generate quad for the condition
    quads.append(("GOTO", p[6][-1], None, start_quad))  # Append the quad with the condition and jump back to start_quad


def p_for_statement(p):
    '''for_statement : FOR LPAREN assignment_statement SEMICOLON expression SEMICOLON assignment_statement RPAREN LBRACE statement_list RBRACE'''
    start_quad = len(quads)  # Get the index of the current quad
    for statement in p[3]:
        quads.append(statement)
    condition_quad_index = len(quads)  # Get the index of the current quad for the condition
    quads.append(("GOTOF", p[5], None, None))  # Append the quad with the condition and a temporary jump destination
    for statement in p[9]:
        quads.append(statement)  # Generate quads for the statement_list
    end_quad_index = len(quads)  # Get the index of the current quad for the end of the loop
    for statement in p[7]:
        quads.append(statement)
    quads.append(("goto", None, None, start_quad))  # Append the quad with the jump back to the condition
    quads[condition_quad_index][3] = end_quad_index + 1  # Update the jump destination to the end of the loop

    
def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('RETURN', p[2])

# Expressions

def p_empty(p):
    '''empty : '''

def p_error(p):
    print("ERROR en {}".format(p))    

parser = yacc.yacc()

data = '''
program prueba;
float y, k;
int t, x;

main(){
    int p = 12;
    x = 7+9;
}
'''
result = parser.parse(data, debug=False)
print(result) 




