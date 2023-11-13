import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def sample_tasks():
    with open('path/to/utils/sample_tasks.txt', 'r') as file:
        return file.readlines()
