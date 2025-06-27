import cv2
import numpy as np

class ArmTracker:
    def __init__(self):
        self.prev_left = None
        self.prev_right = None
        self.curr_left = None
        self.curr_right = None

    def get_hands(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (160, 100, 100), (179, 255, 255))
        mask = cv2.bitwise_or(mask1, mask2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        hands = []
        for cnt in contours:
            if cv2.contourArea(cnt) > 300:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    hands.append((cx, cy))

        hands = sorted(hands, key=lambda x: x[0])
        self.prev_left = self.curr_left
        self.prev_right = self.curr_right
        self.curr_left = hands[0] if len(hands) > 0 else None
        self.curr_right = hands[1] if len(hands) > 1 else None

        return self.curr_left, self.curr_right

    def get_saber_direction(self):
        def direction(prev, curr):
            if not prev or not curr:
                return None
            dx = curr[0] - prev[0]
            dy = curr[1] - prev[1]
            if abs(dx) > abs(dy):
                return "right" if dx > 0 else "left"
            else:
                return "down" if dy > 0 else "up"
        return direction(self.prev_left, self.curr_left), direction(self.prev_right, self.curr_right)
