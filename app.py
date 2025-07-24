import streamlit as st
from model import build_risk_model
from graph_utils import render_graph
from scenarios import sample_network

st.set_page_config(page_title="Symbolic Systemic Risk Analyzer", layout="wide")
st.title("Symbolic Systemic Risk Analyzer")

st.sidebar.header("Network Configuration")
data = sample_network()

# Editable node parameters
st.sidebar.subheader("Edit Node Parameters")
node_config = {}
for node in data['nodes']:
    st.sidebar.markdown(f"#### Node {node['id']}")
    capital = st.sidebar.number_input(f"Capital of {node['id']}", min_value=0.0, value=10.0, key=f"capital_{node['id']}")
    liquidity = st.sidebar.number_input(f"Liquidity of {node['id']}", min_value=0.0, value=5.0, key=f"liquidity_{node['id']}")
    assets = st.sidebar.number_input(f"Assets of {node['id']}", min_value=0.0, value=50.0, key=f"assets_{node['id']}")
    short_term = st.sidebar.number_input(f"Short-Term Obligations of {node['id']}", min_value=0.0, value=20.0, key=f"short_{node['id']}")
    exposure_cap = st.sidebar.number_input(f"Exposure Cap of {node['id']}", min_value=0.0, value=10.0, key=f"exp_cap_{node['id']}")
    node_config[node['id']] = {
        'capital': capital,
        'liquidity': liquidity,
        'assets': assets,
        'short_term': short_term,
        'exposure_cap': exposure_cap
    }

# Visualize the graph
st.subheader("Financial Network")
st.graphviz_chart(render_graph(data))

# Run the symbolic model
st.subheader("Risk Evaluation")
report = build_risk_model(data, node_config)

# Display results
st.markdown("### Model Output")
for line in report:
    st.write(line)

st.success("Edit node-level parameters using the sidebar to evaluate different stress scenarios.")
