import json
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

    # Funcion para regresar el tipo de valor #
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
        print(self.memory)
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
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a + b
                self.localMemory[op3] = result
                self.quad_pointer += 1
            elif opcode == "TIMES":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a * b
                self.localMemory[op3] = result
                self.quad_pointer += 1
            elif opcode == "MINUS":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a - b
                self.localMemory[op3] = result
                self.quad_pointer += 1
            elif opcode == "DIVIDE":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a / b
                self.quad_pointer += 1
                self.localMemory[op3] = result
            elif opcode == "WRITE":
                value = self.getKey(self.memory, op3)
                print(value)
                self.quad_pointer += 1
            elif opcode == "READ":
                inp = input(f"Enter value: ")
                self.localMemory[op3] = inp
                self.quad_pointer += 1
            elif opcode == "ASSIGN":
                value = self.getKey(self.memory, op1)
                self.localMemory[op3] = value
                self.quad_pointer += 1
            elif opcode == "LT":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a < b
                self.localMemory[op3] = result
                self.quad_pointer += 1
            elif opcode == "GT":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a > b
                self.localMemory[op3] = result
                self.quad_pointer += 1
            elif opcode == "GTE":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a >= b
                self.localMemory[op3] = result
                self.quad_pointer += 1
            elif opcode == "LTE":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a <= b
                self.localMemory[op3] = result
                self.quad_pointer += 1
            elif opcode == "EQ":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a == b
                self.localMemory[op3] = result
                self.quad_pointer += 1
            elif opcode == "NEQ":
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
            elif opcode == "END":
                print("Final del programa")
                break
            elif opcode == "ENDFunc":
                self.quad_pointer = temp
            else:
                break

    def find_label(self, label):
        for i, quad in enumerate(self.quads):
            if quad[0] == "LABEL" and quad[1] == label:
                return i
        raise Exception(f"Label '{label}' not found")


vm = VirtualMachine()
obj_file = 'info.json'
quads, memory = vm.loadOBJ(obj_file)
vm.run(quads, memory)