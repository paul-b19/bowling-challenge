from django.shortcuts import render
from bowling_score.models import *
from bowling_score.game_logic import GameLogic

def index(request, message=None):
    message = message if message else 'No Message' ###
    score_board = Game.fetch_n_latest_games(n=3)
    context = {
        'message': message,
        'score_board': score_board
    }
    return render(request, 'index.html', context)

def game_view(request, game=None, entry=None):
    game = game if game else GameLogic()
    if entry:
        game_score, message = game.roll_a_ball(entry=entry)
    else:
        game_score, message = None, 'No Message' ###
    context = {
        'game': game,
        'game_score': game_score,
        'message': message
    }
    return render(request, 'game_view.html', context)
