import pygame
import random
import math

class FireworkParticle:
    def __init__(self, x, y, color, screen):
        self.x, self.y = x, y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.alive = True
        self.screen = screen

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.99
        self.vy *= 0.99
        self.vy += 0.2
        if self.vx**2 + self.vy**2 < 0.1**2:
            self.alive = False

    def draw(self):
        if self.alive:
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), 3)