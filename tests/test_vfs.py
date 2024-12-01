import pytest
from vfs_emulator.vfs import VirtualFileSystem

@pytest.fixture
def vfs():
    return VirtualFileSystem("test_fs.tar")  # Создайте небольшой тестовый tar-файл заранее

def test_load_filesystem(vfs):
    # Проверяем, что виртуальная ФС загрузилась корректно
    assert len(vfs.fs) > 0  # В файле должно быть хотя бы несколько элементов

def test_list_directory(vfs):
    # Проверяем список файлов в корневой директории
    files = vfs.list_directory("/")
    assert "test_file.txt" in files

def test_change_directory(vfs):
    # Проверяем переход в поддиректорию
    vfs.change_directory("/subdir")
    assert vfs.current_directory == "/subdir"

def test_invalid_directory(vfs):
    # Проверяем, что переход в несуществующую директорию вызывает ошибку
    with pytest.raises(FileNotFoundError):
        vfs.change_directory("/nonexistent")
