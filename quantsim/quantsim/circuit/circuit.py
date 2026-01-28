from quantsim.circuit.observer import Observer
from quantsim.circuit.qubit import QubitComponent
from .component import Component

class Circuit:
    qubits: list[QubitComponent] = []
    observers: list[Observer] = []

    # wires and gates
    components: list[Component] = []

    def add(self, component: Component):
        self.components.append(component)

    def clear(self,

    def remove(self, component: Component):
        for i in range(len(self.components)):
            if component is self.components[i]:
                _ = self.components.pop(i)



    def calculate(self):
        """ Sets value to observables if they exist by back tracking """

