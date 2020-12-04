import operator

class IntCodeComputer:
    def __init__(self):
        self.instruction_pointer = None
        self.relative_base = None
        self.buffer = []
    
    def load(self, inpt, extra_buffer=0):
        self.buffer.clear()
        self.relative_base = 0
        self.instruction_pointer = 0
            
        if isinstance(inpt, str):
            inpt = (int(e) for e in  inpt.split(','))
        self.buffer.extend(list(inpt))
        
        if extra_buffer == 'auto':
            extra_buffer = 10*len(self.buffer)
        if extra_buffer:
            self.buffer.extend([0]*extra_buffer)
        
    def _get_index_pmode(self, value, pmode):
        if pmode == 0: #position mode
            return self.buffer[value]
        elif pmode == 1: # immediate mode
            return value
        elif pmode == 2: #relative mode
            return self.buffer[value] + self.relative_base
        else:
            raise ValueError(f'invalid pmode: {pmode}')
        
    def execute_one(self, inpt=None, outputs=None):
        opcode = self.buffer[self.instruction_pointer]
        pmodes = [int(char) for char in '{:03}'.format(opcode//100)][::-1]  # reversed to be in parameter order
        opcode = opcode % 100
        
        if opcode == 1: #add 
            self._do_operation(operator.add, pmodes)
            
        elif opcode == 2: #mul
            self._do_operation(operator.mul, pmodes)
            
        elif opcode == 3: #input
            if inpt is None:
                inpt = int(input('input:'))
            self.buffer[self._get_index_pmode(self.instruction_pointer+1, pmodes[0])] = inpt
            self.instruction_pointer += 2
            return 'usedinput'
        
        elif opcode == 4: #output
            output = self.buffer[self._get_index_pmode(self.instruction_pointer+1, pmodes[0])]
            if outputs is None:
                print('Output', output)
            else:
                outputs.append(output)
            self.instruction_pointer += 2
            
        elif opcode == 5:  # jump-if-true
            totest = self.buffer[self._get_index_pmode(self.instruction_pointer+1, pmodes[0])]
            if totest != 0:
                self.instruction_pointer = self.buffer[self._get_index_pmode(self.instruction_pointer+2, pmodes[1])]
            else:
                self.instruction_pointer += 3
            
        elif opcode == 6:  # jump-if-false
            totest = self.buffer[self._get_index_pmode(self.instruction_pointer+1, pmodes[0])]
            if totest == 0:
                self.instruction_pointer = self.buffer[self._get_index_pmode(self.instruction_pointer+2, pmodes[1])]
            else:
                self.instruction_pointer += 3
            
        elif opcode == 7:  # less than
            self._do_operation(operator.lt, pmodes)
            
        elif opcode == 8:  # equal to
            self._do_operation(operator.eq, pmodes)
            
        elif opcode == 9:  # adjust relative base
            self.relative_base += self.buffer[self._get_index_pmode(self.instruction_pointer+1, pmodes[0])]
            self.instruction_pointer += 2
            
        elif opcode == 99: #halt
            raise StopIteration(99)
            
        else:
            raise ValueError(f'invalid opcode {opcode}')
    
    def _do_operation(self, op, pmodes):
        # op should take 2 inputs and give one output
        operand1 = self.buffer[self._get_index_pmode(self.instruction_pointer+1, pmodes[0])]
        operand2 = self.buffer[self._get_index_pmode(self.instruction_pointer+2, pmodes[1])]
        self.buffer[self._get_index_pmode(self.instruction_pointer+3, pmodes[2])] = int(op(operand1, operand2))
        self.instruction_pointer += 4
        
    def execute_to_halt(self, limit=None, inputs=None, outputs=None):
        if inputs is None:
            inputs  = []
        else:
            inputs = list(inputs)
        inputs.append(None)
        i_input = 0
        
        i = 0
        while limit is None or i < limit:
            try:
                inpt = inputs[i_input]
                if self.execute_one(inpt, outputs) == 'usedinput':
                    i_input += 1
                    inputs.append(None)
                i += 1
            except StopIteration as si:
                if si.args[0] == 99:
                    break
                else:
                    raise
        
        return i
