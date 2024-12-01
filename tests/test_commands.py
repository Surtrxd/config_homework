import pytest
from vfs_emulator.vfs import VirtualFileSystem
from vfs_emulator.commands import ls, cd, rm, find, uniq



@pytest.fixture
def vfs():
    return VirtualFileSystem("test_fs.tar")

def test_ls(vfs):
    # Проверяем корректность команды ls
    files = ls(vfs)
    assert "test_file.txt" in files

def test_cd(vfs):
    # Проверяем команду cd
    cd(vfs, "/subdir")
    assert vfs.current_directory == "/subdir"

def test_rm(vfs):
    # Проверяем удаление файла
    rm(vfs, "test_file.txt")
    assert "test_file.txt" not in vfs.fs

def test_rm_nonexistent(vfs):
    # Проверяем удаление несуществующего файла
    with pytest.raises(FileNotFoundError):
        rm(vfs, "nonexistent_file.txt")

def test_find(vfs):
    # Проверяем поиск файла
    results = find(vfs, ".", "*.txt")
    assert "test_file.txt" in results

def test_uniq():
    # Проверяем фильтрацию повторяющихся строк
    input_data = ["a", "b", "a", "c", "b", "c"]
    result = uniq(input_data)
    assert result == ["a", "b", "c"]
