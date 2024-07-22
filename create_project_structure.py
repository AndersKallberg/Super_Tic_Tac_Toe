import os

def create_project_structure():
    base_dir = 'super_tic_tac_toe'
    dirs = [
        base_dir,
        os.path.join(base_dir, 'tests')
    ]
    files = [
        '__init__.py',
        'cell.py',
        'mini_grid.py',
        'super_grid.py',
        'game.py',
        'cli.py',
        'gui.py',
        'ai.py',
        'utils.py',
        'main.py',
        'tests/__init__.py',
        'tests/test_game.py',
        'tests/test_mini_grid.py',
        'tests/test_super_grid.py',
        'tests/test_cell.py',
        'tests/test_cli.py',
        'tests/test_gui.py',
    ]

    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

    for file in files:
        open(os.path.join(base_dir, file), 'w').close()

if __name__ == '__main__':
    create_project_structure()