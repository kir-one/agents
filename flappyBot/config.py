import random
import pygame
import os
pygame.font.init()

ancho = 500
largo = 700
ratio_aspect = (ancho, largo)
gen = -1
# pygame.transform.scale2x(pygame.image.load(os.path.join("ruta", "0.png")), (47, 33))

yellow_bird = [pygame.transform.scale2x(pygame.image.load(os.path.join("yellow", "0.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("yellow", "1.png"))),
               pygame.transform.scale2x(pygame.image.load(os.path.join("yellow", "2.png")))]

blue_bird = [pygame.transform.scale2x(pygame.image.load(os.path.join("blue", "0.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("blue", "1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("blue", "2.png")))]

red_bird = [pygame.transform.scale2x(pygame.image.load(os.path.join("red", "0.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("red", "1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("red", "2.png")))]

the_pipe = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
the_base = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
bg_day = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "background_d.png")), (500, 700))
bg_night = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "background_n.png")), (500, 700))
the_stat = pygame.font.SysFont("Bahuaus 93", 66)
