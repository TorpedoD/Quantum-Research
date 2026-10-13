
from qiskit import QuantumCircuit

# Create a circuit with 2 qubits
qc = QuantumCircuit(2)

# Apply a Hadamard gate to qubit 0
qc.h(0)

# Apply CNOT: qubit 0 controls qubit 1
qc.cx(0, 1)

# Print the circuit
print(qc.draw())
