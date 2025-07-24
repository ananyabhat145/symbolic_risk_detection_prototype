import streamlit as st
from model import build_risk_model
from graph_utils import render_graph
from scenarios import sample_network

st.set_page_config(page_title="Symbolic Systemic Risk Analyzer", layout="wide")

# Apply custom theme colors using markdown hack
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f0f4f8;
            color: #2c3e50;
        }
        .reportview-container .main .block-container{
            padding: 2rem 2rem 2rem 2rem;
        }
        h1, h2, h3, h4 {
            color: #1e3799;
        }
        .stButton > button {
            background-color: #3c6382;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.6em;
            border: none;
        }
        .stButton > button:hover {
            background-color: #0a3d62;
        }
        .stSidebar {
            background-color: #dff9fb;
        }
        .css-1aumxhk {
            padding: 2rem;
        }
        .sidebar-content {
            padding: 1rem;
            font-size: 0.95rem;
        }
        .element-container label {
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Symbolic Systemic Risk Analyzer")

st.sidebar.header("⚙️ Network Configuration")
data = sample_network()

# Editable node parameters
st.sidebar.subheader("🧮 Edit Node Parameters")
node_config = {}
for node in data['nodes']:
    with st.sidebar.expander(f"🏦 Node {node['id']} Settings", expanded=False):
        capital = st.number_input(f"Capital of {node['id']}", min_value=0.0, value=10.0, key=f"capital_{node['id']}")
        liquidity = st.number_input(f"Liquidity of {node['id']}", min_value=0.0, value=5.0, key=f"liquidity_{node['id']}")
        assets = st.number_input(f"Assets of {node['id']}", min_value=0.0, value=50.0, key=f"assets_{node['id']}")
        short_term = st.number_input(f"Short-Term Obligations of {node['id']}", min_value=0.0, value=20.0, key=f"short_{node['id']}")
        exposure_cap = st.number_input(f"Exposure Cap of {node['id']}", min_value=0.0, value=10.0, key=f"exp_cap_{node['id']}")
        node_config[node['id']] = {
            'capital': capital,
            'liquidity': liquidity,
            'assets': assets,
            'short_term': short_term,
            'exposure_cap': exposure_cap
        }

# Visualize the graph
st.subheader("📉 Financial Network Structure")
st.graphviz_chart(render_graph(data))

# Run the symbolic model
st.subheader("🧠 Risk Evaluation Engine")
report = build_risk_model(data, node_config)

# Display results
st.markdown("### 🔍 Model Output")
for line in report:
    st.code(line)

st.success("✅ Use the sidebar to customize parameters and simulate shock responses.")
