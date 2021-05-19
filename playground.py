import sys
import os
import django
sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'bowling_challenge.settings'
django.setup()
from django.conf import settings
from bowling_score.models import *


def main():

    # games = Game.fetch_n_latest_games(3)
    # for i in games:
    #     print(i.title)
    
    # frame = Frame.objects.first()
    # print(frame)

    # balls = frame.ball_set.first()
    # print(balls)

    from bowling_score.game_logic import GameLogic
    game = GameLogic()
    game.roll_a_ball('x')
    game.roll_a_ball('x')
    game.roll_a_ball('1')
    game.roll_a_ball('/')
    game.roll_a_ball('5')
    game.roll_a_ball('-')
    game.roll_a_ball('-')
    game.roll_a_ball('/')
    game.roll_a_ball('9')

if __name__ == '__main__':
    main()
