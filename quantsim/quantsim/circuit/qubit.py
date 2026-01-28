from quantsim.qubit import Qubit
from .component import Component

class QubitComponent(Component):
    qubit: Qubit
    def __init__(self, outputs: list[Component]):
        super().__init__(None, outputs)
        self.qubit = Qubit()



