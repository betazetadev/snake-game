import curses
from random import randint
import sys

def main(stdscr):
    curses.initscr()
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    # Initialize game variables
    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    food = None
    score = 0

    # Initialize game settings
    key = curses.KEY_RIGHT
    speed = 100
    game_over_flag = False

    while True:
        next_key = w.getch()
        
        if next_key == -1:
            pass  # No new key, keep moving in the current direction
        elif (
            (key == curses.KEY_DOWN and next_key != curses.KEY_UP) or
            (key == curses.KEY_UP and next_key != curses.KEY_DOWN) or
            (key == curses.KEY_LEFT and next_key != curses.KEY_RIGHT) or
            (key == curses.KEY_RIGHT and next_key != curses.KEY_LEFT)
        ):
            key = next_key  # Update the direction only if it's not the opposite
        
        if game_over_flag:
            break  # Exit the loop if the game is over

        # Check if the snake hit the wall or itself
        if (
            snake[0][0] in [0, sh - 1] or
            snake[0][1] in [0, sw - 1] or
            snake[0] in snake[1:]
        ):
            game_over(w, score)
            game_over_flag = True  # Set the game over flag
            continue

        new_head = [snake[0][0], snake[0][1]]

        # Move the snake based on the current direction
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        # Generate new food if it's not present
        if food is None:
            while True:
                nf = [
                    randint(1 + 1, sh - 2),  # Add margin from the top and bottom
                    randint(1 + 1, sw - 2)  # Add margin from the left and right
                ]
                if nf not in snake:
                    food = nf
                    break

            w.addch(food[0], food[1], curses.ACS_PI)

        # Insert new snake head and check if food was eaten
        snake.insert(0, new_head)
        if snake[0] == food:
            score += 1
            food = None
            w.addstr(0, 2, f'Score: {score} ')
            w.refresh()
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        # Draw snake
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

        # Speed control
        if score >= 5:
            speed = 75
        if score >= 10:
            speed = 50

        w.timeout(speed)

def game_over(w, score):
    w.clear()
    sh, sw = w.getmaxyx()
    msg = f"Game Over! Your Score: {score} Press any key to exit."
    w.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
    w.refresh()
    w.getch()
    sys.exit()

if __name__ == "__main__":
    curses.wrapper(main)

