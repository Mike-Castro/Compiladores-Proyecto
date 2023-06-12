import json
import turtle
import time


class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.heap = {}
        self.variables = {}
        self.varTable = {}
        self.quads = []
        self.quad_pointer = 0
        self.varAddress = {}
        self.localMemory = {}
        self.stackCall = []

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

    # Funcion busca el valor para regresar el tipo#
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
            return tipo
        elif (7000 <= valor < 9000) or (17000 <= valor < 19000) or (27000 <= valor < 29000) or (40000 <= valor < 43000):
            return int(tipo)
        elif (30000 <= valor < 33000) or (50000 <= valor < 52000):
            return "POINTER"
        else:
            return "Unknown type"
        

    # Guardar en la VM las variables  #

    def loadOBJ(self, filename):
        quads = []
        memory = {}
        with open(filename, 'r') as file:
            data = json.load(file)
            quads_data = data.get("quad")
            memory_data = data.get("memory")
            if quads_data is not None:
                quads = quads_data
            if memory_data is not None:
                memory = memory_data
        return quads, memory

    # Correr la virtual machine # 
    def run(self, quads, memory):
        self.quads = quads
        self.memory = memory
        for key, value in memory.items():
            if key == "MAIN":
                self.quad_pointer = int(value)
        # While de contadores, con sus operaciones #
        while self.quad_pointer < len(self.quads):
            opcode = self.quads[self.quad_pointer][0]
            op1 = self.quads[self.quad_pointer][1]
            op2 = self.quads[self.quad_pointer][2]
            op3 = self.quads[self.quad_pointer][3]
            if opcode == "PLUS":
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
            elif opcode == "TIMES":
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
            elif opcode == "MINUS":
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
            elif opcode == "DIVIDE":
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
            elif opcode == "WRITE":
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
            elif opcode == "READ":
                inp = input()
                self.localMemory[op3] = inp
                self.quad_pointer += 1
            elif opcode == "ASSIGN":
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
            elif opcode == "LT":
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
            elif opcode == "GT":
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
            elif opcode == "GTE":
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
            elif opcode == "LTE":
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
            elif opcode == "EQ":
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
            elif opcode == "NEQ":
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
            elif opcode == "GOTO":
                point = int(op3)
                self.quad_pointer = point 
            elif opcode == "GOTOV":
                a = vm.getKey(self.memory, op1)
                if a != 0:
                    point = int(op3)
                    self.quad_pointer = point
                else:
                    self.quad_pointer += 1
            elif opcode == "GOTOF":
                a = vm.getKey(self.memory, op1)
                if a == 0:
                    point = int(op3)
                    self.quad_pointer = point
                else:
                    self.quad_pointer += 1
            elif opcode == "GOSUB":
                temp = self.quad_pointer + 1
                for key, value in memory.items():
                    if key == op3:
                        go = int(value)
                self.quad_pointer = go
            elif opcode == "TURTLE":
                if op1 != None:
                    a = vm.getKey(self.memory, op1)
                    vm.turtleGraphics(op3.upper(), a)
                else:
                    vm.turtleGraphics(op3.upper(), None)
                
                self.quad_pointer += 1
            elif opcode == "DEC_ARR":
                for x in range(op3):
                    self.localMemory[op1+x+1] = 0
                self.quad_pointer += 1
            elif opcode == "VER":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op3)
                if a < op2 or a >= b:
                    raise ValueError("Error: index out of range")
                self.quad_pointer += 1
            elif opcode == "END":
                print("\n------------------") 
                print("Fin del Programa")
                break
            elif opcode == "ENDFunc":
                self.quad_pointer = temp
            else:
                break

vm = VirtualMachine()
obj_file = 'info.json'
print("------------------") 
print("   Ejecución")
print("------------------\n")
quads, memory = vm.loadOBJ(obj_file)
vm.run(quads, memory)