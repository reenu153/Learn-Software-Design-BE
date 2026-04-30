import re

def clean(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^\w_]", "", s)
    return s.lower()


def generate_text(graph: dict) -> str:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    node_map = {}

    nodes_text = []

    for n in nodes:
        name = clean(n.get("data", {}).get("name") or n.get("id"))
        node_map[n["id"]] = name

        node_type = n.get("type")

        data = n.get("data", {})

        if node_type == "classNode":
            attrs = data.get("attributes", []) or []
            methods = data.get("methods", []) or []

            nodes_text.append(
                f"CLASS {name} | attrs: {', '.join(attrs) if attrs else 'none'} | methods: {', '.join(methods) if methods else 'none'}"
            )

        elif node_type == "componentNode":
            ports = data.get("ports", []) or []

            nodes_text.append(
                f"COMPONENT {name} | ports: {', '.join(ports) if ports else 'none'}"
            )

        elif node_type in ("interfaceNode", "interfacePortNode"):
            nodes_text.append(f"INTERFACE {name}")

        elif node_type == "databaseNode":
            nodes_text.append(f"DATABASE {name}")

        else:
            nodes_text.append(f"NODE {name} ({node_type})")

    edge_lines = []

    for e in edges:
        source = node_map.get(e.get("source"))
        target = node_map.get(e.get("target"))

        uml_type = (e.get("data") or {}).get("umlType", "association")

        edge_lines.append(
            f"""
RELATIONSHIP:
source: {source}
target: {target}
type: {uml_type}
""".strip()
        )

    return "\n".join(nodes_text + [""] + edge_lines)