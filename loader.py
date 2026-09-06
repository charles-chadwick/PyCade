import sqlite3
import logging
import consts

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s: %(message)s')

class Loader:

    def __init__(self):

        try:
            self._conn = sqlite3.connect(consts.Paths.DATABASE)
            self._conn.row_factory = sqlite3.Row
        except sqlite3.Error as error:
            logging.debug(f"{error}")
            raise

    def loadPlayers(self, kind: consts.PlayerKind):
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM players WHERE kind = ?", (kind,))
        players = []
        for player in cursor.fetchall():
            players.append(dict(player))

        return players

    def loadHuman(self):
        players = self.loadPlayers(consts.PlayerKind.HUMAN)
        if len(players) == 0:
            raise Exception("Cannot load human player")

        return players[0]

    def loadEnemies(self):
        return self.loadPlayers(consts.PlayerKind.ENEMY)
