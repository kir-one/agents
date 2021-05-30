import random
from config import *

class Pipe:
    GAP = random.randrange(160, 171)
    VEL = 2

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(the_pipe, False, True)
        self.pipe_bottom = the_pipe

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 451)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_distance = (self.x - bird.x, self.top - round(bird.y))
        bottom_distance = (self.x - bird.x, self.bottom - round(bird.y))

        # determina si no ha habido algún roze con cualquiera de las 2 tuberías
        b_point = bird_mask.overlap(bottom_mask, bottom_distance)
        t_point = bird_mask.overlap(top_mask, top_distance)

        if t_point or b_point:
            return True

        return False