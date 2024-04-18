from .run import c_tool_string
from os.path import dirname, join

folder_path=dirname(__file__)

def test_c_tool():
    assert c_tool_string(
        string='asd',
        folder_path=folder_path
    ) == {
        join(folder_path, '__init__.py'): 0,
        join(folder_path, 'run.py'): 0,
        join(folder_path, 'run_test.py'): 1
    }
    assert c_tool_string(
        string='path',
        folder_path=folder_path
    ) == {
        join(folder_path, '__init__.py'): 0,
        join(folder_path, 'run.py'): 39,
        join(folder_path, 'run_test.py'): 18
    }
    assert c_tool_string(
        string='.get',
        folder_path=folder_path
    ) == {
        join(folder_path, '__init__.py'): 0,
        join(folder_path, 'run.py'): 0,
        join(folder_path, 'run_test.py'): 1
    }