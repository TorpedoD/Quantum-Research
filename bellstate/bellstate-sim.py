
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create the quantum circuit
qc = QuantumCircuit(2)

# Prepare the Bell state
qc.h(0)
qc.cx(0, 1)

# Inspect the quantum state before measurement
print("Quantum state:")
print(Statevector.from_instruction(qc))

# Measure both qubits
qc.measure_all()

# Display the circuit
print("\nCircuit:")
print(qc.draw())

# Run 1000 shots on the local simulator
sampler = StatevectorSampler()
job = sampler.run([qc], shots=1000)

# Get the measurement counts
result = job.result()
counts = result[0].data.meas.get_counts()

print("\nMeasurement counts:")
print(counts)

# Display a histogram
plot_histogram(counts)
plt.show()
