import cv2
import time
from arm_tracker import ArmTracker
from game_logic import Game, Block

# Init
cap = cv2.VideoCapture(0)
tracker = ArmTracker()
game = Game()

trail_left = []
trail_right = []

last_spawn_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    left, right = tracker.get_hands(frame)
    left_dir, right_dir = tracker.get_saber_direction()

    # Spawn a block every 2 seconds
    if time.time() - last_spawn_time > 2:
        game.spawn_block()
        last_spawn_time = time.time()

    # Update game
    delta = 0.03  # 30ms per frame approx
    game.update(delta)

    # Hit detection
    for block in game.blocks:
        for hand, direction in [(left, left_dir), (right, right_dir)]:
            if block.collides_with(hand) and direction == block.direction:
                block.mark_hit()
                game.score += 10
                game.combo += 1
                break

    # Draw trails
    for trail, point in [(trail_left, left), (trail_right, right)]:
        if point:
            trail.append(point)
            if len(trail) > 15:
                trail.pop(0)
            for i in range(1, len(trail)):
                cv2.line(frame, trail[i-1], trail[i], (255, 255, 255), 2)

    # Draw blocks
    for block in game.blocks:
        color = (0, 255, 0) if block.active else (100, 100, 100)
        if block.hit_flash > 0:
            color = (255, 255, 255)
        cv2.rectangle(
            frame,
            (int(block.x - block.size / 2), int(block.y - block.size / 2)),
            (int(block.x + block.size / 2), int(block.y + block.size / 2)),
            color,
            -1
        )
        cv2.putText(frame, block.direction[0].upper(),
                    (int(block.x - 10), int(block.y + 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # HUD
    cv2.putText(frame, f"Score: {game.score}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    if game.game_over:
        cv2.putText(frame, "GAME OVER", (200, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    cv2.imshow("Beat Saber Clone", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
