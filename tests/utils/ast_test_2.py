import ast


class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []  # Store extracted import info here

    def visit_Import(self, node):
        # Handles 'import module' or 'import module as alias'
        for alias in node.names:
            import_info = {
                'type': 'Import',
                'module_name': alias.name,
                'alias': alias.asname,  # None if no alias
                'line': node.lineno
            }
            self.imports.append(import_info)
        self.generic_visit(node)  # Continue traversing child nodes if any

    def visit_ImportFrom(self, node):
        # Handles 'from module import symbol' or 'from .relative import symbol'
        module_name = node.module if node.module else ""  # Handle 'from . import X'
        level = node.level  # 0 for absolute, 1 for '.', 2 for '..' etc.

        symbols = []
        for alias in node.names:
            symbols.append({
                'name': alias.name,  # The original name ('*' for import *)
                'alias': alias.asname  # The local alias, None if no alias
            })

        import_info = {
            'type': 'ImportFrom',
            'module_name': module_name,
            'level': level,  # Crucial for relative imports
            'symbols': symbols,
            'line': node.lineno
        }
        self.imports.append(import_info)
        self.generic_visit(node)  # Continue traversing child nodes


path = '/home/azevedo/Projetos/hub_agentes_graph/src/utils/expenses_db_sqlite.py'
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

tree = ast.parse(code)
visitor = ImportVisitor()
visitor.visit(tree)
print(visitor.imports)

test = [
    {
        'type': 'ImportFrom',
        'module_name': 'expenses_db_sqlite',
        'level': 1,
        'symbols':
            [
                {'name': 'create_expenses_table', 'alias': None},
                {'name': 'create_user_table', 'alias': None},
                {'name': 'create_user_params_table', 'alias': None},
                {'name': 'get_user_monthly_income', 'alias': None},
                {'name': 'get_user_monthly_expenses', 'alias': None},
                {'name': 'get_expenses_by_month', 'alias': None},
                {'name': 'add_user_expense', 'alias': None},
                {'name': 'add_user', 'alias': None},
                {'name': 'add_user_param', 'alias': None}
            ],
        'line': 1
    },
    {
        'type': 'ImportFrom',
        'module_name': 'messages_db_sqlite',
        'level': 1,
        'symbols': [
            {'name': 'create_conversations_table', 'alias': None},
            {'name': 'add_message_with_embedding', 'alias': None},
            {'name': 'get_recent_conversations', 'alias': None},
            {'name': 'find_similar_messages_for_user', 'alias': None},
            {'name': 'find_recent_similar_messages_by_date', 'alias': None},
            {'name': 'find_similar_messages_by_topic', 'alias': None}],
        'line': 12
    }
]

test2 = [
    {
        'type': 'ImportFrom',
        'module_name': 'typing',
        'level': 0,
        'symbols': [
            {'name': 'Dict', 'alias': None},
            {'name': 'Any', 'alias': None}
        ],
        'line': 1
    },
    {
        'type': 'Import',
        'module_name': 'sqlite3',
        'alias': None, 'line': 2
    }
]
