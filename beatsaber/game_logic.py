import random

class Block:
    def __init__(self, x, y=0, direction="down"):
        self.x = x
        self.y = y
        self.size = 40
        self.direction = direction
        self.active = True
        self.hit_flash = 0
        self._hit_grace = 0

    def update(self, delta):
        self.y += 60 * delta  # falling speed
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self._hit_grace > 0:
            self._hit_grace -= 1
            if self._hit_grace <= 0:
                self.active = False

    def collides_with(self, hand):
        if not self.active or not hand:
            return False
        hx, hy = hand
        return abs(self.x - hx) < self.size and abs(self.y - hy) < self.size

    def mark_hit(self):
        self.hit_flash = 3
        self._hit_grace = 3

class Game:
    def __init__(self):
        self.blocks = []
        self.score = 0
        self.combo = 0
        self.health = 100
        self.game_over = False

    def update(self, delta):
        for block in self.blocks:
            block.update(delta)
        self.blocks = [b for b in self.blocks if b.active and b.y < 700]
        if self.health <= 0:
            self.game_over = True

    def spawn_block(self, x=None, direction=None):
        if x is None:
            x = random.choice([100, 200, 300, 400, 500])
        if direction is None:
            direction = random.choice(["up", "down", "left", "right"])
        self.blocks.append(Block(x, y=0, direction=direction))
