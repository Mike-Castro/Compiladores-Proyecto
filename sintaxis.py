import os
import codecs
import re
import sys
import json
import ply.yacc as yacc
from gramatica import tokens

# Clase memoria, se encarga de asignar una direccion a los diferentes tipos de variables # 
class Memory():
    def __init__(self):
        # Espacios para los diferentes tipos de direccion # 
        self.memory_spaces = {
            'LocalesInt': (1000, 3000),
            'LocalesFloat': (3000, 5000),
            'LocalesString': (5000, 7000),
            'LocalesPointer': (50000, 52000),
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
            'LocalesPointer': [],
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

# Funcion que se le da como parametro si es global, si es temporal, si es constante, 
# si se tiene falso en estas 3, entonces se le asigna uno local, despues se le da el valor del tipo y el tamaño #
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
            elif type == 'POINTER':
                memory_space = 'LocalesPointer'

        if memory_space is not None:
            start_address, end_address = self.memory_spaces[memory_space]  # Unpack the tuple
            self.memory_spaces[memory_space] = (start_address + size, end_address)  # Concatenate size as a tuple
            self.memory[memory_space] = [0] * size
            return start_address
        else:
            raise ValueError(f"Invalid memory type: {type}")
    
    # Funcion para obtener el tipo de la variable dado una direccion # 
    def getTypeFromAddress(self, address):
        if type(address) is tuple:
            address = address[0]
        if (1000 <= address < 3000) or (10000 <= address < 13000) or (20000 <= address < 23000) or (33000 <= address < 35000):
            return "INT"
        elif (3000 <= address < 5000) or (13000 <= address < 15000) or (23000 <= address < 25000) or (35000 <= address < 37000):
            return "FLOAT"
        elif (5000 <= address < 7000) or (15000 <= address < 17000) or (25000 <= address < 27000) or (37000 <= address < 40000):
            return "STRING"
        elif (7000 <= address < 9000) or (17000 <= address < 19000) or (27000 <= address < 29000) or (40000 <= address < 43000):
            return "BOOL"
        elif (30000 <= address < 33000) or (50000 <= address < 52000):
            return "POINTER"
        else:
            return "Unknown type"

# Stacks para guardar los quads y sus pilas, tambien se tiene un contador #
pilaTypes = []
pilaAddr = []
quads = []
contQuads = 0
pilaSaltos = []
mem = Memory()
is_global = True
paramsCall = []
paramsList = []
diccListas = {}

# Ejemplo de quads
# ("GOTOF", address, None, None)
# ("GOTOV", address, None, None)
# ("GOTO", address, None, None)
# ("", address, None, None)
# ("GOSUB", None, None, #quad)
# ("GOSUB", None, None, #quad)
# ("+", addressOp1, addressOp2, address)

# Clase de la tabla de variables #
class VariablesTable():
    def __init__(self):
        # Creacion de la tabla de variables en un diccionario #
        self.memoryTable = {}
        # Ejemplo:  
        # "memory": {
        # "v": 13000,
        # "y": 13001,
        # "j": 10000
        # }
    
    # Funcion que agrega variable al diccionario, se le da como parametro el id y su direccion de memoria #
    def addVarTable(self, variable_id, memory_address):
        if variable_id in self.memoryTable and memory_address: # se cambia o no el <>
            raise ValueError(f'The variable {variable_id} already exists')
        else:
            self.memoryTable[variable_id] = memory_address
    
    # Funcion que regresa la direccion del id, dando como parametro este mismo #
    def getVarAddress(self, variable_id):
        if variable_id not in self.memoryTable:
            raise ValueError(f'The variable {variable_id} does not exists')
        else:
            return self.memoryTable.get(variable_id)

    # Funcion que regresa el tipo de la variable, dando como parametro la direccion de memoria #
    def getTypeFromMemory(self, memory_address):
        return mem.getTypeFromAddress(memory_address)
    
    # Imprime la tabla de variables #
    def printVarTable(self):
        print(self.memoryTable)

varTable = VariablesTable()

# Tabla del cubo semantico #
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

# Funcion que regresa el tipo de la expresion # 
def lookup_semantic_cube(op, type1, type2):
    key = (op, type1, type2)
    if key in semantic_cube:
        return semantic_cube[key]
    else:
        return f"Error: No matching type for operator '{op}' and operand types '{type1}' and '{type2}'"


# Definicion de las reglas # 

# Como debe de estar la sintaxis del programa #
def p_program(p):
    '''program : PROGRAM ID SEMICOLON declaration_list function MAIN LPAREN mainRef RPAREN bloque SEMICOLON final debug dataObj'''

# Agrega valor de donde empieza el main #
def p_mainRef(p):
    '''mainRef :
    '''
    global contQuads
    varTable.addVarTable("MAIN", contQuads)

def p_final(p):
    '''final : 
    '''
    global contQuads
    quads.append(("END",None, None, None))
    contQuads += 1

# Imprime la tabla de variables #
def p_debug(p):
    '''debug : 
    '''
    varTable.printVarTable()
    print(quads)

# Pasa la memoria y la tabla a un archivo OBJ, en este caso un json #
def p_dataObj(p):
    '''dataObj : 
    '''
    data = {
        'quad' : quads,
        'memory' : varTable.memoryTable,
    }
    with open("info.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

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
    '''bloqueB : statement_list bloqueB
                | empty'''
    global is_global
    is_global = False
    

# Funciones
def p_function(p): 
    '''function : functionF function
                | empty'''

def p_functionF(p):
    '''functionF : FUNC idFunc LPAREN parameter_list RPAREN LBRACE statement_list RBRACE SEMICOLON terminaFunc'''

# Guarda el ID de la funcion y verifica # 
def p_idFunc(p):
    '''
    idFunc : ID
    '''
    global is_global, contQuads
    is_global = False
    id = p[1]
    if id not in varTable.memoryTable:
        addrs = mem.addMemory(is_global, False, False, 'POINTER', 1)
        varTable.addVarTable(id, contQuads)
    else:
        print(f"Error: Function with ID: '{id}' is already declared")

# Parametros para funcion #
def p_parameter_list(p):
    '''parameter_list : tipo ID COMMA parameter_list
                      | tipo ID
                      | empty'''
    if p[1] != None:
        paramsList.append(p[1].upper())

# Llama la funcion #
def p_callFunc(p):
    '''callFunc : ID LPAREN paramCall RPAREN checkParam SEMICOLON'''
    global contQuads
    if p[1] not in varTable.memoryTable:
        print(f"Error: Function with ID: '{p[1]}' is not declared")
    else:
        quads.append(("GOSUB", None, None, p[1]))
        contQuads += 1

def p_paramCall(p):
    '''paramCall : ID COMMA paramCall
                 | ID 
                 | empty'''
    if len(p) > 1:
        if p[1] not in varTable.memoryTable:
            print(f"Error: Function with ID: '{p[1]}' is not declared")
        else:
            addrs = varTable.getVarAddress(p[1])
            tipo = varTable.getTypeFromMemory(addrs)
            paramsCall.append(tipo)

def p_checkParam(p):
    '''checkParam :
    '''
    if len(paramsList) == len(paramsCall):
        for i in range(len(paramsCall)):
            if paramsList[i] != paramsCall[i]:
                raise ValueError("Error: call function doesn't match types")
    else:
        raise ValueError("Error: call function doesn't match length of function parameters")

def p_terminaFunc(p):
    '''terminaFunc :
    '''
    global contQuads
    quads.append(("ENDFunc",None, None, None))
    contQuads += 1

# Lista de estatutos #
def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# Posibles estatutos a realizar #
def p_statement(p):
    '''statement : declaration_list
                 | assignment_statement
                 | read_statement
                 | write_statement
                 | if_statement
                 | for_statement
                 | while_statement
                 | do_while_statement
                 | return_statement
                 | callFunc
                 | graph_function'''
    p[0] = p[1]

# Expresiones #
def p_expression(p):
    '''expression : exp1
                    | exp1 AND exp1
                    | exp1 OR exp1'''
    global contQuads
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '&&':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("&&", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address
        
    elif p[2] == '||':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("||", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address

def p_exp1(p):
    '''exp1 : exp
            | exp LT exp
            | exp GT exp
            | exp EQ exp
            | exp NEQ exp'''
    global contQuads
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '<':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("LT", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address

    elif p[2] == '>':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("GT", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address
    
    elif p[2] == '<=':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("LTE", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address

    elif p[2] == '>=':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("GTE", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address
    
    elif p[2] == '==':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("EQ", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address

    elif p[2] == '!=':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("NEQ", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address


def p_exp(p):
    '''exp : term 
             | term PLUS exp
             | term MINUS exp'''
    global contQuads
    if len(p) > 2:
        if p[1] is None or p[3] is None:
            raise ValueError('Invalid variable')
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '+':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("PLUS", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address

    elif p[2] == '-':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("MINUS", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address

def p_term(p):
    '''term : fact
         | fact TIMES term
         | fact DIVIDE term'''
    global contQuads
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == '*':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("TIMES", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address

    elif p[2] == '/':
        operator = p[2]
        op1 = p[1]
        op2 = p[3]
        op1type = varTable.getTypeFromMemory(op1).lower()
        op2type = varTable.getTypeFromMemory(op2).lower()
        temp_address = mem.addMemory(False, True, False, lookup_semantic_cube(operator, op1type, op2type), 1)
        quads.append(("DIVIDE", op1, op2, temp_address))
        contQuads += 1
        p[0] = temp_address

def p_fact(p):
    '''fact : dataId
            | CTEF addConst
            | CTEI addConst
            | CTESTRING addConst
            | LPAREN expression RPAREN'''
    if len(p) == 3:
        p[0] = p[2]
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]


# Añade el tipo de la constante a la pila
def p_addConst(p):
    '''addConst : 
    '''
    if p[-1] in varTable.memoryTable:
        temp = varTable.getVarAddress(p[-1])
        p[0] = temp
    else: 
        if isinstance(p[-1], float):
                t = mem.addMemory(False, False, True, 'FLOAT', 1)
                varTable.addVarTable(p[-1], t)
                p[0] = t
        elif isinstance(p[-1], int):
                t = mem.addMemory(False, False, True, 'INT', 1)
                varTable.addVarTable(p[-1], t)
                p[0] = t
        elif isinstance(p[-1], str):
                t = mem.addMemory(False, False, True, 'STRING', 1)
                varTable.addVarTable(p[-1], t)
                p[0] = t

# Lista de declaraciones # 
def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration'''

def p_declaration(p):
    '''declaration : tipo ID SEMICOLON
                    | tipo ID COMMA declarationD
                    | list_declaration'''
    if len(p) > 2:
        tipo = p[1]
        addrs = mem.addMemory(is_global, False, False, tipo, 1)
        varTable.addVarTable(p[2], addrs)

def p_declarationD(p):
    '''declarationD : ID COMMA declarationD
                    | ID SEMICOLON'''
    if len(p) > 4:
        tipo = pilaTypes.pop()
    else:
        tipo = pilaTypes[-1]

    addrs = mem.addMemory(is_global, False, False, tipo, 1)
    varTable.addVarTable(p[1], addrs)

# Declaracion de lista (array)  #
def p_list_declaration(p):
    '''list_declaration : tipo ID LBRACKET var RBRACKET SEMICOLON'''
    global contQuads, diccListas
    tipo = p[1]
    size = p[4]
    if p[2] not in varTable.memoryTable:
        addrs = mem.addMemory(is_global, False, False, tipo, size+1)
        varTable.addVarTable(p[2], addrs)
        diccListas[p[2]] = size
        quads.append(("DEC_ARR", addrs, None, size))
        contQuads += 1
    else:
        print(f"Error: '{p[2]}' is already declared")

def p_var(p):
    '''var : CTEI'''
    if p[1] < 0:
        raise ValueError(f"Error: Negative values not compatible '{p[1]}'")
    else:
        p[0] = p[1]
        if p[1] not in varTable.memoryTable:
            t = mem.addMemory(False, False, True, 'INT', 1)
            varTable.addVarTable(p[1], t)

# Declaracion de matriz # 
def p_matrix_declaration(p):
    '''matrix_declaration : tipo ID LBRACKET var RBRACKET LBRACKET var RBRACKET SEMICOLON'''
    tipo = p[1]
    size = p[4] * p[7]
    if p[2] not in varTable.memoryTable:
        addrs = mem.addMemory(is_global, False, False, tipo, size)
        varTable.addVarTable(p[2], addrs)
    else:
        print(f"Error: '{p[2]}' is already declared")

# Estatuto de asignacion #
def p_assignment_statement(p):
    '''assignment_statement : dataId ASSIGN exp SEMICOLON'''
    global contQuads
    if type(p[1]) is tuple or type(p[3]) is tuple: 
        quads.append(("ASSIGN", p[3], None, p[1]))
        contQuads += 1
    else:
        a = varTable.getTypeFromMemory(p[1])
        b = varTable.getTypeFromMemory(p[3])
        if a == b:
            quads.append(("ASSIGN", p[3], None, p[1]))
            contQuads += 1
            p[0] = p[1]
        else:
            raise ValueError(f"Error: Can't assign two different types '{p[1]}' , '{p[3]}'")

def p_dataId(p):
    '''dataId : ID
              | ID LBRACKET exp RBRACKET'''
    global contQuads, diccListas
    if p[1] in varTable.memoryTable:
        addrs = varTable.getVarAddress(p[1])
        print(addrs)
        if len(p) == 2:
            p[0] = addrs
        else:
            temp = diccListas[p[1]]
            lim2 = varTable.getVarAddress(temp)
            quads.append(("VER", p[3], 0, lim2))
            contQuads += 1   
            p[0] = (addrs, p[3], lim2)
    else:
        raise ValueError(f"Error: ID isn't declared '{p[1]}'")


# Estatuto leer datos # 
def p_read_statement(p):
    '''read_statement : READ LPAREN ID RPAREN SEMICOLON'''
    global contQuads
    if p[3] not in varTable.memoryTable:
        raise ValueError(f"Error: Variable isn't declared '{p[3]}'")
    else:
        addrs = varTable.getVarAddress(p[3])
        quads.append(("READ", None, None, addrs))
        contQuads += 1

# Impresión de datos
def p_write_statement(p):
    '''write_statement : WRITE LPAREN write_list RPAREN SEMICOLON'''

def p_write_list(p):
    '''write_list : write_item
                       | write_list COMMA write_item'''

def p_write_item(p):
    '''write_item : fact'''
    global contQuads
    quads.append(("WRITE", None, None, p[1]))
    contQuads += 1

# Condicion if y if-else # 

def p_if_statement(p):
    '''if_statement : IF LPAREN expression if2 RPAREN LBRACE statement_list RBRACE condif if3'''

def p_condif(p):
    '''condif : ELSE if4 LBRACE statement_list RBRACE SEMICOLON 
              | SEMICOLON'''

def p_if2(p):
    '''if2 : 
    '''
    global pilaSaltos, jumps, contQuads
    quads.append(("GOTOF", p[-1], None, None))
    pilaSaltos.append(contQuads)
    contQuads += 1

def p_if3(p):
    '''if3 : 
    '''
    global pilaSaltos, jumps, contQuads
    jumps = pilaSaltos.pop()
    last_quad = list(quads[jumps])  
    last_quad[3] = contQuads 
    quads[jumps] = tuple(last_quad)  

def p_if4(p):
    '''if4 : 
    '''
    global pilaSaltos, jumps, contQuads
    quads.append(("GOTO", None, None, None))
    jumps = pilaSaltos.pop()
    pilaSaltos.append(contQuads)
    contQuads += 1
    last_quad = list(quads[jumps]) 
    last_quad[3] = contQuads
    quads[jumps] = tuple(last_quad)  



# Condicion While #
def p_while_statement(p):
    '''while_statement : WHILE LPAREN while1 expression while2 RPAREN LBRACE statement_list RBRACE while3 SEMICOLON'''

def p_while1(p):
    '''while1 : 
    '''
    pilaSaltos.append(contQuads)

def p_while2(p):
    '''while2 : 
    '''
    global contQuads, pilaSaltos, jumps
    if varTable.getTypeFromMemory(p[-1]) != "BOOL" : 
        raise ValueError(f"Error: Type-Mismatch")
    else:
        quads.append(("GOTOF", p[-1], None, None))
        pilaSaltos.append(contQuads)
        contQuads += 1

def p_while3(p):
    '''while3 : 
    ''' 
    global contQuads, pilaSaltos
    temp = pilaSaltos.pop()
    temp2 = pilaSaltos.pop()
    quads.append(("GOTO", None, None, temp2))
    contQuads += 1
    last_quad = list(quads[temp])  
    last_quad[3] = contQuads
    quads[temp] = tuple(last_quad)  

# Condicion Do While #
def p_do_while_statement(p):
    '''do_while_statement : DO dowhile1 LBRACE statement_list RBRACE WHILE LPAREN expression dowhile2 RPAREN SEMICOLON'''

def p_dowhile1(p):
    '''dowhile1 : 
    '''
    global contQuads
    pilaSaltos.append(contQuads)

def p_dowhile2(p):
    '''dowhile2 : 
    '''
    global contQuads, pilaSaltos
    if varTable.getTypeFromMemory(p[-1]) != "BOOL" : 
        raise ValueError(f"Error: Type-Mismatch")
    else:
        quads.append(("GOTOV", p[-1], None, pilaSaltos.pop()))
        contQuads += 1

# Estatuto ciclo for # 
def p_for_statement(p):
    '''for_statement : FOR LPAREN assignment_statement for2 TO exp for3 RPAREN LBRACE statement_list RBRACE for4 SEMICOLON'''
    
def p_for2(p):
    '''for2 : 
    '''
    global pilaAddr
    pilaAddr.append(p[-1])

def p_for3(p):
    '''for3 : 
    ''' 
    global contQuads, pilaSaltos, jumps, pilaAddr
    t = pilaAddr[-1]
    temp_address = mem.addMemory(False, True, False, 'BOOL', 1)
    quads.append(("LTE", t, p[-1], temp_address))
    pilaSaltos.append(contQuads)
    quads.append(("GOTOF", temp_address, None, None))
    pilaSaltos.append(contQuads)
    contQuads += 2

def p_for4(p):
    '''for4 : 
    ''' 
    global contQuads, pilaSaltos, pilaAddr
    temp = pilaSaltos.pop()
    temp2 = pilaSaltos.pop()
    temp_address = mem.addMemory(False, True, False, 'INT', 1)
    quads.append(("PLUS", pilaAddr[-1], 1, temp_address))
    quads.append(("ASSIGN", temp_address, None, pilaAddr[-1]))
    quads.append(("GOTO", None, None, temp2))
    contQuads += 3
    last_quad = list(quads[temp+1])  
    last_quad[3] = contQuads
    quads[temp+1] = tuple(last_quad) 
    
# Estatuto return de funcion # 
def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('RETURN', p[2])

def p_graph_function(p):
    '''graph_function : OPEN LPAREN RPAREN SEMICOLON
                      | END LPAREN RPAREN SEMICOLON
                      | PENDOWN LPAREN RPAREN SEMICOLON
                      | PENUP LPAREN RPAREN SEMICOLON'''
    global contQuads
    quads.append(("TURTLE", None, None, p[1]))
    contQuads += 1

def p_graph_function2(p):
    '''graph_function : FORWARD LPAREN exp RPAREN SEMICOLON
                      | BACKWARD LPAREN exp RPAREN SEMICOLON
                      | LEFT LPAREN exp RPAREN SEMICOLON
                      | RIGHT LPAREN exp RPAREN SEMICOLON
                      | SPEED LPAREN exp RPAREN SEMICOLON
                      | PENSIZE LPAREN exp RPAREN SEMICOLON
                      | CIRCLE LPAREN exp RPAREN SEMICOLON'''
    global contQuads
    quads.append(("TURTLE", p[3], None, p[1]))
    contQuads += 1

# Pasa el empty # 
def p_empty(p):
    '''empty : '''
    p[0] = None

# Imprime si hay algun error # 
def p_error(p):
    if p:
        print("Syntax error at token {}, line {}".format(p.value, p.lineno))
    else:
        print("Syntax error at EOF") 

parser = yacc.yacc()

if __name__ == '__main__':
    if(len(sys.argv) > 1):
            file = sys.argv[1]
            try:
                f = open(file, 'r')
                data = f.read()
                f.close()
                if (yacc.parse(data, tracking=True) == "PROGRAM COMPILED"):
                    print("Valid Syntaxis")
            except EOFError:
                print(EOFError)
    else:
        print("Error: File doesn't exist")



