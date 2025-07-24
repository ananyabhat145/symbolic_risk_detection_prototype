from z3 import *

def build_risk_model(graph_data, node_config):
    report = []
    solver = Solver()

    # Extract node and edge information
    nodes = graph_data.get('nodes', [])
    edges = graph_data.get('edges', [])

    z3_vars = {}

    # Declare Z3 variables and add base + user-defined constraints
    for node in nodes:
        name = node['id']
        config = node_config.get(name, {})

        # Define Z3 Real variables for each financial metric
        c = Real(f"cap_{name}")         # Capital
        a = Real(f"assets_{name}")      # Total Assets
        l = Real(f"liq_{name}")         # Liquid Assets
        s = Real(f"short_{name}")       # Short-Term Obligations

        # Add value assignments (user-provided or default)
        solver.add(c == config.get('capital', 10.0))
        solver.add(a == config.get('assets', 50.0))
        solver.add(l == config.get('liquidity', 5.0))
        solver.add(s == config.get('short_term', 20.0))

        # Add regulatory constraints
        solver.add(c >= 0.08 * a)        # Capital Adequacy Ratio (Basel III)
        solver.add(l >= 0.25 * s)        # Liquidity Coverage Ratio

        # Store Z3 variables for later reference
        z3_vars[name] = {
            'capital': c,
            'assets': a,
            'liquidity': l,
            'short_term': s
        }

    # Debugging: print edge structure
    if edges:
        print("[DEBUG] Edges format:", edges)
        print("[DEBUG] First edge type:", type(edges[0]))

    # Interbank exposures
    for edge in edges:
        try:
            src = edge['source']
            tgt = edge['target']
            weight = float(edge.get('weight', 1.0))

            # Apply shock propagation logic
            solver.add(z3_vars[tgt]['capital'] >= 0.08 * z3_vars[tgt]['assets'] - weight)

        except Exception as e:
            print(f"[ERROR] Invalid edge format: {edge} -> {e}")
            continue

    # Solve constraints
    result = solver.check()
    if result == sat:
        report.append("✅ System is stable under current constraints.")
        model = solver.model()
        for node_id, vars in z3_vars.items():
            cap_val = model.evaluate(vars['capital'], model_completion=True)
            liq_val = model.evaluate(vars['liquidity'], model_completion=True)
            report.append(f"🏦 Node {node_id}: Capital = {cap_val}, Liquidity = {liq_val}")
    else:
        report.append("❌ Constraint violation: Systemic fragility detected!")
        report.append("💥 Cascade simulation: one or more institutions may fail due to insufficient buffers.")

    return report

