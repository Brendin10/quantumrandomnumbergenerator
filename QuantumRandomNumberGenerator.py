import streamlit as st
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
import math

# 1. Set up page configuration
st.set_page_config(page_title="Quantum 100-Digit Generator", page_icon="⚛️", layout="centered")

# Custom CSS for a cool terminal look
st.markdown(
    """
    <style>
    .quantum-box {
        font-family: 'Courier New', Courier, monospace;
        color: #00E5FF;
        background-color: #0F172A;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #00E5FF;
        font-size: 22px !important;
        word-wrap: break-word;
        text-align: center;
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.25);
    }
    stButton>button {
        width: 100%;
        background-color: #00E5FF;
        color: #0F172A;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
        transition: 0.3s;
    }
    </style>
    """,
    unsafe_allowed_html=True,
)

# App Titles
st.title("⚛️ Quantum Random Number Generator")
st.write("Generates a truly random 100-digit number utilizing Qiskit's quantum superposition simulator.")

# 2. Simplified Quantum Bit Generation Function
def get_quantum_bits(total_bits_needed: int) -> str:
    """Uses a 10-qubit circuit in a loop to cleanly harvest random bits."""
    qubits = 10
    qc = QuantumCircuit(qubits, qubits)
    qc.h(range(qubits))  # Put qubits into superposition
    qc.measure(range(qubits), range(qubits))
    
    sampler = Sampler()
    collected_bits = ""
    
    # Run the circuit repeatedly until we have enough bits
    while len(collected_bits) < total_bits_needed:
        job = sampler.run(qc, shots=1)
        probabilities = job.result().quasi_dists[0].binary_probabilities()
        # Grab the measured bitstring outcome
        bitstring = max(probabilities, key=probabilities.get)
        collected_bits += bitstring
        
    return collected_bits

# 3. Streamlit Interface Logic
if "quantum_number" not in st.session_state:
    st.session_state.quantum_number = None

# "Generate Number" Button
if st.button("Generate Number"):
    with st.spinner("Harvesting quantum states..."):
        # We need ~333 bits to safely break into 100-digit space
        raw_bits = get_quantum_bits(total_bits_needed=340)
        
        # Convert binary string directly into a massive integer
        large_int = int(raw_bits, 2)
        
        # Format/slice it to be exactly 100 digits string
        digits_str = str(large_int)[:100]
        
        # Edge case: pad with extra quantum digits if it's slightly short
        while len(digits_str) < 100:
            digits_str += str(int(get_quantum_bits(10), 2))[0]
            
        st.session_state.quantum_number = digits_str

# Display the final output if generated
if st.session_state.quantum_number:
    st.markdown("### Your 100-Digit Quantum Number:")
    st.markdown(
        f'<div class="quantum-box">{st.session_state.quantum_number}</div>',
        unsafe_allowed_html=True,
    )
    
    # Built-in clipboard copy button
    st.text_copy_button("📋 Copy Number", st.session_state.quantum_number)
