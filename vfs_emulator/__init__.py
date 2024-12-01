# vfs_emulator/__init__.py

# Можно оставить пустым или импортировать основные классы и функции для удобства
from .vfs import VirtualFileSystem
from .commands import ls, cd, rm, find, uniq
from .gui import run_gui
