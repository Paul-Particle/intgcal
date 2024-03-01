import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def sample_tasks():
    with open('tests/sample_tasks.ido', 'r') as file:
        return file.readlines()
