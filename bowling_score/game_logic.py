from bowling_score.models import Ball, Frame, Game


class GameLogic:
    def __init__(self):
        self.game = Game.create_game()
        self.current_frame = Frame.add_frame(game=self.game, frame_number=1)

    def roll_a_ball(self, entry):
        add_frame, message = self.verify_and_process(entry)
        completed = self.check_progress()
        add_frame = False if self.current_frame.frame_number == 10 else add_frame
        message = 'Game completed' if completed else message
        if add_frame:
            self.current_frame = Frame.add_frame(
                game=self.game,
                frame_number=self.current_frame.frame_number + 1,
                frame_score=self.current_frame.frame_score
            )
        game_score = Game.fetch_game(game=self.game)
        print(game_score, '\n') ### for test
        return game_score, message

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
        previous_ball = self.current_frame.ball_set.order_by('ball_number').last()
        add_frame, strike_or_spare = True, True
        kwargs = {'frame': self.current_frame, 'ball_result': symbol}

        if (symbol == 'X' and self.current_frame.frame_number != 10 and self.current_frame.rolls_left < 2) \
        or (symbol == '/' and self.current_frame.rolls_left > 1):
            add_frame = False
            return add_frame, 'Entry is incorrect'
        elif symbol == 'X':
            ball = Ball.add_ball(
                ball_number=previous_ball.ball_number + 1 if previous_ball else 1,
                ball_points=10,
                **kwargs
            )
            self.current_frame.bonus_rolls = 2
            if self.current_frame.frame_number != 10:
                self.current_frame.rolls_left = 1
        elif symbol == '/':
            ball = Ball.add_ball(
                ball_number=previous_ball.ball_number + 1,
                ball_points=10 - previous_ball.ball_points,
                **kwargs
            )
            self.current_frame.bonus_rolls = 1
        elif symbol == '-':
            ball = Ball.add_ball(
                ball_number=previous_ball.ball_number + 1 if previous_ball else 1,
                ball_points=0,
                **kwargs
            )
            strike_or_spare = False
            add_frame = True if self.current_frame.rolls_left < 2 else False
        self.current_frame.save()
        self.add_to_open_frames(points=ball.ball_points, strike_or_spare=strike_or_spare)
        return add_frame, None

    def process_number(self, number):
        previous_ball = self.current_frame.ball_set.order_by('ball_number').last()
        add_frame = False
        kwargs = {'frame': self.current_frame, 'ball_result': number, 'ball_points': int(number)}

        if not previous_ball:
            ball = Ball.add_ball(ball_number=1, **kwargs)
        elif previous_ball.ball_result in ['X', '/']:
            ball = Ball.add_ball(ball_number=previous_ball.ball_number + 1, **kwargs)
        elif int(number) > 9 - previous_ball.ball_points:
            return add_frame, 'Entry is incorrect'
        else:
            ball = Ball.add_ball(ball_number=previous_ball.ball_number + 1, **kwargs)
            add_frame = True
        self.add_to_open_frames(points=ball.ball_points)
        return add_frame, None

    def add_to_open_frames(self, points, strike_or_spare=False):
        frame_qs = Frame.fetch_all_frames(self.game)
        extra_points, temp_frame = 0, None
        previous_frame_closed = True

        for i in frame_qs:
            if i.frame_closed:
                continue
            if i.bonus_rolls and not i.rolls_left:
                i.frame_score = i.frame_score + points + extra_points
                extra_points += points
                i.bonus_rolls = max(i.bonus_rolls - 1, 0)
            if i.rolls_left:
                i.frame_score = i.frame_score + points + extra_points
                i.rolls_left = max(i.rolls_left - 1, 0)
            if not i.rolls_left and not i.bonus_rolls and previous_frame_closed:
                i.frame_closed = True
            i.save()
            previous_frame_closed = i.frame_closed
            temp_frame = i

        if temp_frame.frame_number == 10 and temp_frame.ball_set.count() < 3 and strike_or_spare:
            temp_frame.rolls_left += 1
            temp_frame.frame_closed = False
        elif temp_frame.frame_number == 10 and temp_frame.rolls_left == 0:
            temp_frame.frame_closed = True
        temp_frame.save()
        self.current_frame = temp_frame

    def check_progress(self):
        completed = self.game.frame_set.filter(frame_closed=True).count() == 10
        # score_board = None
        if completed:
            self.game.completed = True
            self.game.save()
            # score_board = Game.fetch_n_latest_games(n=3)
        return completed #, score_board
