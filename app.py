import streamlit as st
from model import build_risk_model
from graph_utils import render_graph
from scenarios import sample_network

st.set_page_config(page_title="Symbolic Systemic Risk Analyzer", layout="wide")
st.title("Symbolic Systemic Risk Analyzer")

st.sidebar.header("Network Configuration")

# Sample network data
data = sample_network()

# Visualize the graph
st.subheader("Financial Network")
st.graphviz_chart(render_graph(data))

# Run the symbolic model
st.subheader("Risk Evaluation")
report = build_risk_model(data)

# Display results
st.markdown("### Model Output")
for line in report:
    st.write(line)

st.info("Use the sidebar to edit nodes, obligations, or thresholds in future versions.")

