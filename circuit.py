import numpy as np

class Circuit:
    def __init__(self):
        self.nodes = {}
        self.components = []

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = len(self.nodes)

    def add_component(self, component):
        self.add_node(component.node1)
        self.add_node(component.node2)
        self.components.append(component)

class Resistor:
    def __init__(self, node1, node2, value):
        self.node1 = node1
        self.node2 = node2
        self.value = value

class Capacitor:
    def __init__(self, node1, node2, value):
        self.node1 = node1
        self.node2 = node2
        self.value = value

class Inductor:
    def __init__(self, node1, node2, value):
        self.node1 = node1
        self.node2 = node2
        self.value = value

class VoltageSource:
    def __init__(self, node1, node2, value):
        self.node1 = node1
        self.node2 = node2
        self.value = value

class CurrentSource:
    def __init__(self, node1, node2, value):
        self.node1 = node1
        self.node2 = node2
        self.value = value

def modified_nodal_analysis(circuit, frequency):
    n = len(circuit.nodes)
    A = np.zeros((n, n), dtype=complex)
    Z = np.zeros(n, dtype=complex)

    omega = 2 * np.pi * frequency

    for component in circuit.components:
        idx1 = circuit.nodes[component.node1]
        idx2 = circuit.nodes[component.node2]

        if isinstance(component, Resistor):
            value = component.value
            y = 1 / value

        elif isinstance(component, Capacitor):
            value = component.value
            y = 1j * omega * value

        elif isinstance(component, Inductor):
            value = component.value
            y = -1j / (omega * value)

        elif isinstance(component, VoltageSource):
            value = component.value
            Z[idx1] -= value
            continue

        elif isinstance(component, CurrentSource):
            value = component.value
            Z[idx1] += value
            Z[idx2] -= value
            continue

        A[idx1, idx1] += y
        A[idx2, idx2] += y
        A[idx1, idx2] -= y
        A[idx2, idx1] -= y

    return np.linalg.solve(A, Z)

def main():
    circuit = Circuit()
    circuit.add_component(Resistor('1', '0', 1e3))
    circuit.add_component(Capacitor('1', '2', 1e-6))
    circuit.add_component(Inductor('2', '0', 1e-3))
    circuit.add_component(VoltageSource('1', '0', 5))
    circuit.add_component(CurrentSource('2', '0', 1e-3))

    frequency = 60  # Test frequency in Hz
    node_voltages = modified_nodal_analysis(circuit, frequency)
    print("Node voltages at {} Hz:".format(frequency))
    for node, voltage in zip(circuit.nodes, node_voltages):
        print("Node {}: {:.2f} + {:.2f}j".format(node, voltage.real, voltage.imag))

if __name__ == "__main__":
    main()