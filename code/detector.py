import cv2
import math


def create_background_subtractor(history, var_threshold, detect_shadows):
    return cv2.createBackgroundSubtractorMOG2(
        history=history,
        varThreshold=var_threshold,
        detectShadows=detect_shadows
    )


def detect_round_blobs(mask, scale, min_area, max_area):
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    results = []

    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area or area > max_area:
            continue

        peri = cv2.arcLength(c, True)
        if peri == 0:
            continue

        circularity = 4 * math.pi * area / (peri * peri)
        if circularity < 0.80:
            continue

        c = (c / scale).astype(int)
        x, y, w, h = cv2.boundingRect(c)
        aspr = w / float(h)
        if aspr < 0.8 or aspr > 1.2:
            continue

        cx = x + w // 2
        cy = y + h // 2

        results.append((c, x, y, w, h, cx, cy, area, circularity))

    return results
