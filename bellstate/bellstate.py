
import os
from dotenv import load_dotenv

from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.executor_sampler import Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Build the Bell circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Load credentials and connect to IBM Quantum
load_dotenv()

api_key = os.getenv("IBM_QUANTUM_API_KEY")
crn = os.getenv("IBM_QUANTUM_CRN")

if not api_key or not crn:
    raise ValueError("Missing IBM Quantum credentials in .env")

service = QiskitRuntimeService(
    channel="ibm_quantum_platform",
    token=api_key,
    instance=crn
)

# Select an available real quantum computer
backend = service.least_busy(
    operational=True,
    simulator=False,
    min_num_qubits=2
)

print("Using quantum computer:", backend.name)

# Compile the circuit for that computer
pm = generate_preset_pass_manager(
    backend=backend,
    optimization_level=1
)

isa_circuit = pm.run(qc)

# Submit the quantum circuit
sampler = Sampler(mode=backend)
job = sampler.run([isa_circuit], shots=1000)

print("Job ID:", job.job_id())

# Retrieve measurement results
result = job.result()
counts = result[0].data.meas.get_counts()

print("Results:", counts)

# results
plot_histogram(counts)
plt.show()
