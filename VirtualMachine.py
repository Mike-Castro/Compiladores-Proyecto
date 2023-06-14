import json
import turtle
import time
class VirtualMachine:
    def __init__(self):
        self.quads = []
        self.quad_pointer = 0
        self.localMemory = {}
        self.stackCall = []
        self.params = []

# Funcion para desplegar y hacer los cambios de las graficas #
    def turtleGraphics(self, nameF, value):
        if nameF == "OPEN":
            global t
            t = turtle.Turtle()
        elif nameF == "END":
            turtle.done()
        elif nameF == "PENUP":
            t.penup()
        elif nameF == "PENDOWN":
            t.pendown()
        elif nameF == "FORWARD":
            t.forward(value)
        elif nameF == "BACKWARD":
            t.backward(value)
        elif nameF == "LEFT":
            t.left(value)
        elif nameF == "RIGHT":
            t.right(value)
        elif nameF == "SPEED":
            t.speed(value)
        elif nameF == "PENSIZE":
            t.pensize(value)
        elif nameF == "CIRCLE":
            t.circle(value)

    # Funcion busca el valor en el diccionario de la memoria local, si no esta busca en la tabla de variables 
    # para regresar el tipo #
    def getKey(self, dictionary, valor):
        if valor in self.localMemory:
            tipo = self.localMemory.get(valor)
        else:
            for key, value in dictionary.items():
                if value == valor:
                    tipo = key

        if (1000 <= valor < 3000) or (10000 <= valor < 13000) or (20000 <= valor < 23000) or (33000 <= valor < 35000):
            return int(tipo)
        elif (3000 <= valor < 5000) or (13000 <= valor < 15000) or (23000 <= valor < 25000) or (35000 <= valor < 37000):
            return float(tipo)
        elif (5000 <= valor < 7000) or (15000 <= valor < 17000) or (25000 <= valor < 27000) or (37000 <= valor < 40000):
            return tipo.strip('"')
        elif (7000 <= valor < 9000) or (17000 <= valor < 19000) or (27000 <= valor < 29000) or (40000 <= valor < 43000):
            return int(tipo)
        elif (30000 <= valor < 33000) or (50000 <= valor < 52000):
            return "POINTER"
        else:
            return "Unknown type"
        

    # Guardar en la VM las variables, los quads y el dicc de parametros #
    def loadOBJ(self, filename):
        quads = []
        memory = {}
        paramsListId = {}
        with open(filename, 'r') as file:
            data = json.load(file)
            quads_data = data.get("quad")
            memory_data = data.get("memory")
            paramsListId = data.get("paramsListId")
            if quads_data is not None:
                quads = quads_data
            if memory_data is not None:
                memory = memory_data
        return quads, memory, paramsListId

    # Correr la virtual machine # 
    def run(self, quads, memory, paramsListID):
        self.quads = quads
        self.memory = memory
        for key, value in memory.items():
            if key == "MAIN":                       # Busca el main para empezar desde esa posicion de quad 
                self.quad_pointer = int(value)
        # While de contadores, con sus operaciones #
        while self.quad_pointer < len(self.quads):
            opcode = self.quads[self.quad_pointer][0]
            op1 = self.quads[self.quad_pointer][1]
            op2 = self.quads[self.quad_pointer][2]
            op3 = self.quads[self.quad_pointer][3]
            if opcode == "PLUS": # Clave para guardar el resultado de +
                if(op2) < 2:
                    a = vm.getKey(self.memory, op1)
                    result = a + op2
                    self.localMemory[op3] = result
                    self.quad_pointer += 1
                else:
                    if type(op2) is list:
                        if type(op1) is list:
                            a = self.getKey(self.memory, op1[1])
                            sum = a + op1[0]
                            resul = self.getKey(self.memory, sum)
                            b = self.getKey(self.memory, op2[1])
                            sum2 = b + op2[0]
                            resul2 = self.getKey(self.memory, sum2)
                            final = resul + resul2
                            self.localMemory[op3] = final
                        else:
                            a = self.getKey(self.memory, op2[1])
                            sum = a + op2[0]
                            resul = self.getKey(self.memory, sum)
                            b = self.getKey(self.memory, op1)
                            final = b + resul
                            self.localMemory[op3] = final
                        self.quad_pointer += 1
                    else:
                        if type(op1) is list:
                            a = self.getKey(self.memory, op1[1])
                            sum = a + op1[0]
                            resul = self.getKey(self.memory, sum)
                            b = vm.getKey(self.memory, op2)
                            final = resul + b
                            self.localMemory[op3] = final
                        else:
                            a = vm.getKey(self.memory, op1)
                            b = vm.getKey(self.memory, op2)
                            result = a + b
                            self.localMemory[op3] = result
                        self.quad_pointer += 1
            elif opcode == "TIMES": # Clave para guardar el resultado de *
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul * resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b * resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul * b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a * b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "MINUS": # Clave para guardar el resultado de -
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul - resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b - resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul - b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a - b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "DIVIDE": # Clave para guardar el resultado de /
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul / resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b / resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul / b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a / b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "WRITE": # Clave para imprimir datos
                if type(op3) is list:
                    a = self.getKey(self.memory, op3[1])
                    resultadd = a + op3[0]
                    value = self.localMemory[resultadd]
                    print(value)
                    self.quad_pointer += 1
                else:
                    value = self.getKey(self.memory, op3)
                    print(value)
                    self.quad_pointer += 1
            elif opcode == "READ": # Clave para leer datos
                inp = input()
                self.localMemory[op3] = inp
                self.quad_pointer += 1
            elif opcode == "PARAM": # Clave para guardar los parametros en el stack
                address = op1
                self.params.append(address)
                self.quad_pointer += 1
            elif opcode == "ASSIGN": # Clave para asignar resultados a sus variables
                if type(op3) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op3[1])
                        resul2 = b + op3[0]
                        self.localMemory[resul2] = resul
                    else:
                        value = self.getKey(self.memory, op1)
                        a = self.getKey(self.memory, op3[1])
                        resultadd = a + op3[0]
                        self.localMemory[resultadd] = value
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        self.localMemory[op3] = resul
                    else:
                        value = self.getKey(self.memory, op1)
                        self.localMemory[op3] = value
                    self.quad_pointer += 1
            elif opcode == "LT": # Clave para guardar el resultado de <
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul < resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b < resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul < b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a < b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "GT": # Clave para guardar el resultado de >
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul > resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b > resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul > b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a > b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "GTE": # Clave para guardar el resultado de >=
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul >= resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b >= resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul >= b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a >= b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "LTE": # Clave para guardar el resultado de <=
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul <= resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b <= resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul <= b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a <= b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "EQ": # Clave para guardar el resultado de ==
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul == resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b == resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul == b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a == b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "NEQ": # Clave para guardar el resultado de !=
                if type(op2) is list:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op2[1])
                        sum2 = b + op2[0]
                        resul2 = self.getKey(self.memory, sum2)
                        final = resul != resul2
                        self.localMemory[op3] = final
                    else:
                        a = self.getKey(self.memory, op2[1])
                        sum = a + op2[0]
                        resul = self.getKey(self.memory, sum)
                        b = self.getKey(self.memory, op1)
                        final = b != resul
                        self.localMemory[op3] = final
                    self.quad_pointer += 1
                else:
                    if type(op1) is list:
                        a = self.getKey(self.memory, op1[1])
                        sum = a + op1[0]
                        resul = self.getKey(self.memory, sum)
                        b = vm.getKey(self.memory, op2)
                        final = resul != b
                        self.localMemory[op3] = final
                    else:
                        a = vm.getKey(self.memory, op1)
                        b = vm.getKey(self.memory, op2)
                        result = a != b
                        self.localMemory[op3] = result
                    self.quad_pointer += 1
            elif opcode == "GOTO":   # Hace que el pointer se vaya a donde esta apuntando el goto
                point = int(op3)
                self.quad_pointer = point 
            elif opcode == "GOTOV":     # Verifica que sea verdadero la expresion para poder ir al quad designado
                a = vm.getKey(self.memory, op1)
                if a != 0:
                    point = int(op3)
                    self.quad_pointer = point
                else:
                    self.quad_pointer += 1
            elif opcode == "GOTOF": # Verifica que la expresion sea falsa para poder ir al quad designado
                a = vm.getKey(self.memory, op1)
                if a == 0:
                    point = int(op3)
                    self.quad_pointer = point
                else:
                    self.quad_pointer += 1
            elif opcode == "GOSUB": # Guarda el quad de donde esta ubicado para despues regresarse al ir a la función
                self.stackCall.append((self.quad_pointer + 1, self.localMemory))
                i = 0
                for param in self.params:
                    self.localMemory[paramsListID[op3][i][1]] = self.getKey(self.memory, param)
                    i = i+1
                self.params = []
                for key, value in memory.items():
                    if key == op3:
                        go = int(value)
                self.quad_pointer = go
            elif opcode == "TURTLE": # Clave para mandar a las funciones los valores para generar la grafica
                if op1 != None:
                    a = vm.getKey(self.memory, op1)
                    vm.turtleGraphics(op3.upper(), a)
                else:
                    vm.turtleGraphics(op3.upper(), None)
                
                self.quad_pointer += 1
            elif opcode == "DEC_ARR": # Clave para guardar en la memoria local la lista y asignarle valor inicial de 0
                for x in range(op3):
                    self.localMemory[op1+x+1] = 0
                self.quad_pointer += 1
            elif opcode == "VER": # Clave para verificar que el rango que se usa para la lista este dentro del rango
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op3)
                if a < op2 or a >= b:
                    raise ValueError("Error: index out of range")
                self.quad_pointer += 1
            elif opcode == "END": 
                print("\n------------------") 
                print("Fin del Programa")
                break
            elif opcode == "ENDFunc": # Clave para regresarse al quad en donde se llamo la función
                pop = self.stackCall.pop()
                self.quad_pointer = pop[0]
                self.localMemory = pop[1]
            else:
                break

vm = VirtualMachine()
obj_file = 'info.json'
print("------------------") 
print("   Ejecución")
print("------------------\n")
quads, memory, paramsListID = vm.loadOBJ(obj_file)
vm.run(quads, memory, paramsListID)