import cv2
import numpy as np

# Màu nền sau khi xóa (xám)
BG_COLOR = (192, 192, 192)

def remove_background(frame: np.ndarray) -> np.ndarray:
    """
    Input : frame BGR (OpenCV)
    Output: frame BGR đã xóa nền
    """

    if frame is None:
        return frame

    # Chuyển sang grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Tạo mask đơn giản (foreground sáng)
    _, mask = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)

    # Foreground
    fg = cv2.bitwise_and(frame, frame, mask=mask)

    # Background
    bg = np.zeros_like(frame)
    bg[:] = BG_COLOR

    # Ghép foreground + background
    inv_mask = cv2.bitwise_not(mask)
    bg_part = cv2.bitwise_and(bg, bg, mask=inv_mask)

    output = cv2.add(fg, bg_part)
    return output
