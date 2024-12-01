class Shell:
    def __init__(self, hostname, vfs):
        self.hostname = hostname
        self.vfs = vfs
        self.current_path = "/"

    def execute_command(self, command):
        if command.startswith("ls"):
            print(" ".join(self.vfs.list_dir(self.current_path)))
        elif command.startswith("cd"):
            _, target = command.split(maxsplit=1)
            self.current_path = target
        elif command == "exit":
            print("Выход.")
            exit(0)
        else:
            print(f"Неизвестная команда: {command}")

    def run_interactive(self):
        while True:
            command = input(f"{self.hostname}:{self.current_path}$ ")
            self.execute_command(command)
