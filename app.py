import streamlit as st
from model import build_risk_model
from graph_utils import render_graph
from scenarios import sample_network

st.set_page_config(page_title="Symbolic Systemic Risk Analyzer", layout="wide")

# Theme toggle
if "theme" not in st.session_state:
    st.session_state.theme = "light"

selected_theme = st.sidebar.radio("🎨 Theme", ["light", "dark"], index=0 if st.session_state.theme == "light" else 1)
st.session_state.theme = selected_theme

# Dynamic theme CSS
if selected_theme == "dark":
    background = "#1e272e"
    text = "#ecf0f1"
    primary = "#00a8ff"
    secondary = "#2f3640"
else:
    background = "#f9f9fc"
    text = "#2c3e50"
    primary = "#40739e"
    secondary = "#ecf0f1"

st.markdown(f"""
    <style>
        html, body, [class*="css"]  {{
            font-family: 'Segoe UI', sans-serif;
            background-color: {background};
            color: {text};
        }}
        .reportview-container .main .block-container{{
            padding: 2rem;
        }}
        h1, h2, h3, h4 {{
            color: {primary};
        }}
        .stButton > button {{
            background-color: {primary};
            color: white;
            border-radius: 8px;
            padding: 0.5em 1.5em;
            transition: all 0.3s ease-in-out;
        }}
        .stButton > button:hover {{
            transform: scale(1.05);
            background-color: {text};
            color: {background};
        }}
        .stSidebar {{
            background-color: {secondary};
        }}
        .css-1aumxhk {{
            padding: 2rem;
        }}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Symbolic Systemic Risk Analyzer")

with st.sidebar.expander("📘 Help: What do these values mean?", expanded=False):
    st.markdown("""
    - **Capital**: Equity or capital buffer of the institution.
    - **Liquidity**: Easily accessible cash or liquid assets.
    - **Total Assets**: The full balance sheet size.
    - **Short-Term Obligations**: Debts due in the near term.
    - **Exposure Cap**: Limit to how much risk an institution can absorb from others.
    """)

st.sidebar.header("⚙️ Network Configuration")
data = sample_network()

# Editable node parameters
st.sidebar.subheader("🧮 Edit Node Parameters")
node_config = {}
for node in data['nodes']:
    with st.sidebar.expander(f"🏦 Node {node['id']}", expanded=False):
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

# Display results with animation-like messaging
st.markdown("### 🔍 Model Output")
collapse_detected = any("FAILURE" in line.upper() for line in report)
for line in report:
    if "FAIL" in line.upper():
        st.error(f"💥 {line} — system stress cascading!")
    else:
        st.code(line, language="text")

if collapse_detected:
    st.warning("🚨 Multiple institutions failed — potential domino effect!")
    st.balloons()
else:
    st.success("✅ No catastrophic failures detected in this configuration.")
