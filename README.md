# 2048 AI Bot (Python + OpenCV + PyAutoGUI)

This project is an **AI bot that plays the 2048 game automatically** by reading the board with OCR and applying heuristic strategies.

## Features
- Uses **PyAutoGUI** to capture the game board and simulate swipe moves.
- Uses **OpenCV + Tesseract OCR** to recognize the numbers on the 2048 tiles.
- AI strategy is based on **heuristics**:
  - Favor keeping the highest tile in the bottom-left corner.
  - Prefer boards with more empty cells.
  - Penalize "rough" boards with large differences between adjacent tiles.
- Automatically performs moves (`up`, `down`, `left`, `right`) by dragging the mouse.

---

## Requirements

### Python packages
Install dependencies with:
```bash
pip install opencv-python pyautogui pytesseract numpy
```

### Tesseract OCR
- Download and install Tesseract OCR:  
  [Tesseract for Windows (UB Mannheim)](https://github.com/UB-Mannheim/tesseract/wiki)  
- After installation, set the path in code:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```

---

## Setup

1. Open your browser and run the 2048 game (e.g., [https://play2048.co/](https://play2048.co/)).
2. Make sure:
   - Screen resolution: **2560x1600**
   - Windows scaling: **150%**
   - Browser zoom: **100%**
3. Adjust coordinates if necessary in the code:
   ```python
   x1, y1, x2, y2 = 1016, 541, 1539, 1061
   ```

---

## Run

Start the bot:
```bash
python main.py
```

The script will:
1. Wait 5 seconds for you to switch to the game window.
2. Continuously read the board with OCR.
3. Choose the best move based on heuristics.
4. Perform the move by dragging the mouse.

---

## Example Output
```
You have 5 seconds to open the game window...
OCR board result:
[0, 0, 0, 2]
[0, 4, 0, 8]
[16, 32, 0, 0]
[128, 256, 512, 1024]
Move executed: DOWN
```

---

## Notes
- OCR may sometimes misread numbers (e.g., "32" as "37"). Better training or template-matching can improve accuracy.
- The coordinates are **hardcoded** for a specific screen setup. If your setup is different, re-measure the top-left and bottom-right corners of the board.
- Move speed is adjustable by changing the `duration` in:
  ```python
  pyautogui.dragRel(..., duration=0.1)
  ```

---

## License
MIT License
