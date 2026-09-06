import consts
import loader, players

def test_instantiate_player():

    loader_class = loader.Loader()
    human_data = loader_class.loadHuman()
    player = players.Player(consts.PlayerKind.HUMAN)
    player.load(human_data)

