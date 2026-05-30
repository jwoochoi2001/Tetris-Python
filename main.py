import curses
from game import Game


def safe_addstr(stdscr, y, x, text):
    h, w = stdscr.getmaxyx()

    if y < 0 or y >= h:
        return

    if x < 0:
        text = text[-x:]
        x = 0

    if x >= w:
        return

    if x + len(text) >= w:
        text = text[: w - x - 1]

    try:
        stdscr.addstr(y, x, text)
    except curses.error:
        pass


def show_start_screen(stdscr):

    stdscr.clear()

    h, w = stdscr.getmaxyx()

    start_y = 1

    safe_addstr(stdscr, start_y + 0, 0, '  TTTTTT  EEEEEE  TTTTTT  RRRRRR  IIIIII  SSSSSS')
    safe_addstr(stdscr, start_y + 1, 0, '    TT    EE        TT    RR   RR   II    SS')
    safe_addstr(stdscr, start_y + 2, 0, '    TT    EEEEE     TT    RRRRRR    II    SSSSSS')
    safe_addstr(stdscr, start_y + 3, 0, '    TT    EE        TT    RR  RR    II         SS')
    safe_addstr(stdscr, start_y + 4, 0, '    TT    EEEEEE    TT    RR   RR IIIIII  SSSSSS')

    safe_addstr(stdscr, start_y + 7, 5, '╔════════════════════════════╗')
    safe_addstr(stdscr, start_y + 8, 5, '║        START GAME          ║')
    safe_addstr(stdscr, start_y + 9, 5, '╚════════════════════════════╝')

    safe_addstr(stdscr, start_y + 11, 5, 'Select Difficulty')
    safe_addstr(stdscr, start_y + 13, 7, '[1] Beginner')
    safe_addstr(stdscr, start_y + 14, 7, '[2] Expert')
    safe_addstr(stdscr, start_y + 16, 7, '[Q] Quit')

    safe_addstr(stdscr, start_y + 18, 5, 'Controls')
    safe_addstr(stdscr, start_y + 19, 7, '<- -> : Move')
    safe_addstr(stdscr, start_y + 20, 7, '^     : Rotate')
    safe_addstr(stdscr, start_y + 21, 7, 'v     : Soft Drop')
    safe_addstr(stdscr, start_y + 22, 7, 'Space : Hard Drop')
    safe_addstr(stdscr, start_y + 23, 7, 'P     : Pause')
    safe_addstr(stdscr, start_y + 24, 7, 'C     : Hold')
    safe_addstr(stdscr, start_y + 25, 7, 'Q     : Quit')

    safe_addstr(stdscr, start_y + 28, 5, 'Choose your level: ')

    stdscr.refresh()


def main(stdscr):

    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.nodelay(False)

    while True:

        show_start_screen(stdscr)

        while True:

            key = stdscr.getch()

            if key == ord('1'):
                level = 0
                break

            elif key == ord('2'):
                level = 5
                break

            elif key in [ord('q'), ord('Q')]:
                return

        game = Game(stdscr, level)

        if not game.run():
            break


curses.wrapper(main)