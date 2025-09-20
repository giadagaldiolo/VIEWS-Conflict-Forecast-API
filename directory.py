import os
import fnmatch

# 表示対象の拡張子（Noneにするとすべて表示）
ALLOWED_EXTENSIONS = ['.py', '.js', '.ts', '.md', '.html']

# 表示する最大深さ（Noneにすると制限なし）
MAX_DEPTH = 3

# 1つのフォルダ内で表示する最大ファイル数（Noneで無制限）
MAX_FILES_PER_FOLDER = 5

def read_gitignore(directory):
    path = os.path.join(directory, '.gitignore')
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return [
            line.strip()
            for line in f.readlines()
            if line.strip() and not line.startswith('#')
        ]

def matches_ignore_patterns(rel_path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(rel_path, pattern):
            return True
    return False

def has_allowed_extension(filename):
    if ALLOWED_EXTENSIONS is None:
        return True
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def visualize_directory(directory, ignore_patterns, indent=0, root=None, depth=0):
    if root is None:
        root = directory

    if MAX_DEPTH is not None and depth > MAX_DEPTH:
        return

    try:
        items = os.listdir(directory)
    except Exception:
        return

    files_shown = 0
    for item in sorted(items):
        full_path = os.path.join(directory, item)
        rel_path = os.path.relpath(full_path, root).replace('\\', '/')

        # 無条件に除外
        if rel_path.startswith('.git'):
            continue

        if matches_ignore_patterns(rel_path, ignore_patterns):
            continue

        if os.path.isdir(full_path):
            print(' ' * indent + f"[DIR] {item}")
            visualize_directory(full_path, ignore_patterns, indent + 4, root, depth + 1)
        else:
            if not has_allowed_extension(item):
                continue
            if MAX_FILES_PER_FOLDER is not None and files_shown >= MAX_FILES_PER_FOLDER:
                if files_shown == MAX_FILES_PER_FOLDER:
                    print(' ' * (indent + 4) + '... (more files)')
                continue
            print(' ' * indent + f"[FILE] {item}")
            files_shown += 1

# === 実行 ===
directory_path = './'  # カレントディレクトリなど
ignore_patterns = read_gitignore(directory_path)
visualize_directory(directory_path, ignore_patterns)
