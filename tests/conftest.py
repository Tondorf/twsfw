import pathlib

import pytest


@pytest.fixture
def wasm_agent():
    with open(pathlib.Path(__file__).parents[1] / "agents" / "example" / "agent.wasm", "rb") as f:
        return f.read()
