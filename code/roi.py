def apply_corridor_mask(mask, scale, w, roi_left, roi_right):
    rx1 = int(w * roi_left * scale)
    rx2 = int(w * roi_right * scale)
    mask[:, :rx1] = 0
    mask[:, rx2:] = 0
    return mask
