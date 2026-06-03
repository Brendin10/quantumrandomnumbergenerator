from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.primitives import Sampler
import numpy as np
from typing import Tuple

class QuantumRNG:
    """
    Quantum Random Number Generator using Hadamard gates and measurement.
    Each qubit in superposition gives us a genuinely random bit.
    """
    
    def __init__(self, simulator: bool = True):
        self.backend = AerSimulator()
        
    def generate_random_bits(self, num_bits: int = 8, shots: int = 1) -> str:
        """
        Generate random bits using quantum superposition.
        
        Args:
            num_bits: Number of random bits to generate
            shots: Number of measurements (usually 1 for true randomness)
            
        Returns:
            Binary string of random bits
        """
        # Create quantum circuit
        qc = QuantumCircuit(num_bits, num_bits)
        
        # Put all qubits in superposition (Hadamard gate)
        qc.h(range(num_bits))
        
        # Measure all qubits
        qc.measure(range(num_bits), range(num_bits))
        
        # Execute the circuit
        sampler = Sampler()
        job = sampler.run(qc, shots=shots)
        result = job.result()
        
        # Get the measured bitstring
        # The Sampler returns quasi-probabilities, we take the most likely outcome
        counts = result.quasi_dists[0].binary_probabilities()
        bitstring = max(counts, key=counts.get)
        
        return bitstring
    
    def generate_random_int(self, num_bits: int = 8) -> Tuple[int, str]:
        """
        Generate a random integer using quantum measurement.
        
        Args:
            num_bits: Size of the random number in bits
            
        Returns:
            Tuple of (random_integer, binary_representation)
        """
        bitstring = self.generate_random_bits(num_bits)
        random_int = int(bitstring, 2)
        
        return random_int, bitstring
    
    def generate_random_float(self, num_bits: int = 32) -> float:
        """
        Generate a random float between 0 and 1.
        """
        bitstring = self.generate_random_bits(num_bits)
        random_int = int(bitstring, 2)
        return random_int / (2**num_bits - 1)


# ================================
# Example Usage
# ================================

if __name__ == "__main__":
    qrng = QuantumRNG()
    
    print("=== Quantum Random Number Generator ===\n")
    
    # Generate an 8-bit random number (0-255)
    for i in range(5):
        random_num, bits = qrng.generate_random_int(8)
        print(f"Run {i+1}:")
        print(f"  Binary : {bits}")
        print(f"  Decimal: {random_num}")
        print("-" * 30)
    
    # Generate a random float between 0 and 1
    random_float = qrng.generate_random_float(32)
    print(f"\nRandom float (32-bit precision): {random_float:.8f}")
    
    # Generate a larger random number (e.g. 32-bit)
    large_num, bits = qrng.generate_random_int(32)
    print(f"\n32-bit random number: {large_num:,} (0x{large_num:08X})")