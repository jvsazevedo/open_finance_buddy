import ast

with open('/home/azevedo/Projetos/hub_agentes_graph/src/utils/__init__.py', 'r', encoding='utf-8') as f:
    code = f.read()

tree = ast.parse(code)

for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            print(f"at line: {node.lineno} " + f"import {alias.name}" + (f" as {alias.asname}" if alias.asname else ""))
    elif isinstance(node, ast.ImportFrom):
        module = node.module
        for alias in node.names:
            print(f"at line: {node.lineno} " + f"from {module} import {alias.name}" + (f" as {alias.asname}" if alias.asname else ""))
