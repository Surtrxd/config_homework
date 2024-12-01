import tarfile
import os

class VirtualFileSystem:
    def __init__(self, tar_path):
        self.root = {}  # Структура файловой системы
        self.current_dir = self.root
        self.load_tar(tar_path)

    def load_tar(self, tar_path):
        """
        Загружает файловую систему из tar-архива в виде вложенного словаря.
        """
        try:
            with tarfile.open(tar_path, "r") as tar:
                for member in tar.getmembers():
                    parts = os.path.normpath(member.name).split(os.sep)
                    current = self.root
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    if member.isfile():
                        current[parts[-1]] = None
                    elif member.isdir():
                        current[parts[-1]] = {}
            self.current_dir = self.root
        except FileNotFoundError:
            print(f"Ошибка: файл {tar_path} не найден.")
        except tarfile.ReadError:
            print(f"Ошибка: файл {tar_path} не является корректным tar-архивом.")

    def list_dir(self):
        if not self.current_dir:
            return "Текущая директория пуста."
        return "\n".join(
            f"{name}/" if isinstance(content, dict) else name
            for name, content in self.current_dir.items()
        )

    def change_dir(self, path):
        if path == "/":
            self.current_dir = self.root
            return "Перешли в корневую директорию."

        parts = path.strip("/").split("/")
        current = self.current_dir if not path.startswith("/") else self.root
        stack = [] if path.startswith("/") else [self.current_dir]

        for part in parts:
            if part == "..":
                if not stack:
                    return "Ошибка: вы уже находитесь в корневой директории."
                stack.pop()
            elif part and part in current and isinstance(current[part], dict):
                stack.append(current)
                current = current[part]
            else:
                return f"Ошибка: директория {path} не существует."
        
        self.current_dir = stack[-1] if stack else self.root
        return f"Перешли в директорию {path}."


    def find(self, filename):
        result = []

        def recursive_search(directory, path):
            for name, content in directory.items():
                new_path = f"{path}/{name}"
                if name == filename:
                    result.append(new_path)
                if isinstance(content, dict):
                    recursive_search(content, new_path)

        recursive_search(self.root, "")
        return "\n".join(result) if result else f"Файл {filename} не найден."

    def remove_file(self, filename):
        if filename in self.current_dir:
            if isinstance(self.current_dir[filename], dict):
                return f"Ошибка: {filename} — это директория, а не файл."
            del self.current_dir[filename]
            return f"Файл {filename} удалён."
        return f"Ошибка: файл {filename} не найден."

    def uniq(self, filename):
        if filename not in self.current_dir or self.current_dir[filename] is not None:
            return f"Ошибка: файл {filename} не найден или он является директорией."

        # Заглушка для содержимого файла
        file_content = [
            "строка 1",
            "строка 2",
            "строка 1",
            "строка 3",
        ]
        unique_lines = list(dict.fromkeys(file_content))
        return "\n".join(unique_lines)

    def execute(self, command):
        """
        Выполняет команду в виртуальной файловой системе.
        """
        parts = command.split()
        if not parts:
            return "Введите команду."
        cmd, *args = parts
        if cmd == "ls":
            return self.list_dir()
        elif cmd == "cd":
            if not args:
                return "Ошибка: укажите директорию."
            return self.change_dir(args[0])
        elif cmd == "find":
            if not args:
                return "Ошибка: укажите имя файла."
            return self.find(args[0])
        elif cmd == "rm":
            if not args:
                return "Ошибка: укажите файл для удаления."
            return self.remove_file(args[0])
        elif cmd == "uniq":
            if not args:
                return "Ошибка: укажите файл для обработки."
            return self.uniq(args[0])
        else:
            return f"Неизвестная команда: {cmd}"
