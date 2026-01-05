import cv2
import numpy as np

BG_COLOR = (192, 192, 192)

def remove_background(frame: np.ndarray) -> np.ndarray:
    if frame is None:
        return frame

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
    fg = cv2.bitwise_and(frame, frame, mask=mask)

    bg = np.zeros_like(frame)
    bg[:] = BG_COLOR

    # ghép foreground + background
    inv_mask = cv2.bitwise_not(mask)
    bg_part = cv2.bitwise_and(bg, bg, mask=inv_mask)

    output = cv2.add(fg, bg_part)
    return output
