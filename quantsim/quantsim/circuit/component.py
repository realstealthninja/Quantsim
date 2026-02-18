from abc import ABC, abstractmethod



class Component(ABC):
    """A Base class representing a component in a quantum circuit"""
    inputs: list[Component] | None
    outputs: list[Component] | None
    id: str = ""

    def __init__(self, inputs: list[Component] | None, outputs: list[Component] | None):
        self.inputs = inputs 
        self.outputs = outputs

    def add_input(self, comp: Component) -> None:
        if self.inputs is not None and comp.outputs is not None:
            self.inputs.append(comp)
            comp.outputs.append(self)
        else:
            raise NotImplementedError()

    def add_output(self, comp: Component) -> None:
        if self.outputs is not None and comp.inputs is not None:
            self.outputs.append(comp)
            comp.inputs.append(self)
        else:
            raise NotImplementedError()




