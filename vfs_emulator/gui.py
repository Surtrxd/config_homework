import tkinter as tk
from tkinter import messagebox

class ShellGUI:
    def __init__(self, hostname, vfs):
        self.hostname = hostname
        self.vfs = vfs
        self.current_dir = "/"
        self.init_gui()

    def init_gui(self):
        """Инициализация графического интерфейса."""
        self.root = tk.Tk()
        self.root.title(f"Shell Emulator - {self.hostname}")

        # Поле для ввода команд
        self.command_entry = tk.Entry(self.root, width=50)
        self.command_entry.pack(pady=10)
        self.command_entry.bind("<Return>", self.handle_command)

        # Поле вывода
        self.output_text = tk.Text(self.root, height=20, width=80, state="disabled")
        self.output_text.pack(pady=10)

        # Кнопка выхода
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(pady=5)

    def handle_command(self, event):
        """Обработка команды, введённой пользователем."""
        command = self.command_entry.get().strip()
        if not command:
            return

        self.log_output(f"{self.hostname}:{self.current_dir}$ {command}")
        self.command_entry.delete(0, tk.END)

        try:
            self.execute_command(command)
        except Exception as e:
            self.log_output(f"Ошибка: {e}")

    def execute_command(self, command):
        """Исполнение команды."""
        parts = command.split()
        if not parts:
            return

        cmd, *args = parts

        if cmd == "ls":
            self.log_output("\n".join(self.vfs.list_dir(self.current_dir)))
        elif cmd == "cd":
            if args:
                new_dir = args[0]
                self.current_dir = self.vfs.change_dir(self.current_dir, new_dir)
                self.log_output(f"Перешёл в {self.current_dir}")
            else:
                self.log_output("Ошибка: отсутствует аргумент для cd")
        elif cmd == "exit":
            self.root.destroy()
        elif cmd == "rm":
            if args:
                self.vfs.remove_file(self.current_dir, args[0])
                self.log_output(f"Файл {args[0]} удалён")
            else:
                self.log_output("Ошибка: отсутствует аргумент для rm")
        elif cmd == "find":
            if args:
                result = self.vfs.find(self.current_dir, args[0])
                self.log_output("\n".join(result))
            else:
                self.log_output("Ошибка: отсутствует аргумент для find")
        elif cmd == "uniq":
            if args:
                unique_lines = self.vfs.uniq(args[0])
                self.log_output("\n".join(unique_lines))
            else:
                self.log_output("Ошибка: отсутствует аргумент для uniq")
        else:
            self.log_output(f"Неизвестная команда: {cmd}")

    def log_output(self, text):
        """Добавляет текст в поле вывода."""
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.config(state="disabled")
        self.output_text.see(tk.END)

def run_gui(hostname, vfs):
    """Запуск GUI оболочки."""
    try:
        gui = ShellGUI(hostname, vfs)
        gui.root.mainloop()
    except tk.TclError as e:
        print(f"Ошибка запуска GUI: {e}. Убедитесь, что Tcl/Tk установлены корректно.")
