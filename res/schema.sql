
CREATE TABLE IF NOT EXISTS players (
    id     INTEGER NOT NULL PRIMARY KEY,
    kind   TEXT    NOT NULL,
    name   TEXT,
    health INTEGER NOT NULL,
    size   TEXT    NOT NULL,
    shape  TEXT    NOT NULL,
    speed  INTEGER NOT NULL
);
