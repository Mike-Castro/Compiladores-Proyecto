import numpy as np

class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.heap = {}
        self.variables = {}
        self.varTable = {}
        self.quads = []
        self.quad_pointer = 0
        self.varAddress = {}
    # Guardar en la VM las variables  #

    def loadOBJ(filename):
        quads = []
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(' ')
                opcode = parts[0]
                op1 = parts[1] 
                op2 = parts[2] 
                result = parts[3]
                quads.append((opcode, op1, op2, result))
        return quads

    # Correr la virtual machine # 
    def run(self):
        self.quad_pointer = 0
        self.memory_addresses = {}

        while self.quad_pointer < len(self.quads):
            quad = self.quads[self.quad_pointer]
            opcode = quad[0]
            if opcode == "ADD":
                if len(self.stack) < 2:
                    raise Exception("Stack has less than 2 values")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif opcode == "MULTIPLY":
                if len(self.stack) < 2:
                    raise Exception("Stack has less than 2 values")
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
            elif opcode == "SUBTRACT":
                if len(self.stack) < 2:
                    raise Exception("Stack has less than 2 values")
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a - b)
            elif opcode == "DIVIDE":
                if len(self.stack) < 2:
                    raise Exception("Stack has less than 2 values")
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a / b)
            elif opcode == "PRINT":
                if len(self.stack) == 0:
                    raise Exception("Stack is empty")
                value = self.stack.pop()
                print(value)
            elif opcode == "READ":
                variable = quad[1]
                value = input(f"Enter a value for '{variable}': ")
                self.variables[variable] = value
            elif opcode == "ASSIGN":
                value = self.stack.pop()
                address = self.stack.pop()
                index = int(self.stack.pop())
                self.heap[address][index] = value
            elif opcode == "IF":
                condition = self.stack.pop()
                if not condition:
                    self.quad_pointer += 1
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
                condition = self.stack.pop()
                label = quad[1]
                if not condition:
                    self.quad_pointer = self.find_label(label)
                    continue
            elif opcode == "PARAM":
                variable = quad[1]
                value = self.variables[variable]
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
obj_file = 'file'
quads = vm.loadOBJ(obj_file)
vm.execute(quads)