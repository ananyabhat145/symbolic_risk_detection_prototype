from z3 import *

def build_risk_model(graph_data, node_config):
    report = []
    solver = Solver()
    nodes = graph_data['nodes']
    edges = graph_data['edges']

    z3_vars = {}

    # Declare Z3 variables and add constraints
    for node in nodes:
        name = node['id']
        config = node_config.get(name, {})

        c = Real(f"cap_{name}")
        a = Real(f"assets_{name}")
        l = Real(f"liq_{name}")
        s = Real(f"short_{name}")

        # Use actual user-provided values as constants
        solver.add(c == config.get('capital', 10.0))
        solver.add(a == config.get('assets', 50.0))
        solver.add(l == config.get('liquidity', 5.0))
        solver.add(s == config.get('short_term', 20.0))

        # Regulatory constraints
        solver.add(c >= 0.08 * a)         # Basel-style capital adequacy
        solver.add(l >= 0.25 * s)         # Liquidity Coverage Ratio

        z3_vars[name] = {
            'capital': c,
            'assets': a,
            'liquidity': l,
            'short_term': s
        }

    # Handle interbank exposures
    print("[DEBUG] Edges format:", edges)
    print("[DEBUG] First edge type:", type(edges[0]))

    for edge in edges:
        src = edge['source']
        tgt = edge['target']
        weight = edge.get('weight', 1.0)

        # Exposure: If source defaults, it imposes capital stress on target
        solver.add(z3_vars[tgt]['capital'] >= 0.08 * z3_vars[tgt]['assets'] - weight)

    # Solve
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
