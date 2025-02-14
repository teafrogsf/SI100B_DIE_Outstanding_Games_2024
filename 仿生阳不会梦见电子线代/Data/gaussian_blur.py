import pygame
import numpy as np
from scipy.ndimage import gaussian_filter

pygame.init()

def pygame_to_numpy(surface):
    return np.array(pygame.surfarray.array3d(surface)).transpose([1, 0, 2])

def numpy_to_pygame(array):
    return pygame.surfarray.make_surface(array.transpose([1, 0, 2]))

def apply_gaussian_blur(surface, sigma=4.0):
    array = pygame_to_numpy(surface)
    blurred_array = np.zeros_like(array)
    for i in range(3):
        blurred_array[:, :, i] = gaussian_filter(array[:, :, i], sigma=sigma)
    return numpy_to_pygame(blurred_array)