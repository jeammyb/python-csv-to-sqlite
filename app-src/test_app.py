import pytest
import os
import app

app.DATA_BASE = "test_data.db"


@pytest.fixture()
def setup_rm_database(request):
    def teardown():
        os.remove(app.DATA_BASE)
    request.addfinalizer(teardown)


@pytest.fixture()
def setup_db_table(request):
    app.create_game_table()

    def teardown():
        os.remove(app.DATA_BASE)
    request.addfinalizer(teardown)


@pytest.fixture()
def setup_parser_file(request):
    data = """name,artist,rating
    Blood Rage,Eric M. Lang,9
    Stone Age,Bernd Brunnhofer,7
    King of Tokyo,Richard Garfield,7
    Ticket to Ride,Alan R. Moon,8"""

    file_path = "csv_test_data.txt"
    file = open(file_path, "w") 
    file.write(data)
    file.close

    def teardown():
        os.remove(file_path)

    request.addfinalizer(teardown)


def test_create_game_table(setup_rm_database):
    app.create_game_table()


def test_parser_file_count(setup_parser_file):      
    result = app.parser_file('csv_test_data.txt')
    assert len(result) == 4


def test_parser_file_values(setup_parser_file):      
    result = app.parser_file('csv_test_data.txt')
    assert result[0].rating == "9"
    assert result[0].name == "Blood Rage"
    assert result[0].designer == "Eric M. Lang"


def test_save_game(setup_db_table):
    game = app.Game('Exploding Kittens', 'Matthew Inman', 7)
    result = app.save_game(game)
    assert result == True


def test_add_games(setup_db_table):
    game_a = app.Game('Exploding Kittens', 'Matthew Inman', 7)
    game_b = app.Game('Blood Rage', 'Eric M. Lang', 10)
    game_c = app.Game('Stone Age', 'Bernd Brunnhofer', 6)
    games = [game_a, game_b, game_c]
    app.add_games(games)
