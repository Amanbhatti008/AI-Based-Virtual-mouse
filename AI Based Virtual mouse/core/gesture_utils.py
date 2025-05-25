import math

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def fingers_up(lm_list):
    fingers = []
    if lm_list[8][1] < lm_list[6][1]:   # Index finger
        fingers.append(1)
    else:
        fingers.append(0)

    if lm_list[12][1] < lm_list[10][1]:  # Middle finger
        fingers.append(1)
    else:
        fingers.append(0)

    if lm_list[16][1] < lm_list[14][1]:  # Ring finger
        fingers.append(1)
    else:
        fingers.append(0)

    if lm_list[20][1] < lm_list[18][1]:  # Pinky
        fingers.append(1)
    else:
        fingers.append(0)

    return fingers
