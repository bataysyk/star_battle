import datetime
from statistics import *
import sys
from models import *
import csv


class GameProcess(object):
    def __init__(self):
        self.settings = Settings()
        self.squad_aliens = Squad_aliens()
        self.hero = Hero()
        self.statistic = Statistic()
        self.menu_open = False
        self.count = 0
        self.count_for_draw_alien_bullet = 0

    def information(self):
        text_1 = self.settings.font.render(str(self.hero.killed), 1, (180, 0, 0))
        text_2 = self.settings.font.render(str(self.settings.passed), 1, (180, 0, 0))
        self.settings.screen.blit(text_1, (self.settings.width // 4, 10))
        self.settings.screen.blit(text_2, (self.settings.width // 2, 10))
        distance = 20
        for i in range(self.settings.live_count):
            x = 1266 + distance
            self.settings.screen.blit(self.settings.live, (x, 748))
            distance += 20

    # def append_alien(self):
    #     if len(self.squad_aliens.aliens_list) < 10:
    #         i = random.randint(25, self.settings.width - 25)
    #         self.squad_aliens.aliens_list.append(Alien(x=i, y=10, status=False))

    def alien_move(self):
        for alien in self.squad_aliens.aliens_list:
            if alien.x + alien.width // 2 + 1 > self.hero.x:
                alien.y += alien.alien_speed
                alien.x -= alien.alien_turn
            elif alien.x + alien.width // 2 + 1 < self.hero.x:
                alien.y += alien.alien_speed
                alien.x += alien.alien_turn
            if alien.y >= self.settings.height:
                self.squad_aliens.aliens_list.pop(self.squad_aliens.aliens_list.index(alien))
                self.settings.passed += 1
            if alien.status:
                self.squad_aliens.aliens_list.pop(self.squad_aliens.aliens_list.index(alien))

    def drawWindow(self):
        self.settings.screen.blit(self.settings.fon, (0, 0))
        self.information()
        self.hero.draw_hero(self.settings.screen)
        self.squad_aliens.draw_alien(self.settings.screen)

    def game_process(self):
        self.settings.clock.tick(self.settings.tick_rate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.settings.run = False

        # fill aliens till 10
        self.squad_aliens.append_alien()

        # alien shoot
        for alian in self.squad_aliens.aliens_list:
            if 0 == random.randint(0, 10):
                alian.shoot()
        self.alien_move()

        # if aliens passed live_count -= 1
        if self.settings.passed == 10:
            self.settings.live_count -= 1
            self.settings.passed = 0

        # bullet move from hero
        for bullet in self.hero.hero_bullets:
            if self.settings.height > bullet.y > 0:
                bullet.y += bullet.vel
            else:
                bullet.used = True

        # bullet move from alien
        for alien in self.squad_aliens.aliens_list:
            for bullet in alien.alien_bullets:
                if self.settings.height > bullet.y > 0:
                    bullet.y += bullet.vel
                else:
                    bullet.used = True

        # hero move
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.settings.run = False
            pygame.quit()
        if keys[pygame.K_SPACE]:
            if 0 == random.randint(0, 3):
                self.hero.shoot()

        if keys[pygame.K_LEFT] and self.hero.x > self.hero.width // 2:
            self.hero.x -= self.hero.speed
            self.hero.left = True
            self.hero.right = False
        elif keys[pygame.K_RIGHT] and self.hero.x < self.settings.width - self.hero.width // 2:
            self.hero.x += self.hero.speed
            self.hero.left = False
            self.hero.right = True
        else:
            self.hero.left = False
            self.hero.right = False

    def check_collision(self):

        # checking the collision between the bullet and the alien
        for alien in self.squad_aliens.aliens_list:
            for bullet in self.hero.hero_bullets:
                x = alien.x - bullet.x
                y = alien.y - bullet.y
                z = (x ** 2 + y ** 2) ** (1 / 2)
                if 30 >= z >= -30:
                    self.hero.killed += 1
                    alien.status = True

        # checking the colision between the bullet, alien and the hero
        for alien in self.squad_aliens.aliens_list:
            for bullet in alien.alien_bullets:
                a = bullet.x - self.hero.x
                b = bullet.y - self.hero.y
                f = (a ** 2 + b ** 2) ** (1 / 2)
                x = alien.x - self.hero.x
                y = alien.y - self.hero.y
                z = (x ** 2 + y ** 2) ** (1 / 2)
                if 20 >= z >= -20 or 20 >= f >= -20:
                    self.settings.hero_died = True

    # output records to the screen
    def records_display(self):
        with open("records.csv", 'rt') as f:
            data = csv.reader(f)
            count = 0
            text_navigation_menu = self.settings.font.render(f"Menu press '3'", 1, (180, 0, 0))
            self.settings.screen.blit(text_navigation_menu, (10, 10))
            text_navigation_show_graph = self.settings.font.render(f"Show graph press '1'", 1, (180, 0, 0))
            self.settings.screen.blit(text_navigation_show_graph, (1000, 10))
            for row in data:
                text = self.settings.font.render(f"{str(row)}", 1, (180, 0, 0))
                self.settings.screen.blit(text, (200, 30 + count))
                count += 30
                if count == 150:
                    self.exit()

    # cleaning the display
    def clean_display(self):
        pygame.draw.rect(self.settings.screen, (0, 0, 0),
                         (0, 0, self.settings.width, self.settings.height))

    # menu_open view
    def menu_display(self):
        self.clean_display()
        # self.settings.screen.blit(self.settings.game_over, (75, 75))
        text_game_over = self.settings.font.render(f"GAME OVER", 1, (180, 0, 0))
        text_1 = self.settings.font.render(f"Your result: ({str(self.hero.killed)})", 1,
                                           (180, 0, 0))
        text_2 = self.settings.font.render("Click SPACES to continue", 1,
                                           (180, 0, 0))
        text_3 = self.settings.font.render("Click '1' records ", 1,
                                           (180, 0, 0))
        self.settings.screen.blit(text_game_over, (400, 100))
        self.settings.screen.blit(text_1, (400, 130))
        self.settings.screen.blit(text_2, (400, 160))
        self.settings.screen.blit(text_3, (400, 190))

    # menu_open functionality
    def menu(self):
        keys = pygame.key.get_pressed()
        if self.count == 0:
            with open("records.csv", "a") as f:
                f.write(f"{datetime.datetime.now()}, 'dima', {self.hero.killed}\n")
            self.count = 1

        self.menu_display()
        if keys[pygame.K_SPACE]:
            self.squad_aliens.aliens_list = []
            self.hero.hero_bullets = []
            self.settings.hero_died = False
            self.hero.killed = 0
            self.settings.live_count = 3
            self.count = 0
        if keys[pygame.K_q]:
            self.exit()
        if keys[pygame.K_ESCAPE]:
            self.menu_open = True
        if keys[pygame.K_1]:
            self.settings.show_graph = True
        elif keys[pygame.K_2]:
            self.settings.show_record = True
        if self.settings.show_record:
            self.clean_display()
            self.records_display()
            if keys[pygame.K_ESCAPE]:
                self.menu_open = True
                self.settings.show_record = False
        if self.settings.show_graph:
            self.statistic.create_graph()
            graph = pygame.image.load("media/Figyre_1.png")
            transform_graph = pygame.transform.scale(graph, (self.settings.width, self.settings.height))
            self.settings.screen.blit(transform_graph, (0, 0))
            if keys[pygame.K_ESCAPE]:
                self.menu_open = True
                self.settings.show_graph = False

    # exit from game
    def exit(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            sys.exit()  # pygame.quit()

    # game cycle
    def start(self):
        pygame.init()
        pygame.mixer.music.play(-1, 0.0)
        while self.settings.run:
            if not self.settings.hero_died:
                self.drawWindow()
                self.check_collision()
                self.game_process()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self.menu_open = True
                    self.menu()
            elif self.settings.hero_died:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.settings.run = False
                    elif self.settings.live_count != 0:
                        self.settings.live_count -= 1
                        self.settings.hero_died = False
                        self.squad_aliens.aliens_list = []
                        self.hero.hero_bullets = []
                    elif self.settings.live_count == 0:
                        self.menu_open = True
                        self.menu()
            pygame.display.update()
