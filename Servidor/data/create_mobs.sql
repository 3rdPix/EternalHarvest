-- Creatures table
Create Table mobs (
    ID INTEGER PRIMARY KEY NOT NULL,
    game_id INTEGER,
    mob_zone TEXT (50) NOT NULL,
    mob_type INTEGER DEFAULT 0,
    sp_name TEXT (20) NOT NULL,
    en_name TEXT (20) NOT NULL,
    fr_name TEXT (20) NOT NULL,
    url_img TEXT(200) NOT NULL
    );