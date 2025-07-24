import streamlit as st
from model import build_risk_model
from graph_utils import render_graph
from scenarios import sample_network

st.set_page_config(page_title="Symbolic Systemic Risk Analyzer", layout="wide")

# Theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "light"

st.sidebar.toggle("🌗 Toggle Dark Mode", value=(st.session_state.theme == "dark"), key="theme_toggle")
if st.session_state.theme_toggle:
    st.session_state.theme = "dark"
    primary_color = "#ecf0f1"
    background_color = "#2c3e50"
    font_color = "#ecf0f1"
else:
    st.session_state.theme = "light"
    primary_color = "#2c3e50"
    background_color = "#f9f9fc"
    font_color = "#2c3e50"

st.markdown(f"""
    <style>
        html, body, [class*="css"]  {{
            font-family: 'Segoe UI', sans-serif;
            background-color: {background_color};
            color: {font_color};
        }}
        .reportview-container .main .block-container{{
            padding: 2rem 2rem 2rem 2rem;
        }}
        h1, h2, h3, h4 {{
            color: {primary_color};
        }}
        .stButton > button {{
            background-color: #40739e;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1.5em;
        }}
        .stSidebar {{
            background-color: #ecf0f1;
        }}
        .css-1aumxhk {{
            padding: 2rem;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Symbolic Systemic Risk Analyzer")

st.sidebar.header("⚙️ Network Configuration")
data = sample_network()

# Help button
with st.sidebar.expander("❓ What do these settings mean?"):
    st.markdown("""
    - **Capital**: Total equity available to absorb losses.
    - **Liquidity**: Cash or near-cash assets for short-term obligations.
    - **Assets**: Total assets (including investments and loans).
    - **Short-Term Obligations**: Liabilities due soon.
    - **Exposure Cap**: Maximum acceptable exposure to another institution.
    """)

# Editable node parameters
st.sidebar.subheader("🧮 Edit Node Parameters")
node_config = {}
for node in data['nodes']:
    with st.sidebar.expander(f"🏦 Node {node['id']}"):
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
report, systemic_failure = build_risk_model(data, node_config)

# Display results
st.markdown("### 🔍 Model Output")
for line in report:
    st.code(line, language='text')

if systemic_failure:
    st.error("⚠️ Systemic cascade detected! Institutions failing across the network.")
    st.balloons()
else:
    st.success("✅ No cascading failures detected under current configuration.")

st.info("📌 Edit node-level parameters using the sidebar to evaluate different stress scenarios.")
