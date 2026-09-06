import pytest
import loader

load_class = loader.Loader()

def test_loads_human():
    human = load_class.loadHuman()
    assert type(human) is dict

def test_loads_enemies():
    enemies = load_class.loadEnemies()
    assert type(enemies) is list