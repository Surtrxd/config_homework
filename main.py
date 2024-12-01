import os
import toml
from vfs_emulator.vfs import VirtualFileSystem


def load_config(config_path):
    """
    Загружает конфигурационный файл TOML.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Файл конфигурации {config_path} не найден.")
    with open(config_path, "r", encoding="utf-8") as file:
        return toml.load(file)



def main():
    # Пути
    config_path = os.path.join(os.path.dirname(__file__), "config.toml")
    config = load_config(config_path)

    hostname = config.get("hostname", "VirtualMachine")
    fs_path = config.get("fs_path")
    start_script_path = config.get("start_script")

    print(f"Ищу конфигурационный файл по пути: {config_path}")
    print(f"Конфигурация загружена: {config}")

    # Инициализация виртуальной файловой системы
    if not fs_path or not os.path.exists(fs_path):
        raise FileNotFoundError(f"Образ файловой системы {fs_path} не найден.")
    vfs = VirtualFileSystem(fs_path)
    print(f"Файловая система загружена из {fs_path}")

    # Выполнение команд из стартового скрипта
    if start_script_path and os.path.exists(start_script_path):
        print(f"Выполняю команды из скрипта {start_script_path}...")
        with open(start_script_path, "r") as script_file:
            for command in script_file:
                command = command.strip()
                print(f"Выполняю: {command}")
                if command:
                    print(vfs.execute(command))
    else:
        print(f"Стартовый скрипт {start_script_path} не найден или не указан.")

    # Интерактивный режим
    print(f"{hostname}: Введите команду (exit для выхода)")
    while True:
        try:
            command = input(f"{hostname}:~$ ")
            if command.strip().lower() == "exit":
                print("Выход из эмулятора.")
                break
            if command.strip():
                print(vfs.execute(command))
        except KeyboardInterrupt:
            print("\nВыход из эмулятора.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
