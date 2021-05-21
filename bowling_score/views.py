from django.shortcuts import render, redirect
from django.core.cache import cache
from bowling_score.models import *
from bowling_score.game_logic import GameLogic
from bowling_score.forms import EntryForm

def index(request):
    game = cache.get('current_game')
    score_board = Game.fetch_n_latest_games(n=3)
    context = {
        'game_title': game.game.title if game else None,
        'message': 'Game completed' if game else '',
        'score_board': score_board
    }
    return render(request, 'index.html', context)

def game_view(request):
    if request.method == 'GET':
        game = GameLogic()
        cache.set('current_game', game)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        game = cache.get('current_game')
        if form.is_valid():
            entry=form.cleaned_data['entry']
            game = game.roll_a_ball(entry=entry)
        if game.game_completed:
            return redirect(index)

    form = EntryForm()

    context = {
        'game_score': game.game_score,
        'message': game.message if game.message else '',
        'form': form,
    }
    return render(request, 'game_view.html', context)
