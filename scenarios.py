def sample_network():
    nodes = [
        {"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}
    ]
    edges = [
        {"source": "A", "target": "B", "weight": 2.0},
        {"source": "B", "target": "C", "weight": 1.5},
        {"source": "C", "target": "D", "weight": 2.2},
        {"source": "D", "target": "A", "weight": 1.0}
    ]
    return {"nodes": nodes, "edges": edges}


