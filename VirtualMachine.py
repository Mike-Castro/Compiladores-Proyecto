import json

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
        
    def getKey(self, dictionary, valor):
        if valor in self.localMemory:
            return self.localMemory.get(valor)
        else:
            for key, value in dictionary.items():
                if value == valor:
                    try:
                        key = int(key)
                        return key
                    except ValueError:
                        pass
                    try:
                        key = float(key)
                        return key
                    except ValueError:
                        pass
                    return key
        return valor

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
        self.quad_pointer = 0
        while self.quad_pointer < len(self.quads):
            opcode = self.quads[self.quad_pointer][0]
            op1 = self.quads[self.quad_pointer][1]
            op2 = self.quads[self.quad_pointer][2]
            op3 = self.quads[self.quad_pointer][3]
            if opcode == "PLUS":
                print(op1, op2, 'x')
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                print(a, b, 'x')
                result = a + b
                self.localMemory[op3] = result
            elif opcode == "TIMES":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a * b
                self.localMemory[op3] = result
            elif opcode == "MINUS":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a - b
                self.localMemory[op3] = result
            elif opcode == "DIVIDE":
                a = vm.getKey(self.memory, op1)
                b = vm.getKey(self.memory, op2)
                result = a / b
                self.localMemory[op3] = result
            elif opcode == "WRITE":
                value = self.getKey(self.memory, op3)
                print(value)
            elif opcode == "READ":
                inp = input(f"Enter value: ")
                self.localMemory[op3] = inp
            elif opcode == "ASSIGN":
                value = self.getKey(self.memory, op1)
                self.localMemory[op3] = value
                print(self.localMemory)
            elif opcode == "GOTO":
                label = quad[1]
                self.quad_pointer = self.find_label(label)
                continue
            elif opcode == "GOTOV":
                condition = self.stack.pop()
                label = quad[1]
                if condition:
                    self.quad_pointer = self.find_label(label)
                    continue
            elif opcode == "GOTOF":
                label = quad[1]
                if not condition:
                    self.quad_pointer = self.find_label(label)
                    continue
            elif opcode == "PARAM":
                self.stack.append(value)
            elif opcode == "END":
                break

            self.quad_pointer += 1

    def find_label(self, label):
        for i, quad in enumerate(self.quads):
            if quad[0] == "LABEL" and quad[1] == label:
                return i
        raise Exception(f"Label '{label}' not found")


vm = VirtualMachine()
obj_file = 'info.json'
quads, memory = vm.loadOBJ(obj_file)
vm.run(quads, memory)