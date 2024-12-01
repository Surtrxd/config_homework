def ls(vfs):
    return "\n".join(vfs.list_files())

def cd(vfs, path):
    vfs.change_directory(path)
    return f"Перешли в {vfs.current_path}"

def rm(vfs, filename):
    vfs.remove_file(filename)
    return f"Удалён файл {filename}"

def find(vfs, query):
    results = [name for name in vfs.list_files() if query in name]
    return "\n".join(results)

def uniq(lines):
    unique_lines = list(dict.fromkeys(lines.split("\n")))
    return "\n".join(unique_lines)
