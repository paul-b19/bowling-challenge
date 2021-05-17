from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


class Player(BaseModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Game(BaseModel):
    title = models.CharField(max_length=50)
    game_score = models.IntegerField(default=0)
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Game: {self.title}, Score: {self.game_score}'


class Frame(BaseModel):
    frame_number = models.IntegerField()
    frame_score = models.IntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Ball(BaseModel):
    ball_number = models.IntegerField()
    ball_result = models.CharField(max_length=1)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
