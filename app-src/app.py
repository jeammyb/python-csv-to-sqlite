#!/usr/bin/env python3

import sqlite3
import sys
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger('boardgames')

DATA_BASE = "data.db"


# Database connection class to be use as a context manager
class DatabaseConnection:
    def __init__(self, host):
        self.connection = None
        self.host = host

    def __enter__(self):
        self.connection = sqlite3.connect(self.host)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()


# represents a game 
class Game:
    def __init__(self, name, designer, rating):
        self.name = name
        self.designer = designer
        self.rating = rating

    def __repr__(self):
        return f'Game {self.name} by {self.designer}, Rating: {self.rating}'


# creating game table in case it does not exist
def create_game_table():
    with DatabaseConnection(DATA_BASE) as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS games(name text primary key, designer text, rating integer)')


# parsing input file and return a list with all the game objects
def parser_file(file_path):
    games = []
    try:
        logger.info('Reading file...')
        file = open(file_path, 'r')
        lines = file.readlines()
        file.close()

        if len(lines) == 0:
            logger.warning(f'The file {file_path} is empty')
            quit()

        lines = [line.strip() for line in lines[1:]]
        for line in lines:
            game = line.split(',')
            games.append(Game(*game))
    except FileNotFoundError as e:
        logger.error(e)
        quit(1)
    except TypeError as e:
        logger.error(e)
        quit(1)
    return games


# receive a list with games and it is in charge of adding them to the database
def add_games(games):
    logger.info('Adding games...')
    items_added = []
    for game in games:
        if save_game(game):
            items_added.append(game)
    logger.info(f'{len(items_added)} games were inserted of {len(games)}')


# save a game in database
def save_game(game):
    try:
        with DatabaseConnection(DATA_BASE) as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO games VALUES(?, ?, ?)', (game.name, game.designer, game.rating))
        return True
    except sqlite3.IntegrityError as e:
        logger.error(f'{e} error inserting {game}')
        return False
    

# get all games stored in the database and return them.
def get_all_games():
    with DatabaseConnection(DATA_BASE) as connection:    
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM games')
        games = [Game(*row) for row in cursor.fetchall()]
    return games


# print all games stored in the database
def print_all_games():
    games = get_all_games()
    if len(games) == 0:
        logger.info('There are not games added in the database.')
    for game in games:
        print(game)        


def main():
    # getting file name from second argument
    if len(sys.argv) < 1:
        logger.error(f'Missing input file name argument')
        quit(1)

    file_path = sys.argv[1]
    # creating game table in case it does not exist
    create_game_table()
    # parsing file
    games = parser_file(file_path)
    # saving data 
    add_games(games)
    # printing values from database


if __name__ == "__main__":
    main()
