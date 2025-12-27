import os

DATA_ROOT = r"C:\Users\prith\OneDrive\Desktop\IIT\EdgeFleet_Assignment"

SCALE = 0.5
MIN_AREA = 32
MAX_AREA = 300
SKIP_FRAMES = 0

HISTORY = 120
VAR_THRESHOLD = 25
DETECT_SHADOWS = False

ROI_LEFT = 0.30
ROI_RIGHT = 0.70


def paths_for(x: int):
    if x == 1:
        input_path = rf"{DATA_ROOT}\data\1.mp4"
    else:
        input_path = rf"{DATA_ROOT}\data\{x}.mov"
    output_path = rf"{DATA_ROOT}\results\output_fast_blobs{x}.mp4"
    csv_path = rf"{DATA_ROOT}\annotations\ball_annotations{x}.csv"
    return input_path, output_path, csv_path
