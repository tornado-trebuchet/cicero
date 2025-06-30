import os
import sys
import pytest

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    sys.exit(pytest.main(["tests"]))
