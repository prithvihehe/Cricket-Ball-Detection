import cv2
import csv
from config import *
from roi import apply_corridor_mask
from detector import create_background_subtractor, detect_round_blobs
from io_utils import open_video, create_writer


def run_for_video(x: int):
    INPUT_PATH, OUTPUT_PATH, CSV_PATH = paths_for(x)

    cap, fps, W, H = open_video(INPUT_PATH)
    out = create_writer(OUTPUT_PATH, fps, W, H)

    fg = create_background_subtractor(HISTORY, VAR_THRESHOLD, DETECT_SHADOWS)

    frame_id = 0
    csv_file = open(CSV_PATH, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["frame", "x", "y", "visible"])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if SKIP_FRAMES and (frame_id % 2 == 1):
            frame_id += 1
            continue

        small = cv2.resize(frame, (0, 0), fx=SCALE, fy=SCALE)

        mask = fg.apply(small)
        _, mask = cv2.threshold(mask, 180, 255, cv2.THRESH_BINARY)
        mask = cv2.medianBlur(mask, 3)
        mask = cv2.dilate(mask, None, iterations=1)

        mask = apply_corridor_mask(mask, SCALE, W, ROI_LEFT, ROI_RIGHT)

        vis = frame.copy()
        cv2.line(vis, (int(W * ROI_LEFT), 0),
                 (int(W * ROI_LEFT), H), (255, 255, 0), 2)
        cv2.line(vis, (int(W * ROI_RIGHT), 0),
                 (int(W * ROI_RIGHT), H), (255, 255, 0), 2)

        blobs = detect_round_blobs(mask, SCALE, MIN_AREA, MAX_AREA)

        cx_frame, cy_frame, visible = -1, -1, 0

        if blobs:
            blobs_sorted = sorted(blobs, key=lambda b: b[-1], reverse=True)
            c, x0, y0, w, h, cx, cy, area, circ = blobs_sorted[0]

            cx_frame, cy_frame, visible = cx, cy, 1

            cv2.rectangle(vis, (x0, y0), (x0 + w, y0 + h), (0, 255, 0), 2)
            cv2.circle(vis, (cx, cy), 3, (0, 255, 0), -1)
            cv2.drawContours(vis, [c], -1, (0, 0, 255), -1)
            cv2.putText(vis, f"{area:.1f}", (x0, y0 - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 1, cv2.LINE_AA)

        csv_writer.writerow([frame_id, cx_frame, cy_frame, visible])
        out.write(vis)
        frame_id += 1

    cap.release()
    out.release()
    csv_file.close()


if __name__ == "__main__":
    for x in range(1, 16):
        run_for_video(x)
        print(f"Running video {x}")
