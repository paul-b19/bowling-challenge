import sys
import os
import django
sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'bowling_challenge.settings'
django.setup()

from bowling_score.models import *
from bowling_score.game_logic import GameLogic


def main():

    ''' print n latest games '''
    # games = Game.fetch_n_latest_games(n=3)
    # for i in games:
    #     print(i.title)
    
    ''' game test '''
    ### frames 1 - 9
    frames_1_to_9 = ['x','7','/','9','-','x','-','8','8','/','-','6','x','x']

    ### 10th frame original
    n1 = ['x','8','1']

    ### 10th frame options:
    n2 = ['3','/','1']
    n3 = ['3','/','x']
    n4 = ['x','x','1']
    n5 = ['7','/','x']
    n6 = ['x','x','x']

    game = GameLogic()
    for i in frames_1_to_9 + n1: # <- change 10th frame here
        game = game.roll_a_ball(i)
        print(game.game_score, '\n')

if __name__ == '__main__':
    main()
