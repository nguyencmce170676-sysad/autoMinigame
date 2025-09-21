import time
import cv2
import numpy as np
import pyautogui
import pytesseract
import random

# ====== Tesseract setup ======
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ====== OCR for each cell ======
def preprocess_and_ocr(cell_img):
    gray = cv2.cvtColor(cell_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    resized = cv2.resize(thresh, (cell_img.shape[1]*3, cell_img.shape[0]*3))
    config = "--psm 8 -c tessedit_char_whitelist=0123456789"
    text = pytesseract.image_to_string(resized, config=config)
    try:
        return int(text.strip())
    except:
        return 0

def capture_board():
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Coordinates of the board (already measured)
    x1, y1, x2, y2 = 1016, 541, 1539, 1061
    board = frame[y1:y2, x1:x2]

    cell_h = (y2 - y1) // 4
    cell_w = (x2 - x1) // 4

    matrix = []
    for i in range(4):
        row = []
        for j in range(4):
            cell = board[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            number = preprocess_and_ocr(cell)
            row.append(number)
        matrix.append(row)

    return matrix

# ====== Simulation and heuristics ======
def simulate_move(board, move):
    """Return new board after making a move, or None if the move is invalid"""
    new_board = [row[:] for row in board]

    def compress(row):
        new_row = [x for x in row if x != 0]
        merged = []
        skip = False
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                merged.append(new_row[i] * 2)
                skip = True
            else:
                merged.append(new_row[i])
        return merged + [0] * (4 - len(merged))

    rotated = False
    if move == "up":
        new_board = list(map(list, zip(*new_board)))
        rotated = True
    elif move == "down":
        new_board = list(map(list, zip(*new_board[::-1])))
        rotated = True
    elif move == "right":
        new_board = [row[::-1] for row in new_board]

    new_board = [compress(row) for row in new_board]

    if move == "right":
        new_board = [row[::-1] for row in new_board]
    elif move == "down":
        new_board = list(zip(*new_board))[::-1]
        new_board = [list(row) for row in new_board]
    elif move == "up":
        new_board = list(zip(*new_board))
        new_board = [list(row) for row in new_board]

    if new_board == board:
        return None
    return new_board


def heuristic_score(board):
    score = 0
    # Empty cells
    empty = sum(row.count(0) for row in board)
    score += empty * 10

    # Reward if the max tile is at bottom-left corner
    max_tile = max(max(row) for row in board)
    if board[3][0] == max_tile:
        score += 1000

    # Smoothness (penalize big differences between neighbors)
    for row in board:
        for i in range(3):
            score -= abs(row[i] - row[i + 1])
    for j in range(4):
        for i in range(3):
            score -= abs(board[i][j] - board[i + 1][j])

    return score


def choose_move(board):
    moves = ["up", "down", "left", "right"]
    best_move = None
    best_score = -float("inf")

    for move in moves:
        new_board = simulate_move(board, move)
        if new_board is None:
            continue
        score = heuristic_score(new_board)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

# ====== Perform moves with mouse drag ======
def perform_move(move):
    # Board center
    center_x, center_y = (1016 + 1539) // 2, (541 + 1061) // 2
    offset = 200  # drag distance

    pyautogui.moveTo(center_x, center_y, duration=0.05)
    pyautogui.mouseDown()

    if move == "up":
        pyautogui.moveRel(0, -offset, duration=0.1)
    elif move == "down":
        pyautogui.moveRel(0, offset, duration=0.1)
    elif move == "left":
        pyautogui.moveRel(-offset, 0, duration=0.1)
    elif move == "right":
        pyautogui.moveRel(offset, 0, duration=0.1)

    pyautogui.mouseUp()
    print(f"Move executed: {move.upper()}")

# ====== Main loop ======
if __name__ == "__main__":
    print("You have 5 seconds to open the game window...")
    time.sleep(5)

    while True:
        board = capture_board()
        print("OCR board result:")
        for row in board:
            print(row)

        move = choose_move(board)
        if move is None:
            print("No more valid moves. Game over!")
            break

        perform_move(move)
        time.sleep(0.1)  # wait for game update
