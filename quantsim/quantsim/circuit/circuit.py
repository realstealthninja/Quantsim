from numpy import matrix
from quantsim.circuit.observer import Observer
from quantsim.circuit.qubit import QubitComponent
from quantsim.quantsim.circuit.gate import GateComponent
from quantsim.quantsim.core.qubit import Qubit
from .component import Component

class Circuit:
    qubits: list[QubitComponent] = []
    observers: list[Observer] = []

    # wires and gates
    components: list[Component] = []

    def add(self, component: Component):
        self.components.append(component)

    def clear(self): 
        self.qubits.clear()
        self.observers.clear()
        self.components.clear()

    def remove(self, component: Component):
        for i in range(len(self.components)):
            if component is self.components[i]:
                _ = self.components.pop(i)



    def calculate(self):
        """ Sets value to observables by back tracking"""
        for qubit in self.qubits:
            gates: list[GateComponent] = []
            observer: Observer | None = None
            if qubit.outputs:
                for component in qubit.outputs:
                    if isinstance(component, GateComponent):
                        gates.append(component)
                    elif isinstance(component, Observer):
                        observer = component
                    else: 
                        continue
        
            # reverse direction
            gates = gates[::-1]
            endmat: matrix = gates.pop().gate.__array__()
            for gate in gates:
                endmat *= gate
            
            qubit_mat= endmat * qubit.qubit 
            qubit = Qubit(alpha=qubit_mat[0][0], beta=qubit_mat[1][0])
            if observer:
                observer.value = qubit.observe()
            

        

