import map

def test_loads_map_data():

    game_map = map.Map()
    game_map.load("Space Invaders", 1)
    assert isinstance(game_map.boundaries, list)
    assert game_map.name is not None
    assert game_map.level is not None