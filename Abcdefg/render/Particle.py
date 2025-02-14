import random
from typing import Tuple

import pygame

import I18n
from render import Renderer


class ParticleManager:

    def __init__(self):
        self.particles = []

    def tick(self):
        for i in self.particles:
            i.tick()
            if i.is_end():
                self.particles = [i for i in self.particles if not i.is_end()]

    def render(self, screen, font: pygame.font.Font, camera=None):
        for i in self.particles:
            i.render_wrapper(screen, font, camera)

    def add(self, particle):
        self.particles.append(particle)

    def clear(self):
        self.particles.clear()


UI_PARTICLES = ParticleManager()
ENV_PARTICLES = ParticleManager()


class Particle:

    def __init__(self, pos, duration):
        self.pos = pos
        self.duration = duration
        self.timer = 0

    def tick(self):
        self.timer = min(self.timer + 1, self.duration)

    def is_end(self):
        return self.timer >= self.duration

    def render_wrapper(self, screen, font: pygame.font.Font, camera=None):
        if camera is not None:
            self.render(screen, font, (self.pos[0] - camera[0], self.pos[1] - camera[1]))
        else:
            self.render(screen, font, self.pos)

    def render(self, screen, font: pygame.font.Font, base_pos: Tuple[int, int]):
        pass


class DamageParticle(Particle):

    def __init__(self, damage, pos, duration, is_crt=False, color=(255, 0, 0)):
        super().__init__(pos, duration)
        self.damage = damage
        self.color = color
        self.alpha = 255
        self.is_crt = is_crt
        self.delta_y = 0

    def tick(self):
        super().tick()
        self.delta_y -= 1
        self.alpha -= 255 / self.duration

    def render(self, screen, font: pygame.font.Font, base_pos: Tuple[int, int]):
        txt_surface = font.render(
            (I18n.text('crt_hit').get() + ' ' if self.is_crt else '') + ('+' if self.damage < 0 else '')
            + f"{-self.damage:.0f}", True, self.color)
        txt_surface.set_alpha(max(0, int(self.alpha)))
        screen.blit(txt_surface, (base_pos[0], base_pos[1] + self.delta_y))


class AnimationParticle(Particle):

    def __init__(self, images, pos, duration, repeat_times=1):
        super().__init__(pos, duration)
        self.images = images
        self.index = 0
        self.repeat_times = repeat_times

    def tick(self):
        if self.repeat_times > 1 and self.timer == self.duration - 1:
            self.timer = 0
            self.repeat_times -= 1
        super().tick()
        self.index = min(self.timer * (len(self.images) - 1) // self.duration, len(self.images) - 1)

    def render(self, screen, font: pygame.font.Font, base_pos: Tuple[int, int]):
        screen.blit(self.images[self.index], base_pos)


class LaserCannonParticle(AnimationParticle):

    def __init__(self, pos, duration):
        super().__init__(LASER_CANNON, pos, duration, 9)


class ExplosionParticle(AnimationParticle):

    def __init__(self, pos, duration):
        super().__init__(EXPLOSION, pos, duration)


class ClickParticle(AnimationParticle):

    def __init__(self, pos, duration):
        super().__init__(CLICK, pos, duration)


class SplashParticle(AnimationParticle):

    def __init__(self, pos, duration):
        super().__init__(SPLASH, pos, duration)


class ImageParticle(Particle):

    def __init__(self, image, pos, duration):
        super().__init__(pos, duration)
        self.image = image

    def render(self, screen, font: pygame.font.Font, base_pos: Tuple[int, int]):
        screen.blit(self.image, base_pos)


class LavaParticle(ImageParticle):

    def __init__(self, pos, duration):
        super().__init__(LAVA, pos, duration)
        self.start_pos = pos
        self.end_pos = (pos[0] + random.randint(-40, 40), pos[1] + random.randint(-40, 40))
        self.peak_height = random.randint(10, 20)

    def tick(self):
        super().tick()
        t = self.timer / self.duration
        x = self.start_pos[0] + t * (self.end_pos[0] - self.start_pos[0])
        y = self.start_pos[1] + t * (self.end_pos[1] - self.start_pos[1]) - self.peak_height * (4 * t * (1 - t))
        self.pos = (x, y)


class GlintParticle(ImageParticle):

    def __init__(self, pos, duration):
        super().__init__(GLINT, pos, duration)
        self.delta_y = -0.2

    def tick(self):
        super().tick()
        self.pos = (self.pos[0], self.pos[1] + self.delta_y)


class WalkParticle(ImageParticle):

    def __init__(self, pos, duration):
        super().__init__(WALK, pos, duration)


class CriticalHitParticle(ImageParticle):

    def __init__(self, pos, duration):
        super().__init__(random.choice([CRITICAL_HIT, CRITICAL_HIT_YELLOW, CRITICAL_HIT_RED, CRITICAL_HIT_GREEN]),
                         pos, duration)
        self.vel_x = random.uniform(-10, 10)
        self.vel_y = random.uniform(-10, 10)

    def tick(self):
        super().tick()
        self.pos = (self.pos[0] + self.vel_x, self.pos[1] + self.vel_y)


class LifeStealingParticle(ImageParticle):

    def __init__(self, pos, duration):
        super().__init__(HEART, pos, duration)
        self.start_pos = pos
        self.end_pos = (pos[0] - 400, pos[1])

    def tick(self):
        super().tick()
        t = self.timer / self.duration
        x = self.start_pos[0] + t * (self.end_pos[0] - self.start_pos[0])
        self.pos = (x, self.pos[1])


class ArrowParticle(ImageParticle):

    def __init__(self, pos, duration):
        super().__init__(ARROW, pos, duration)
        self.start_pos = pos
        self.end_pos = (pos[0] - 400, pos[1])

    def tick(self):
        super().tick()
        t = self.timer / self.duration
        x = self.start_pos[0] + t * (self.end_pos[0] - self.start_pos[0])
        self.pos = (x, self.pos[1])


class TntParticle(ImageParticle):

    def __init__(self, pos, duration):
        super().__init__(TNT, pos, duration)
        self.start_pos = pos
        self.end_pos = (pos[0] + 400, pos[1])
        self.peak_height = random.randint(100, 180)

    def tick(self):
        super().tick()
        t = self.timer / self.duration
        x = self.start_pos[0] + t * (self.end_pos[0] - self.start_pos[0])
        y = self.start_pos[1] - self.peak_height * (4 * t * (1 - t))
        self.pos = (x, y)


LASER_CANNON = Renderer.load_images_from_sprite('./assets/particles/laser_cannon.png', (398, 102), (398, 102))
EXPLOSION = Renderer.load_images_from_sprite('./assets/particles/explosion.png', (32, 32), (64, 64))
CLICK = Renderer.load_images_from_sprite('./assets/particles/click.png', (32, 32), (32, 32))
SPLASH = Renderer.load_images_from_sprite('./assets/particles/splash.png', (8, 8), (16, 16))
LAVA = Renderer.load_image('particles/lava.png', (8, 8))
GLINT = Renderer.load_image('particles/glint.png', (16, 16))
WALK = Renderer.load_image('particles/walk.png', (4, 4))
CRITICAL_HIT = Renderer.load_image('particles/critical_hit.png', (8, 8))
CRITICAL_HIT_YELLOW = Renderer.load_image('particles/critical_hit_yellow.png', (8, 8))
CRITICAL_HIT_RED = Renderer.load_image('particles/critical_hit_red.png', (8, 8))
CRITICAL_HIT_GREEN = Renderer.load_image('particles/critical_hit_green.png', (8, 8))
HEART = Renderer.load_image('particles/heart.png', (20, 20))
ARROW = Renderer.load_image('particles/arrow.png', (32, 10))
TNT = Renderer.load_image('particles/tnt.png', (32, 32))
