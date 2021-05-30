from config import *

class Bird:

    MAX_rotation = 25
    ROT_level = 20
    ANIMATION_time = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        color = random.randrange(0, 3)
        if color == 0:
            self.imgs = yellow_bird
        elif color == 1:
            self.imgs = blue_bird
        else:
            self.imgs = red_bird
        self.img = self.imgs[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        gravity = self.vel*self.tick_count + 1.5*self.tick_count**2
        if gravity >= 16:
            gravity = 16

        if gravity < 0:
            gravity -= 2

        self.y = self.y + gravity

        if gravity < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_rotation:
                self.tilt = self.MAX_rotation

        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_level

    def draw(self, win):
        self.img_count += 1

        # transición
        if self.img_count < self.ANIMATION_time:
            self.img = self.imgs[0]
        elif self.img_count < self.ANIMATION_time*2:
            self.img = self.imgs[1]
        elif self.img_count < self.ANIMATION_time*3:
            self.img = self.imgs[2]
        elif self.img_count < self.ANIMATION_time*4:
            self.img = self.imgs[1]
        elif self.img_count == self.ANIMATION_time*4 + 1:
            self.img = self.imgs[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.ANIMATION_time*2

        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    # contorno de flappy
    def get_mask(self):
        return pygame.mask.from_surface(self.img)