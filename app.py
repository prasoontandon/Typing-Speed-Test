import time
import random
import curses
from curses import wrapper

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        try:
            wpm_test(stdscr)
        except:
            break

        stdscr.addstr(2, 0, "You completed the text! Press ESC to exit. Press any other key to retry.")
        
        user_key = stdscr.getkey()
        if ord(user_key) == 27:
            break

def get_text():
    with open("test_text.txt") as file:
        lines = file.readlines()
        return random.choice(lines).strip()

def text_display(stdscr, current, target, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"Words Per Minute = {wpm}")

    for index, char in enumerate(current):
        letter_color = curses.color_pair(1)
        if char != target[index]:
            letter_color = curses.color_pair(2)

        stdscr.addstr(0, index, char, letter_color)
        
def wpm_test(stdscr):
    target_text = get_text()
    current_text = []
    wpm = 0
    start_time = time.time()

    stdscr.nodelay(True)

    while True:
        elapsed_time = max(1, time.time() - start_time)
        wpm = round((len(current_text) / (elapsed_time / 60)) / 5)


        stdscr.clear()
        text_display(stdscr, current_text, target_text, wpm)
        stdscr.refresh()

        if target_text == "".join(current_text):
            stdscr.nodelay(False)
            break

        try:
            user_key = stdscr.getkey()
        except:
            continue

        if ord(user_key) == 27:
            raise KeyError

        if user_key in ["KEY_BACKSPACE", '\x7f', '\b']:
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(user_key)

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("This is a speed typing test. ALL words have to be spelled correctly!!\n")
    stdscr.addstr("Press any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)