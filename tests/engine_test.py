from twsfw import Engine


def test_engine_version():
    assert Engine().__version__ == "0.1.0"
