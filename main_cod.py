import os
import sys
import pygame

level_temp = ['----------------',
              '-    -  -      -',
              '-    -  -      -',
              '-              -',
              '-              -',
              '-        -     -',
              '-    --        -',
              '-              -',
              '----------------']
WIDTH = 1280
HEIGHT = 720


def start_screen():  # Класс стартер
    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((1, 1))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    pygame.init()
    pygame.display.set_caption('Проект pygame')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.blit(load_image('background1.png'), (300, 0))
    screen.blit(load_image('Press F to play .png'), (400, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start()
                pygame.quit()
            pygame.display.flip()


def start():  # Класс основной работы игры
    pygame.init()
    pygame.display.set_caption('Проект pygame')
    screen = pygame.display.set_mode((1280, 720))

    test_sprites = pygame.sprite.Group()
    shot_sp_1 = pygame.sprite.Group()
    shot_sp_2 = pygame.sprite.Group()
    shot_sp = pygame.sprite.Group()
    sp_wall = pygame.sprite.Group()

    level = level_temp

    def draw_map():
        y = -1
        for row in level:
            y += 1
            x = 0
            for col in row:
                if col == "-":
                    a = wall(x, y)
                    sp_wall.add(a)
                x += 1

    class wall(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = load_image('wall_80_80.png')
            self.rect = self.image.get_rect()
            self.rect.x = x * 80
            self.rect.y = y * 80
            self.mask = pygame.mask.from_surface(self.image)

    class projectile(pygame.sprite.Sprite):
        def __init__(self, x, y, dir, tank):
            pygame.sprite.Sprite.__init__(self)
            self.count = 0
            self.tank = tank
            self.image = load_image('снаряд-финиш1.png')
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.direction = 1  # Направление танка (1 = вверх)
            self.rect.x = x
            self.rect.y = y
            self.count = 0
            while self.direction % 4 != dir:
                self.image = pygame.transform.rotate(self.image, 90)
                self.direction += 1
            self.direction = self.direction % 4
            if self.direction == 1:  # up
                self.rect.x = x
                self.rect.y -= 80
            elif self.direction == 2:
                self.rect.x -= 80
                self.rect.y = y
            elif self.direction == 3:
                self.rect.x = x
                self.rect.y += 80
            else:
                self.rect.x += 80
                self.rect.y = y

        def update(self):
            if self.count % 2 == 0:
                if self.direction == 1:  # up
                    self.rect.y -= 30
                elif self.direction == 2:
                    self.rect.x -= 30
                elif self.direction == 3:
                    self.rect.y += 30
                else:
                    self.rect.x += 30
            self.count += 1

            if pygame.sprite.spritecollideany(self, sp_wall):
                if self.tank == 1:
                    shot_sp_1.remove(self)
                    shot_sp.remove(self)
                    print(self.rect)

                else:
                    print(self.rect)
                    shot_sp_2.remove(self)
                    shot_sp.remove(self)

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((1, 1))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    class tank1(pygame.sprite.Sprite):
        def __init__(self, x, y, tank):
            super().__init__(test_sprites)
            self.image = load_image(f'tank1_1.png', -1)
            self.rect = self.image.get_rect()
            self.tank = tank
            self.rect.x = 80
            self.rect.y = 80
            self.dead_b = True
            self.direction = 1
            self.mask_t = pygame.mask.from_surface(self.image)

        def riding(self, arg):
            if arg == 1073741906:  # UP
                while self.direction % 4 != 1:
                    self.rotate()
                    self.direction += 1
                self.direction = 1
                self.rect.y -= 30
                if pygame.sprite.spritecollideany(self, sp_wall):
                    self.rect.y += 30
            if arg == 1073741905:  # DOWN
                while self.direction % 4 != 3:
                    self.rotate()
                    self.direction += 1
                self.direction = 3
                self.rect.y += 30
                if pygame.sprite.spritecollideany(self, sp_wall):
                    self.rect.y -= 30
            if arg == 1073741904:  # LEFT
                while self.direction % 4 != 2:
                    self.rotate()
                    self.direction += 1
                self.direction = 2
                self.rect.x -= 30
                if pygame.sprite.spritecollideany(self, sp_wall):
                    self.rect.x += 30
            if arg == 1073741903:  # RIGHT
                while self.direction % 4 != 0:
                    self.rotate()
                    self.direction += 1
                self.direction = 0
                self.rect.x += 30
                if pygame.sprite.spritecollideany(self, sp_wall):
                    self.rect.x -= 30
            if arg == 1073741922:
                self.shot()

        def rotate(self):
            self.image = pygame.transform.rotate(self.image, 90)

        def dead(self):
            if self.dead_b:
                test_sprites.remove(min_1)
                self.dead_b = False

        def shot(self):
            if self.dead_b:
                shot = projectile(self.rect.x, self.rect.y, self.direction, self.tank)
                shot_sp_1.add(shot)
                shot_sp.add(shot)

        def update(self):
            if pygame.sprite.spritecollideany(self, shot_sp_2):
                self.dead()
                test_sprites.remove(self)

    class tank2(pygame.sprite.Sprite):
        def __init__(self, x, y, tank):
            super().__init__(test_sprites)
            b = str(tank)
            self.image = load_image(f'tank2.png', -1)
            self.rect = self.image.get_rect()
            self.tank = tank
            self.rect.x = 800
            self.rect.y = 80
            self.dead_b = True
            self.direction = 1
            self.mask_t = pygame.mask.from_surface(self.image)

        def riding(self, arg):
            if arg == 119:  # UP
                while self.direction % 4 != 1:
                    self.rotate()
                    self.direction += 1
                self.direction = 1
                self.rect.y -= 30
                if pygame.sprite.spritecollideany(self, sp_wall):
                    self.rect.y += 30
            if arg == 115:  # DOWN
                while self.direction % 4 != 3:
                    self.rotate()
                    self.direction += 1
                self.direction = 3
                self.rect.y += 30
                if pygame.sprite.spritecollideany(self, sp_wall):
                    self.rect.y -= 30
            if arg == 97:  # LEFT
                while self.direction % 4 != 2:
                    self.rotate()
                    self.direction += 1
                self.direction = 2
                self.rect.x -= 30
                if pygame.sprite.spritecollideany(self, sp_wall):
                    self.rect.x += 30
            if arg == 100:  # RIGHT
                while self.direction % 4 != 0:
                    self.rotate()
                    self.direction += 1
                self.direction = 0
                self.rect.x += 30
                if pygame.sprite.spritecollideany(self, sp_wall):
                    self.rect.x -= 30
            if arg == 114:
                self.shot()

        def rotate(self):
            self.image = pygame.transform.rotate(self.image, 90)

        def dead(self):
            if self.dead_b:
                test_sprites.remove(min_2)
                self.dead_b = False

        def shot(self):
            if self.dead_b:
                shot = projectile(self.rect.x, self.rect.y, self.direction, self.tank)
                shot_sp_2.add(shot)
                shot_sp.add(shot)

        def update(self):
            if pygame.sprite.spritecollideany(self, shot_sp_1):
                self.dead()
                test_sprites.remove(self)

    min_1 = tank1(30, 30, 1)
    min_2 = tank2(30, 30, 2)

    running = True
    draw_map()
    while running:
        screen.fill((0, 0, 0))
        sp_wall.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                min_1.riding(event.key)
                min_2.riding(event.key)
                if min_1.dead_b == False or min_2.dead_b == False:
                    restart()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            shot_sp.update()
            shot_sp.draw(screen)
            test_sprites.update()
            test_sprites.draw(screen)
            pygame.display.flip()
    pygame.quit()


def restart():  # Класс рестарта
    start()


start_screen()
