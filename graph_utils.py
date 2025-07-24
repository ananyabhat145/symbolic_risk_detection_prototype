def render_graph(graph_data):
    lines = ["digraph G {"]
    for node in graph_data['nodes']:
        lines.append(f'{node["id"]} [label="{node["id"]}", style=filled, fillcolor="#dcdde1"]')
    for edge in graph_data['edges']:
        lines.append(f'{edge["source"]} -> {edge["target"]} [label="{edge["weight"]}", color="#718093"]')
    lines.append("}")
    return "\n".join(lines)

