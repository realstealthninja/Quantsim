
from abc import ABC, abstractmethod


class Component(ABC):
    """A Base class representing a component in a quantum circuit"""
    inputs: list[Component] | None
    outputs: list[Component] | None
    id: str = ""

    def __init__(self, inputs: list[Component] | None, outputs: list[Component] | None):
        self.inputs = inputs 
        self.outputs = outputs



