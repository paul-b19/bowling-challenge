from bowling_score.models import Ball, Frame, Game


class GameLogic:
    def __init__(self):
        self.game = Game.create_game()
        self.current_frame = Frame.add_frame(game=self.game, frame_number=1)

    def roll_a_ball(self, entry):
        add_frame, error = self.verify_and_process(entry)
        if add_frame:
            self.current_frame = Frame.add_frame(
                game=self.game,
                frame_number=self.current_frame.frame_number + 1,
                frame_score=self.current_frame.frame_score
            )
        current_game = Game.fetch_game(game=self.game)
        print(current_game) ###
        # more logic here
        return current_game, error

    def verify_and_process(self, entry):
        add_frame = False
        if len(entry) != 1 or entry == '0':
            return add_frame, 'Entry is incorrect'
        elif entry.upper() in ['X', '-', '/']:
            return self.process_symbol(entry.upper())
        elif entry.isnumeric():
            return self.process_number(entry)
        else:
            return add_frame, 'Entry is incorrect'

    def process_symbol(self, symbol):
        previous_ball = self.current_frame.ball_set.first()
        add_frame = True
        kwargs = {'frame': self.current_frame, 'ball_result': symbol}
        if (symbol == 'X' and previous_ball) or (symbol == '/' and not previous_ball):
            add_frame = False
            return add_frame, 'Entry is incorrect'
        elif symbol == 'X':
            ball = Ball.add_ball(
                ball_number=1,
                ball_points=10,
                **kwargs
            )
            self.current_frame.bonus_rolls = 2
        elif symbol == '/':
            ball = Ball.add_ball(
                ball_number=2,
                ball_points=10 - previous_ball.ball_points,
                **kwargs
            )
            self.current_frame.bonus_rolls = 1
        elif symbol == '-':
            ball = Ball.add_ball(
                ball_number=2 if previous_ball else 1,
                ball_points=0,
                **kwargs
            )
            add_frame = True if previous_ball else False
        self.current_frame.save()
        self.add_to_open_frames(points=ball.ball_points)
        return add_frame, None

    def process_number(self, number):
        previous_ball = self.current_frame.ball_set.first()
        add_frame = False
        kwargs = {'frame': self.current_frame, 'ball_result': number, 'ball_points': int(number)}
        if not previous_ball:
            ball = Ball.add_ball(ball_number=1, **kwargs)
        elif int(number) > 9 - previous_ball.ball_points:
            return add_frame, 'Entry is incorrect'
        else:
            ball = Ball.add_ball(ball_number=2, **kwargs)
            add_frame = True
        self.add_to_open_frames(points=ball.ball_points)
        return add_frame, None

    def process_10th_frame(self):
        pass

    def add_to_open_frames(self, points):
        frame_qs = Frame.fetch_all_frames(self.game)
        temp_score = 0
        previous_frame_closed = True
        for i in frame_qs:
            if i.frame_closed:
                continue
            i.frame_score = i.frame_score + points + temp_score
            temp_score += points
            if i.rolls_left == 0 and i.bonus_rolls == 0 and previous_frame_closed:
                i.frame_closed = True
            i.bonus_rolls = i.bonus_rolls - 1 if i.bonus_rolls > 0 else 0
            i.rolls_left = i.rolls_left - 1 if i.rolls_left > 0 else 0
            i.save()
            previous_frame_closed = i.frame_closed
            self.current_frame = i

    def game_over():
        pass
