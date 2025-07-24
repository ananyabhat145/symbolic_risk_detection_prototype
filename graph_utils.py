def render_graph(graph_data):
    lines = ["digraph G {"]
    for node in graph_data['nodes']:
        lines.append(f'{node["id"]} [label="{node["id"]}"]')
    for edge in graph_data['edges']:
        lines.append(f'{edge["source"]} -> {edge["target"]} [label="{edge["weight"]}"]')
    lines.append("}")
    return "\n".join(lines)

