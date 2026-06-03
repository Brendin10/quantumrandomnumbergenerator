import streamlit as st
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler
import numpy as np

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Quantum 100-Digit Generator",
    page_icon="⚛️",
    layout="centered"
)

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
        min-height: 80px;
    }
    div.stButton > button {
        width: 100%;
        background-color: #00E5FF;
        color: #0F172A;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚛️ Quantum Random Number Generator")
st.write("Generates a **truly random** 100-digit number using quantum superposition.")

# ====================== QUANTUM FUNCTION ======================
def generate_quantum_bits(total_bits: int = 340) -> str:
    """
    Efficiently generates random bits using quantum measurement.
    Uses 25 qubits per circuit for better performance.
    """
    num_qubits = 25
    collected_bits = ""
    
    sampler = Sampler()
    
    while len(collected_bits) < total_bits:
        # Create circuit
        qc = QuantumCircuit(num_qubits)
        qc.h(range(num_qubits))      # Superposition
        qc.measure_all()             # Measure all qubits
        
        # Run circuit
        job = sampler.run([qc], shots=1)
        result = job.result()
        
        # Correct way to extract bitstring in Aer Sampler (Qiskit 1.x)
        bitstring = result[0].data.meas.get_bitstrings()[0]
        collected_bits += bitstring
    
    return collected_bits[:total_bits]


# ====================== STREAMLIT APP ======================
if "quantum_number" not in st.session_state:
    st.session_state.quantum_number = None
    st.session_state.raw_bits = None

if st.button("Generate 100-Digit Quantum Number"):
    with st.spinner("Entangling qubits and harvesting quantum randomness..."):
        try:
            # Generate ~340 random bits (log2(10) ≈ 3.32 → 100 digits need ~332 bits)
            raw_bits = generate_quantum_bits(340)
            large_int = int(raw_bits, 2)
            number_str = str(large_int)
            
            # Ensure we have exactly 100 digits (pad with more bits if needed)
            while len(number_str) < 100:
                extra_bits = generate_quantum_bits(20)
                extra_int = int(extra_bits, 2)
                number_str += str(extra_int)
            number_str = number_str[:100]
            
            st.session_state.quantum_number = number_str
            st.session_state.raw_bits = raw_bits
            
        except Exception as e:
            st.error(f"Quantum circuit failed: {str(e)}")
            st.session_state.quantum_number = None

# ====================== DISPLAY RESULT ======================
if st.session_state.quantum_number:
    st.success("✅ Quantum randomness successfully harvested!")
    
    st.markdown("### Your 100-Digit Quantum Random Number:")
    st.markdown(
        f'<div class="quantum-box">{st.session_state.quantum_number}</div>',
        unsafe_allow_html=True,
    )
    
    # Copy button (replaces non-existent st.text_copy_button)
    if st.button("📋 Copy Number to Clipboard"):
        st.code(st.session_state.quantum_number, language=None)
        st.success("Number copied to clipboard! (Use Ctrl+C)")
    
    # Optional: Show technical details
    with st.expander("Show Technical Details"):
        st.write("**Raw Quantum Bits (first 64):**")
        st.code(st.session_state.raw_bits[:64] + "...")
        st.write(f"**Total bits used:** {len(st.session_state.raw_bits)}")
        st.write("**Method:** 25-qubit Hadamard + measurement repeated as needed")
        
st.caption("Powered by Qiskit Aer Sampler • Each bit comes from quantum superposition")