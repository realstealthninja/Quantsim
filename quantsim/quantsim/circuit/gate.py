from ..gates.gate import QuantumGate
from .component import Component

class GateComponent(Component):
    gate: QuantumGate 

    def __init__(self, gate: QuantumGate, inputs: list[Component], outputs: list[Component])-> None:
        super().__init__(inputs, outputs)
        self.gate = gate

    
    def __array__(self):
        return self.gate.__array__()
    
    def __mul__(self, rhs):
        return self.gate.__mul__(rhs)