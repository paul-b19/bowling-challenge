import sys
import os
import django
sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'bowling_challenge.settings'
django.setup()

from bowling_score.models import *
from bowling_score.game_logic import GameLogic


def main():

    # games = Game.fetch_n_latest_games(3)
    # for i in games:
    #     print(i.title)
    
    game = GameLogic()
    # frames 1 - 9
    game.roll_a_ball('x')
    game.roll_a_ball('7')
    game.roll_a_ball('/')
    game.roll_a_ball('9')
    game.roll_a_ball('-')
    game.roll_a_ball('x')
    game.roll_a_ball('-')
    game.roll_a_ball('8')
    game.roll_a_ball('8')
    game.roll_a_ball('/')
    game.roll_a_ball('-')
    game.roll_a_ball('6')
    game.roll_a_ball('x')
    game.roll_a_ball('x')

    # 10th frame original
    game.roll_a_ball('x')
    game.roll_a_ball('8')
    game.roll_a_ball('1')

    # #2
    # game.roll_a_ball('3')
    # game.roll_a_ball('/')
    # game.roll_a_ball('1')

    # #3
    # game.roll_a_ball('3')
    # game.roll_a_ball('/')
    # game.roll_a_ball('x')

    # #4
    # game.roll_a_ball('x')
    # game.roll_a_ball('x')
    # game.roll_a_ball('1')

    # #5
    # game.roll_a_ball('x')
    # game.roll_a_ball('x')
    # game.roll_a_ball('-')

    # #6
    # game.roll_a_ball('x')
    # game.roll_a_ball('x')
    # game.roll_a_ball('x')

if __name__ == '__main__':
    main()
