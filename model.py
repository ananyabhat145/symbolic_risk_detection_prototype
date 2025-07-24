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
