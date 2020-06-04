import pygame
import random
import time

pygame.init()


# game settings
class Settings(object):
    def __init__(self):
        self.run = True
        self.width = 1366
        self.height = 768
        # self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height),
                                              pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        self.photo = pygame.image.load("media/spaces.jpg")
        self.fon = pygame.transform.scale(self.photo, (self.width, self.height))
        self.clock = pygame.time.Clock()
        self.tick_rate = 30
        self.game_over = pygame.image.load("media/game_over.png")
        self.title = pygame.display.set_caption("Star Battle")
        self.font = pygame.font.Font(None, 40)
        self.live = pygame.image.load("media/live.png")
        self.music = pygame.mixer.music.load('media/fon_sound.mp3')
        self.icon = pygame.display.set_icon(pygame.image.load("media/package_2.png"))
        self.records = False
        self.hero_died = False
        self.show_record = False
        self.show_graph = False
        self.live_count = 3
        self.passed = 0
        # self.screen.blit(self.fon, (0, 0))


class Bullet(object):
    def __init__(self, x=1, y=1, radius=1, color=(255, 255, 255), used=False, vel=-8):
        self.x = x
        self.y = y
        self.used = used
        self.radius = radius
        self.color = color
        self.vel = vel

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class AlienBullet(Bullet):
    def __init__(self, x, y, radius, color, used, vel):
        super().__init__(x, y, radius, color=(180, 0, 0), used=used, vel=8)


class HeroBullet(Bullet):
    def __init__(self, x=1, y=1, radius=1, used=False, vel=-8):
        super().__init__(x, y, radius, color=(0, 255, 0), used=used, vel=vel)


class Hero(object):
    def __init__(self):
        self.x = 1316
        self.y = 718
        self.width = 50
        self.height = 50
        self.speed = 5
        self.left = False
        self.right = False
        self.walkRight = pygame.image.load("media/package_1.png")
        self.walkLeft = pygame.image.load("media/package_3.png")
        self.playerStand = pygame.image.load("media/package_2.png")
        self.killed = 0
        self.hero_bullets = []

    def draw_hero(self, screen):
        if self.left:
            screen.blit(self.walkLeft, (self.x - 25, self.y))
        elif self.right:
            screen.blit(self.walkRight, (self.x - 25, self.y))
        else:
            screen.blit(self.playerStand, (self.x - 25, self.y))
        for bullet in self.hero_bullets:
            bullet.draw(screen)

    # adding hero bullets to the list
    def shoot(self):
        used_bullets = filter(lambda x: x.used == False, self.hero_bullets)
        self.hero_bullets = list(used_bullets)

        if len(list(self.hero_bullets)) < 10:
            new_bullet = HeroBullet(round(self.x), round(self.y + self.height // 2), radius=5, used=False, vel=-8)
            self.hero_bullets.append(new_bullet)


class Alien(object):
    def __init__(self, x=0, y=0, status=True, reload=random.randint(0, 15)):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.alien_turn = 2
        self.alien_speed = 5
        self.status = status
        self.alien_img = pygame.image.load("media/enemies.png")
        self.alien_bullets = []
        self.reload = reload

    def alien_draw(self, screen):
        screen.blit(self.alien_img, (self.x, self.y))

    # adding alien bullets to the list
    def shoot(self):
        used_bullets = filter(lambda x: x.used == False, self.alien_bullets)
        self.alien_bullets = list(used_bullets)

        if len(list(self.alien_bullets)) < 10:
            new_bullet = AlienBullet(round(self.x + self.width // 2), round(self.y + self.height // 2), 5,
                                     (225, 0, 0), False, 8)
            self.alien_bullets.append(new_bullet)


class Squad_aliens(object):
    def __init__(self):
        self.aliens_list = []

    # drawing aliens
    def draw_alien(self, screen):
        for alien in self.aliens_list:
            alien.alien_draw(screen)
            for bullet in alien.alien_bullets:
                bullet.draw(screen)

    # adding aliens to the list
    def append_alien(self):
        if len(self.aliens_list) < 10:
            i = random.randint(25, 1366 - 25)
            self.aliens_list.append(Alien(x=i, y=10, status=False))
