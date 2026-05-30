import curses
import random
import time

from block import BLOCK_SHAPES
from color import init_colors


class Game:

    WIDTH = 12
    HEIGHT = 22

    def __init__(self, stdscr, level=0):

        init_colors()

        self.stdscr = stdscr
        self.level = level
        self.level = level

        if level == 0:
            self.difficulty = "Beginner"
        elif level == 5:
            self.difficulty = "Expert"
        else:
            self.difficulty = "Custom"

        self.score = 0
        self.lines = 0

        self.game_over = False
        self.back_to_menu = False

        self.board = [[0] * self.WIDTH for _ in range(self.HEIGHT)]

        for y in range(self.HEIGHT):
            self.board[y][0] = 1
            self.board[y][self.WIDTH - 1] = 1

        # 진짜 7-bag 시스템
        self.bag = []

        self.next_piece = self.get_random_piece()

        self.hold_piece = None
        self.can_hold = True

        self.lock_delay = 0.20
        self.lock_start = None

        self.spawn_block()

    # -----------------------------
    # 진짜 7-bag 시스템
    # -----------------------------
    def get_random_piece(self):

        if len(self.bag) == 0:

            self.bag = [0, 1, 2, 3, 4, 5, 6]
            random.shuffle(self.bag)

        return self.bag.pop()

    def spawn_block(self):

        self.cur_piece = self.next_piece
        self.next_piece = self.get_random_piece()

        self.cur_x = self.WIDTH // 2 - 2
        self.cur_y = 0
        self.cur_rot = 0

        self.lock_start = None
        self.can_hold = True

        if self.check_collision(self.cur_x, self.cur_y, self.cur_rot):
            self.game_over = True

    def hold_current_piece(self):

        if not self.can_hold:
            return

        self.can_hold = False

        if self.hold_piece is None:

            self.hold_piece = self.cur_piece
            self.spawn_block()

        else:

            temp = self.cur_piece
            self.cur_piece = self.hold_piece
            self.hold_piece = temp

            self.cur_x = self.WIDTH // 2 - 2
            self.cur_y = 0
            self.cur_rot = 0

            self.lock_start = None

    def check_collision(self, x, y, rot):

        shape = BLOCK_SHAPES[self.cur_piece][rot]

        for i in range(4):
            for j in range(4):

                if shape[i][j]:

                    bx = x + j
                    by = y + i

                    if bx < 0 or bx >= self.WIDTH:
                        return True

                    if by >= self.HEIGHT:
                        return True

                    if self.board[by][bx]:
                        return True

        return False

    def rotate(self):

        new_rot = (self.cur_rot + 1) % 4

        if not self.check_collision(
                self.cur_x,
                self.cur_y,
                new_rot
        ):

            self.cur_rot = new_rot
            self.lock_start = None
            return

        for dx in [-1, 1, -2, 2]:

            if not self.check_collision(
                    self.cur_x + dx,
                    self.cur_y,
                    new_rot
            ):

                self.cur_x += dx
                self.cur_rot = new_rot
                self.lock_start = None
                return

    def move(self, dx):

        if not self.check_collision(
                self.cur_x + dx,
                self.cur_y,
                self.cur_rot
        ):

            self.cur_x += dx
            self.lock_start = None

    def hard_drop(self):

        while not self.check_collision(
                self.cur_x,
                self.cur_y + 1,
                self.cur_rot
        ):
            self.cur_y += 1

        self.fix_block()

    def fix_block(self):

        shape = BLOCK_SHAPES[self.cur_piece][self.cur_rot]

        for y in range(4):
            for x in range(4):

                if shape[y][x]:
                    self.board[self.cur_y + y][self.cur_x + x] = self.cur_piece + 1

        self.clear_lines()
        self.spawn_block()

    def clear_lines(self):

        y = self.HEIGHT - 1

        while y > 0:

            full = True

            for x in range(1, self.WIDTH - 1):

                if self.board[y][x] == 0:
                    full = False
                    break

            if full:

                self.lines += 1
                self.score += 100 * (self.level + 1)

                if self.lines % 10 == 0:
                    self.level += 1

                for row in range(y, 0, -1):

                    for col in range(1, self.WIDTH - 1):
                        self.board[row][col] = self.board[row - 1][col]

                for col in range(1, self.WIDTH - 1):
                    self.board[0][col] = 0

            else:
                y -= 1

    def get_ghost_y(self):

        ghost_y = self.cur_y

        while not self.check_collision(
                self.cur_x,
                ghost_y + 1,
                self.cur_rot
        ):
            ghost_y += 1

        return ghost_y

    def draw_preview_piece(self, piece, box_y, box_x):

        shape = BLOCK_SHAPES[piece][0]

        preview_offsets = {

            0: (0, 1),
            1: (2, 1),
            2: (0, 1),
            3: (0, 1),
            4: (1, 1),
            5: (1, 1),
            6: (1, 1)
        }

        offset_x, offset_y = preview_offsets[piece]

        color = curses.color_pair(piece + 1)

        for y in range(4):
            for x in range(4):

                if shape[y][x]:

                    draw_x = (
                            box_x
                            + offset_x
                            + (x * 2)
                    )

                    draw_y = (
                            box_y
                            + offset_y
                            + y
                    )

                    self.stdscr.addstr(
                        draw_y,
                        draw_x,
                        '[]',
                        color
                    )

    def draw_hold_block(self):

        start_y = 6
        start_x = 30

        self.stdscr.addstr(start_y, start_x, '╔══════════╗')
        self.stdscr.addstr(start_y + 1, start_x, '║   HOLD   ║')
        self.stdscr.addstr(start_y + 2, start_x, '║          ║')

        for i in range(3, 6):
            self.stdscr.addstr(start_y + i, start_x, '║          ║')

        self.stdscr.addstr(start_y + 6, start_x, '╚══════════╝')

        if self.hold_piece is not None:

            self.draw_preview_piece(
                self.hold_piece,
                start_y + 2,
                start_x + 2
            )

    def draw_next_block(self):

        start_y = 15
        start_x = 30

        self.stdscr.addstr(start_y, start_x, '╔══════════╗')
        self.stdscr.addstr(start_y + 1, start_x, '║   NEXT   ║')
        self.stdscr.addstr(start_y + 2, start_x, '║          ║')

        for i in range(3, 6):
            self.stdscr.addstr(start_y + i, start_x, '║          ║')

        self.stdscr.addstr(start_y + 6, start_x, '╚══════════╝')

        self.draw_preview_piece(
            self.next_piece,
            start_y + 2,
            start_x + 2
        )

    def draw_ui(self):

        self.stdscr.addstr(0, 0, '  TTTTTT  EEEEEE  TTTTTT  RRRRRR  IIIIII  SSSSSS')
        self.stdscr.addstr(1, 0, '    TT    EE        TT    RR   RR   II    SS')
        self.stdscr.addstr(2, 0, '    TT    EEEEE     TT    RRRRRR    II    SSSSSS')
        self.stdscr.addstr(3, 0, '    TT    EE        TT    RR  RR    II         SS')
        self.stdscr.addstr(4, 0, '    TT    EEEEEE    TT    RR   RR IIIIII  SSSSSS')

        self.stdscr.addstr(24, 30, f'Score : {self.score}')
        self.stdscr.addstr(25, 30, f'Level : {self.level}')
        self.stdscr.addstr(26, 30, f'Lines : {self.lines}')
        self.stdscr.addstr(27, 30, f'Mode  : {self.difficulty}')

        self.stdscr.addstr(29, 30, 'Controls')
        self.stdscr.addstr(30, 30, '<- -> : Move')
        self.stdscr.addstr(31, 30, '^     : Rotate')
        self.stdscr.addstr(32, 30, 'v     : Soft Drop')
        self.stdscr.addstr(33, 30, 'Space : Hard Drop')
        self.stdscr.addstr(34, 30, 'C     : Hold')
        self.stdscr.addstr(35, 30, 'P     : Pause')

        return

    def draw_board_frame(self):

        for y in range(self.HEIGHT):

            self.stdscr.addstr(y + 6, 0, '||')
            self.stdscr.addstr(y + 6, 22, '||')

    def draw_ghost_piece(self):

        ghost_y = self.get_ghost_y()

        if ghost_y <= self.cur_y:
            return

        shape = BLOCK_SHAPES[self.cur_piece][self.cur_rot]

        for y in range(4):
            for x in range(4):

                if shape[y][x]:

                    self.stdscr.addstr(
                        ghost_y + y + 6,
                        (self.cur_x + x - 1) * 2 + 2,
                        '..'
                    )

    def draw_fixed_blocks(self):

        for y in range(self.HEIGHT):
            for x in range(1, self.WIDTH - 1):

                if self.board[y][x]:

                    color = curses.color_pair(self.board[y][x])

                    self.stdscr.addstr(
                        y + 6,
                        (x - 1) * 2 + 2,
                        '[]',
                        color
                    )

                else:

                    self.stdscr.addstr(
                        y + 6,
                        (x - 1) * 2 + 2,
                        '  '
                    )

    def draw_current_piece(self):

        shape = BLOCK_SHAPES[self.cur_piece][self.cur_rot]

        color = curses.color_pair(self.cur_piece + 1)

        for y in range(4):
            for x in range(4):

                if shape[y][x]:

                    self.stdscr.addstr(
                        self.cur_y + y + 6,
                        (self.cur_x + x - 1) * 2 + 2,
                        '[]',
                        color
                    )

    def draw(self):

        self.stdscr.erase()

        self.draw_ui()
        self.draw_board_frame()

        self.draw_hold_block()
        self.draw_next_block()

        self.draw_fixed_blocks()
        self.draw_ghost_piece()
        self.draw_current_piece()

        self.stdscr.refresh()

    def pause_menu(self):

        center_y = 15
        center_x = 2

        self.draw()
        self.stdscr.addstr(center_y, center_x, '╔══════════════════╗')
        self.stdscr.addstr(center_y + 1, center_x, '║      PAUSED      ║')
        self.stdscr.addstr(center_y + 2, center_x, '╠══════════════════╣')

        self.stdscr.addstr(center_y + 3, center_x, '║ [C] Continue     ║')
        self.stdscr.addstr(center_y + 4, center_x, '║ [Q] Quit Menu    ║')

        self.stdscr.addstr(center_y + 5, center_x, '╚══════════════════╝')

        self.stdscr.refresh()

        while True:

            key = self.stdscr.getch()

            if key in [ord('c'), ord('C')]:
                return

            elif key in [ord('q'), ord('Q')]:
                self.back_to_menu = True
                return

    def show_game_over(self):

        self.stdscr.nodelay(False)

        self.stdscr.clear()

        self.stdscr.addstr(10, 8, '╔══════════════════╗')
        self.stdscr.addstr(11, 8, '║    GAME OVER     ║')
        self.stdscr.addstr(12, 8, '╚══════════════════╝')

        self.stdscr.addstr(14, 8, f'Final Score : {self.score}')
        self.stdscr.addstr(15, 8, f'Difficulty : {self.difficulty}')

        self.stdscr.addstr(17, 8, '[R] Return Menu')

        self.stdscr.refresh()

        while True:

            key = self.stdscr.getch()

            if key in [ord('r'), ord('R')]:
                self.back_to_menu = True
                return

    def run(self):

        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)

        last_fall = time.time()

        while not self.game_over and not self.back_to_menu:

            key = self.stdscr.getch()

            if key == curses.KEY_LEFT:
                self.move(-1)

            elif key == curses.KEY_RIGHT:
                self.move(1)

            elif key == curses.KEY_UP:
                self.rotate()

            elif key == curses.KEY_DOWN:

                if not self.check_collision(
                        self.cur_x,
                        self.cur_y + 1,
                        self.cur_rot
                ):
                    self.cur_y += 1

            elif key == ord(' '):
                self.hard_drop()

            elif key in [ord('c'), ord('C')]:
                self.hold_current_piece()

            elif key in [ord('p'), ord('P')]:
                self.pause_menu()

            now = time.time()

            speed = max(0.03, 0.5 - (self.level * 0.045))

            if now - last_fall > speed:

                if not self.check_collision(
                        self.cur_x,
                        self.cur_y + 1,
                        self.cur_rot
                ):

                    self.cur_y += 1
                    self.lock_start = None

                else:

                    if self.lock_start is None:
                        self.lock_start = time.time()

                    elif time.time() - self.lock_start >= self.lock_delay:
                        self.fix_block()

                last_fall = now

            self.draw()

            time.sleep(0.016)

        if self.game_over:
            self.show_game_over()

        return self.back_to_menu