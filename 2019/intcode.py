import operator

class IntCodeComputer:
    def __init__(self):
        self.instruction_pointer = None
        self.buffer = []
    
    def load(self, inpt):
        self.buffer.clear()
            
        if isinstance(inpt, str):
            inpt = (int(e) for e in  inpt.split(','))
        self.buffer.extend(list(inpt))
        self.instruction_pointer = 0
        
    def execute_one(self):
        opcode = self.buffer[self.instruction_pointer]
        if opcode == 1:
            self._do_operation(operator.add)
        elif opcode == 2:
            self._do_operation(operator.mul)
        elif opcode == 99:
            raise StopIteration(99)
        else:
            raise ValueError(f'invalid opcode {opcode}')
            
        self.instruction_pointer += 4
    
    def _do_operation(self, op):
        # op should take 2 inputs and give one output
        operand1 = self.buffer[self.buffer[self.instruction_pointer+1]]
        operand2 = self.buffer[self.buffer[self.instruction_pointer+2]]
        self.buffer[self.buffer[self.instruction_pointer+3]] = op(operand1, operand2)
        
    def execute_to_halt(self, limit=None):
        i = 0
        while limit is None or i < limit:
            try:
                self.execute_one()
                i += 1
            except StopIteration as si:
                if si.args[0] == 99:
                    break
                else:
                    raise
        
        return i