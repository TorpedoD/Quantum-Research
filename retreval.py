
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Load IBM credentials
load_dotenv(Path(__file__).with_name(".env"))

service = QiskitRuntimeService(
    channel="ibm_quantum_platform",
    token=os.getenv("IBM_QUANTUM_API_KEY"),
    instance=os.getenv("IBM_QUANTUM_CRN")
)

# Retrieve the EXISTING job (does not submit a new one)
job = service.job("db6p4esvf2bc73d1ium0")

print("Waiting for IBM Quantum results...")

# Keep checking until the job finishes
while True:
    status = job.status()
    print("Current job status:", status, flush=True)

    if status == "DONE":
        print("\nJob completed successfully!")
        break

    elif status in ("ERROR", "CANCELLED"):
        raise RuntimeError("Job ended with status: {}".format(status))

    # Wait 15 seconds before checking again
    time.sleep(15)

# Retrieve the completed job's results
result = job.result()
counts = result[0].data.meas.get_counts()

print("\nMeasurement results:")
print(counts)

# Display the results
plot_histogram(counts)
plt.show()
