import pytest
import tkinter as tk
from vfs_emulator.gui import run_gui



@pytest.fixture
def gui_app():
    root = tk.Tk()
    return root

def test_gui_render(gui_app):
    # Проверяем создание главного окна
    assert gui_app.winfo_exists()

def test_command_execution(mocker):
    # Мокаем функцию выполнения команды
    mock_execute = mocker.patch("vfs_emulator.gui.execute_command")
    run_gui("TestHost", None)
    mock_execute.assert_not_called()
