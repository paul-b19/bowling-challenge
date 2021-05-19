from datetime import datetime
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Game(BaseModel):
    title = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)

    def __str__(self):
        frame = self.frame_set.filter(frame_number=10, frame_closed=True).first()
        score = frame.frame_score if frame else 'Game is not completed'
        return f'Game: {self.title}, Score: {score}'

    @classmethod
    def create_game(cls):
        game = cls.objects.create(
            title=datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
        )
        return game

    @staticmethod
    def fetch_game(game):
        frame_qs = Frame.fetch_all_frames(game=game)
        game_list = list()
        for i in frame_qs:
            temp_dict = {
                'frame_score': i.frame_score,
                'balls': [(b.ball_number, b.ball_result) for b in i.ball_set.order_by('ball_number')]
            }
            game_list.append(temp_dict)
        return game_list

    @classmethod
    def fetch_n_latest_games(cls, n):
        games_qs = cls.objects.filter(completed=True).order_by('-created')[:n]
        games_list = list()
        for i in games_qs:
            games_list.append(cls.fetch_game(i))
        return games_list


class Frame(BaseModel):
    frame_number = models.IntegerField()
    frame_score = models.IntegerField(default=0)
    frame_closed = models.BooleanField(default=False)
    bonus_rolls = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    @classmethod
    def add_frame(cls, game, frame_number, frame_score=0):
        frame = cls.objects.create(
            frame_number=frame_number,
            frame_score=frame_score,
            game=game
        )
        return frame

    @classmethod
    def fetch_all_frames(cls, game):
        frame_qs = cls.objects.filter(game=game).prefetch_related('ball_set').order_by('frame_number')
        return frame_qs

    @classmethod
    def fetch_open_frames(cls, game):
        frame_qs = cls.objects.filter(game=game, frame_closed=False).order_by('frame_number')
        return frame_qs


class Ball(BaseModel):
    ball_number = models.IntegerField()
    ball_result = models.CharField(max_length=1)
    ball_points = models.IntegerField(default=0)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)

    @classmethod
    def add_ball(cls, frame, ball_number, ball_result, ball_points):
        ball = cls.objects.create(
            ball_number=ball_number,
            ball_result=ball_result,
            ball_points=ball_points,
            frame=frame
        )
        return ball
