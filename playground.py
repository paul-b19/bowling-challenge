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

    games = Game.objects.all()
    for i, j in list(enumerate(games)):
        print(i, j.title)

if __name__ == '__main__':
    main()
