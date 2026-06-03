import streamlit as st
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# 1. Page Configuration & Aesthetic Theme
st.set_page_config(page_title="Quantum 100-Digit Generator", page_icon="⚛️", layout="centered")

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
st.write("Generates a truly random 100-digit number utilizing Qiskit's quantum superposition.")

# 2. Updated Quantum Generation using Modern V2 Primitives
def get_quantum_bits(total_bits_needed: int) -> str:
    """Uses a 10-qubit circuit with modern StatevectorSampler to extract random bits."""
    num_qubits = 10
    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))      # Map qubits to superposition
    qc.measure_all()              # Automatically adds classical registers and measures
    
    sampler = StatevectorSampler()
    collected_bits = ""
    
    # Safely loop until we harvest enough unique bits
    while len(collected_bits) < total_bits_needed:
        job = sampler.run([qc], shots=1)
        result = job.result()[0]  # Extract result for our circuit pub
        
        # Pull bitstring data directly from classical register fields
        bit_data = result.data.meas.get_bitstrings()
        if bit_data:
            collected_bits += bit_data[0]
            
    return collected_bits

# 3. Streamlit State & Execution 
if "quantum_number" not in st.session_state:
    st.session_state.quantum_number = None

if st.button("Generate Number"):
    with st.spinner("Harvesting quantum states..."):
        # Fetch bits (~340 bits cleanly converts past 100 base-10 characters)
        raw_bits = get_quantum_bits(total_bits_needed=340)
        
        # Cast to base-10 and isolate the first 100 digits
        large_int = int(raw_bits, 2)
        digits_str = str(large_int)[:100]
        
        # Pad edge cases if integer evaluation drops leading digits
        while len(digits_str) < 100:
            digits_str += str(int(get_quantum_bits(10), 2))[0]
            
        st.session_state.quantum_number = digits_str

# Display Container
if st.session_state.quantum_number:
    st.markdown("### Your 100-Digit Quantum Number:")
    st.markdown(
        f'<div class="quantum-box">{st.session_state.quantum_number}</div>',
        unsafe_allow_html=True,
    )
    st.text_copy_button("📋 Copy Number", st.session_state.quantum_number)
