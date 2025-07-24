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

# File: model.py

from z3 import *

def build_risk_model(graph_data):
    report = []
    solver = Solver()

    # Unpack graph structure
    nodes = graph_data['nodes']
    edges = graph_data['edges']

    z3_vars = {}

    # Declare variables and constraints
    for node in nodes:
        name = node['id']
        c = Real(f"cap_{name}")
        a = Real(f"assets_{name}")
        l = Real(f"liq_{name}")
        s = Real(f"short_{name}")

        solver.add(c >= 0.08 * a)
        solver.add(l >= 0.25 * s)

        z3_vars[name] = {
            'capital': c,
            'assets': a,
            'liquidity': l,
            'short_term': s
        }

    # Handle exposures
    for edge in edges:
        src = edge['source']
        tgt = edge['target']
        w = edge['weight']

        # Simulate capital loss on target if source defaults
        solver.add(z3_vars[tgt]['capital'] >= 0.08 * z3_vars[tgt]['assets'] - w)

    result = solver.check()
    if result == sat:
        report.append("✅ System is stable under current constraints.")
        model = solver.model()
        for v in z3_vars:
            cap = model.evaluate(z3_vars[v]['capital'])
            liq = model.evaluate(z3_vars[v]['liquidity'])
            report.append(f"Node {v}: capital = {cap}, liquidity = {liq}")
    else:
        report.append("❌ Constraint violation: potential systemic risk detected.")

    return report

# File: graph_utils.py

def render_graph(graph_data):
    lines = ["digraph G {"]
    for node in graph_data['nodes']:
        lines.append(f'{node["id"]} [label="{node["id"]}"]')
    for edge in graph_data['edges']:
        lines.append(f'{edge["source"]} -> {edge["target"]} [label="{edge["weight"]}"]')
    lines.append("}")
    return "\n".join(lines)
