import os

def analyze_file_structure(base_path):
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

if __name__ == "__main__":
    base_path = os.path.abspath(os.path.dirname(__file__))
    print("Project file structure:")
    analyze_file_structure(base_path)
