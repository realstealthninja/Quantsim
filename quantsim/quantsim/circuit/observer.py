from .component import Component


class Observer(Component):
    value: bool
    
    def __init__(self, inputs: list[Component]) -> None:
        super().__init__(inputs, None)


    