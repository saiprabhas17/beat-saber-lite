import cv2
import time
import json
import pygame
from arm_tracker import ArmTracker
from game_logic import Game, Block

# ========== Load Beatmap ==========
try:
    with open("assets/beatmap.json", "r") as f:
        BEATMAP = json.load(f)
    print(f"✅ Loaded beatmap with {len(BEATMAP)} notes")
except Exception as e:
    print("❌ Error loading beatmap:", e)
    BEATMAP = []

# ========== Audio Setup ==========
pygame.mixer.init()
pygame.mixer.music.load("assets/song.mp3")
slice_sound = pygame.mixer.Sound("assets/hit.wav")

def play_hit():
    slice_sound.play()

def play_music():
    pygame.mixer.music.play()

def get_timestamp(start_time):
    return (pygame.time.get_ticks() - start_time) / 1000.0

# ========== Init ==========
cap = cv2.VideoCapture(0)
tracker = ArmTracker()
game = Game()
trail_left, trail_right = [], []

play_music()
start_ticks = pygame.time.get_ticks()
beat_index = 0
last_fallback_spawn = 0
fallback_mode = False

print("🎮 Game started. ESC to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    left, right = tracker.get_hands(frame)
    left_dir, right_dir = tracker.get_saber_direction()
    current_time = get_timestamp(start_ticks)
    delta = 0.03

    # ========== Beatmap Blocks ==========
    spawned_from_beatmap = False
    while beat_index < len(BEATMAP) and BEATMAP[beat_index]["time"] <= current_time:
        note = BEATMAP[beat_index]
        game.blocks.append(Block(note["x"], direction=note["direction"]))
        print(f"🎵 Beatmap Block Spawned: {note}")
        beat_index += 1
        spawned_from_beatmap = True

    # ========== Fallback Block (Debug Mode) ==========
    if not spawned_from_beatmap and current_time - last_fallback_spawn > 3:
        game.spawn_block()
        print("🧪 Fallback Block Spawned")
        last_fallback_spawn = current_time
        fallback_mode = True

    # ========== Game Update ==========
    game.update(delta)

    # ========== Hit Detection ==========
    for block in game.blocks:
        for hand, direction in [(left, left_dir), (right, right_dir)]:
            if block.collides_with(hand) and direction == block.direction:
                block.mark_hit()
                game.score += 10
                game.combo += 1
                play_hit()
                print(f"✅ Block hit with {direction}!")
                break

    # ========== Draw Saber Trails ==========
    for trail, point in [(trail_left, left), (trail_right, right)]:
        if point:
            trail.append(point)
            if len(trail) > 15:
                trail.pop(0)
            for i in range(1, len(trail)):
                cv2.line(frame, trail[i-1], trail[i], (255, 255, 255), 2)

    # ========== Draw Blocks ==========
    for block in game.blocks:
        color = (0, 255, 0) if block.active else (80, 80, 80)
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

    # ========== HUD ==========
    cv2.putText(frame, f"Score: {game.score}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    if fallback_mode:
        cv2.putText(frame, "DEBUG: Fallback Block Mode",
                    (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    if game.game_over:
        cv2.putText(frame, "GAME OVER", (200, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    cv2.imshow("Beat Saber Clone (Debug)", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
