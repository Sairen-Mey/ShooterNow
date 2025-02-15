import pygame
import sys
import random
pygame.init()
pygame.mixer.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 150, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
qqq = (76,0,153)
qq = (102,0,204)
width = 1920
height = 1080
Lose = False
font = pygame.font.Font(None, 48)
uwu = pygame.display.set_mode((width, height))
pygame.display.set_caption("UwU")
clock = pygame.time.Clock()
FPS = 60
sss = pygame.image.load("backgrounf.jpeg")
sss = pygame.transform.scale(sss, (width, height))
bob = pygame.image.load("backgroun_of_battles.jpeg")
bob = pygame.transform.scale(bob, (width, height))
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
class Player(pygame.sprite.Sprite):
    def __init__(self, image, imageleft, imageright, x, y, speed):
        super().__init__()
        self.image = image
        self.imagetop = pygame.transform.scale(image, (150, 150))
        self.imageleft = pygame.transform.scale(imageleft, (150, 150))
        self.imageright = pygame.transform.scale(imageright, (150, 150))
        self.base_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.base_image = self.imageleft
        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.base_image = self.imageright
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            self.base_image = self.imagetop
        self.image = self.base_image
        if self.rect.x > width-100:
            self.rect.x = 10
        if self.rect.x < 0:
            self.rect.x = width-150
player = Player(pygame.image.load("player.png"), pygame.image.load("playerleft.png"), pygame.image.load("playerright.png"), width/2, 820, 5)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image =   pygame.transform.scale(image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:  
            self.kill()
    def draw(self):
        uwu.blit(self.image, self.rect)
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed, x):
        super().__init__()
        self.image = pygame.transform.scale(image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0
        self.speed = speed
    def update(self):
        global Lose
        self.rect.y += self.speed
        self.rect.y = int(self.rect.y)
        if self.rect.y > height - 100:
            Lose = True
startgame = pygame.mixer.Sound("startplay.mp3")
pygame.mixer.music.load("backgroundsound.mp3")
pygame.mixer.music.play(-1)
sound_effect = pygame.mixer.Sound("boom.mp3")
music_volume = 50
sound_volume = 50
def update_volumes():
    pygame.mixer.music.set_volume(music_volume / 100)
    sound_effect.set_volume(sound_volume / 100)
update_volumes()
class Slider:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.width = 300
        self.height = 10
        self.knob_radius = 10
        self.value = 50
        self.label = label
        self.dragging = False
    def draw(self, screen):
        pygame.draw.line(screen, (200, 200, 200), (self.x, self.y), (self.x + self.width, self.y), self.height)
        knob_x = self.x + int((self.value / 100) * self.width)
        pygame.draw.circle(screen, (255, 0, 0), (knob_x, self.y), self.knob_radius)
        font = pygame.font.Font(None, 24)
        text = font.render(f"{self.label}: {self.value}", True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 25))
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            knob_x = self.x + int((self.value / 100) * self.width)
            if abs(mouse_x - knob_x) < self.knob_radius * 2 and abs(mouse_y - self.y) < self.knob_radius * 2:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, _ = event.pos
            new_value = max(0, min(100, int(((mouse_x - self.x) / self.width) * 100)))
            self.value = new_value
music_slider = Slider(width/2-140, 450, "Музика")
sound_slider = Slider(width/2-140, 550, "Звуки")
enemy_image = pygame.image.load("enemy.png")
def generate_enemy_positions(num_enemies, width, min_distance, enemy_width):
    enemy_positions = []
    for _ in range(num_enemies):
        while True:
            x = random.randint(100, width - enemy_width)
            if all(abs(x - ex) > min_distance for ex in enemy_positions):
                enemy_positions.append(x)
                break
    return enemy_positions
def draw_text(text, color, rect, center=True):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect()
    if center:
        text_rect.center = rect.center
    else:
        text_rect.topleft = rect.topleft
    uwu.blit(rendered_text, text_rect)
exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
def main_menu():
    global width, height
    while True:
        play_button = pygame.Rect(width // 2 - 100, 500, 250, 50)
        exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
        author_button = pygame.Rect(width // 2 - 100, 600, 250, 50)
        settings_menu_button = pygame.Rect(width // 2 - 100, 700, 250, 50)
        pygame.draw.rect(uwu, qqq if play_button.collidepoint(pygame.mouse.get_pos()) else qq, play_button)
        pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
        pygame.draw.rect(uwu, qqq if author_button.collidepoint(pygame.mouse.get_pos()) else qq, author_button)
        pygame.draw.rect(uwu, qqq if settings_menu_button.collidepoint(pygame.mouse.get_pos()) else qq, settings_menu_button)
        draw_text("Почати гру", WHITE, play_button)
        draw_text("Вихід", WHITE, exit_button)
        draw_text("автор гри", WHITE, author_button)
        draw_text("Налаштування", WHITE, settings_menu_button)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if author_button.collidepoint(event.pos):
                    AuthorOfGame()
                if play_button.collidepoint(event.pos):
                    ChooseTheLevel()
                if settings_menu_button.collidepoint(event.pos):
                    settings_menu()
        uwu.blit(sss, (0, 0))
def settings_menu():
    global music_volume, sound_volume
    while True:
        uwu.blit(sss, (0, 0))
        back_button = pygame.Rect(width // 2 - 100, 900, 250, 50)
        pygame.draw.rect(uwu, qqq if back_button.collidepoint(pygame.mouse.get_pos()) else qq, back_button)
        draw_text("Назад", WHITE, back_button)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    main_menu()    
            music_slider.handle_event(event)
            sound_slider.handle_event(event)
        music_volume = music_slider.value
        sound_volume = sound_slider.value
        update_volumes()
        music_slider.draw(uwu)
        sound_slider.draw(uwu)
        pygame.display.flip()
def AuthorOfGame():
    while True:
        author = pygame.Rect(width // 2 - 100, 550, 250, 50)
        draw_text("Kyrylov Bohdan", WHITE, author)
        back_button = pygame.Rect(width // 2 - 100, 700, 250, 50)
        pygame.draw.rect(uwu, qqq if back_button.collidepoint(pygame.mouse.get_pos()) else qq, back_button)
        draw_text("Назад", WHITE, back_button)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):  
                    main_menu()
        uwu.blit(sss, (0, 0))
def level1start():
    global l1, Lose
    Lose = False
    enemies.empty()
    exit_button = pygame.Rect(width / 2 + 720, 100, 50, 50)
    enemy_width = enemy_image.get_width()
    enemy_positions = generate_enemy_positions(5, width, 100, enemy_width)
    for x in enemy_positions:
        enemies.add(Enemy(enemy_image, 0.5, x))
    while True:
        uwu.blit(bob, (0, 0))
        enemies.draw(uwu)
        enemies.update()
        pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
        draw_text("X", WHITE, exit_button)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    ChooseTheLevel()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sound_effect.play()
                    bullet = Bullet(pygame.image.load("bullet.png"), player.rect.x + 50, player.rect.y, 5)
                    bullets.add(bullet)
        collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
        player.update() 
        uwu.blit(player.image, player.rect)
        if len(enemies) == 0:
            l1 = True
            exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
            pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
            draw_text("Назад", WHITE, exit_button)
            textbutton = pygame.Rect(width // 2 - 100, 500, 250, 50)
            pygame.draw.rect(uwu, qqq, textbutton)
            draw_text("Ви виграли", WHITE, textbutton)
        if Lose:
            exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
            pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
            draw_text("Назад", WHITE, exit_button)
            textbutton = pygame.Rect(width // 2 - 100, 500, 250, 50)
            pygame.draw.rect(uwu, qqq, textbutton)
            draw_text("Ви програли", WHITE, textbutton)
        bullets.update()
        bullets.draw(uwu)
        pygame.display.flip()
def level2start():
    global l2, Lose
    Lose = False
    exit_button = pygame.Rect(width / 2 + 720, 100, 50, 50)
    enemies.empty()
    enemy_width = enemy_image.get_width()
    enemy_positions = generate_enemy_positions(6, width, 100, enemy_width)
    for x in enemy_positions:
        enemies.add(Enemy(enemy_image, 0.5, x))
    while True:
        uwu.blit(bob, (0, 0))
        enemies.draw(uwu)
        enemies.update()
        pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
        for event in pygame.event.get(): 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                   ChooseTheLevel()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sound_effect.play()
                    bullet = Bullet(pygame.image.load("bullet.png"), player.rect.x + 50, player.rect.y, 5)
                    bullets.add(bullet)
        collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
        player.update() 
        uwu.blit(player.image, player.rect)
        if len(enemies) == 0:
            l2 = True
            exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
            pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
            draw_text("Назад", WHITE, exit_button)
            textbutton = pygame.Rect(width // 2 - 100, 500, 250, 50)
            pygame.draw.rect(uwu, qqq, textbutton)
            draw_text("Ви виграли", WHITE, textbutton)
        uwu.blit(player.image, player.rect)
        if Lose:
            exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
            pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
            draw_text("Назад", WHITE, exit_button)
            textbutton = pygame.Rect(width // 2 - 100, 500, 250, 50)
            pygame.draw.rect(uwu, qqq, textbutton)
            draw_text("Ви програли", WHITE, textbutton)
        bullets.update()
        bullets.draw(uwu)
        pygame.display.flip()
def level3start():
    global l3, Lose
    Lose = False
    exit_button = pygame.Rect(width / 2 + 720, 100, 50, 50)
    enemies.empty()
    enemy_width = enemy_image.get_width()
    enemy_positions = generate_enemy_positions(7, width, 100, enemy_width)
    for x in enemy_positions:
        enemies.add(Enemy(enemy_image, 0.5, x))
    while True:
        uwu.blit(bob, (0, 0))
        enemies.draw(uwu)
        enemies.update()
        pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    ChooseTheLevel()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sound_effect.play()
                    bullet = Bullet(pygame.image.load("bullet.png"), player.rect.x + 50, player.rect.y, 5)
                    bullets.add(bullet)
        collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
        uwu.blit(player.image, player.rect)
        if len(enemies) == 0:
            l3 = True
            exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
            pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
            draw_text("Назад", WHITE, exit_button)
            textbutton = pygame.Rect(width // 2 - 100, 500, 250, 50)
            pygame.draw.rect(uwu, qqq, textbutton)
            draw_text("Ви виграли", WHITE, textbutton)
        player.update() 
        if Lose:
            exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
            pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
            draw_text("Назад", WHITE, exit_button)
            textbutton = pygame.Rect(width // 2 - 100, 500, 250, 50)
            pygame.draw.rect(uwu, qqq, textbutton)
            draw_text("Ви програли", WHITE, textbutton)
        bullets.update()
        bullets.draw(uwu)
        pygame.display.flip()
def level4start():
    global l4, Lose
    Lose = False
    exit_button = pygame.Rect(width / 2 + 720, 100, 50, 50)
    enemies.empty()
    enemy_width = enemy_image.get_width()
    enemy_positions = generate_enemy_positions(10, width, 100, enemy_width)
    for x in enemy_positions:
        enemies.add(Enemy(enemy_image, 0.5, x))
    while True:
        uwu.blit(bob, (0, 0))
        enemies.draw(uwu)
        enemies.update()
        pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
        for event in pygame.event.get(): 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    ChooseTheLevel()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sound_effect.play()
                    bullet = Bullet(pygame.image.load("bullet.png"), player.rect.x + 50, player.rect.y, 5)
                    bullets.add(bullet)
        collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
        uwu.blit(player.image, player.rect)
        if len(enemies) == 0:
            l4 = True
            exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
            pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
            draw_text("Назад", WHITE, exit_button)
            textbutton = pygame.Rect(width // 2 - 100, 500, 250, 50)
            pygame.draw.rect(uwu, qqq, textbutton)
            draw_text("Ви виграли", WHITE, textbutton)
        if Lose:
            exit_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
            pygame.draw.rect(uwu, qqq if exit_button.collidepoint(pygame.mouse.get_pos()) else qq, exit_button)
            draw_text("Назад", WHITE, exit_button)
            textbutton = pygame.Rect(width // 2 - 100, 500, 250, 50)
            pygame.draw.rect(uwu, qqq, textbutton)
            draw_text("Ви програли", WHITE, textbutton)
        player.update()  
        bullets.update()
        bullets.draw(uwu)
        pygame.display.flip()
l1, l2, l3, l4 = False, False, False, False
def ChooseTheLevel():
    while True:
        global l1, l2, l3, l4
        level1 = pygame.Rect(width // 2 - 100, 200, 250, 50)
        level2 = pygame.Rect(width // 2 - 100, 300, 250, 50)
        level3 = pygame.Rect(width // 2 - 100, 400, 250, 50)
        level4 = pygame.Rect(width // 2 - 100, 500, 250, 50)
        back_button = pygame.Rect(width // 2 - 100, 800, 250, 50)
        reset_button = pygame.Rect(width // 2 + 700, 900, 50, 50)
        check_level1 = pygame.Rect(width // 2 + 165, 200, 50, 50)
        check_level2 = pygame.Rect(width // 2 + 165, 300, 50, 50)
        check_level3 = pygame.Rect(width // 2 + 165, 400, 50, 50)
        check_level4 = pygame.Rect(width // 2 + 165, 500, 50, 50)
        pygame.draw.rect(uwu, qqq if level1.collidepoint(pygame.mouse.get_pos()) else qq, level1)
        pygame.draw.rect(uwu, qqq if level2.collidepoint(pygame.mouse.get_pos()) else qq, level2)
        pygame.draw.rect(uwu, qqq if level3.collidepoint(pygame.mouse.get_pos()) else qq, level3)
        pygame.draw.rect(uwu, qqq if level4.collidepoint(pygame.mouse.get_pos()) else qq, level4)
        pygame.draw.rect(uwu, qqq if back_button.collidepoint(pygame.mouse.get_pos()) else qq, back_button)
        pygame.draw.rect(uwu, GREEN if l1 == True else RED, check_level1)
        pygame.draw.rect(uwu, GREEN if l2 == True else RED, check_level2)
        pygame.draw.rect(uwu, GREEN if l3 == True else RED, check_level3)
        pygame.draw.rect(uwu, GREEN if l4 == True else RED, check_level4)
        pygame.draw.rect(uwu, RED if reset_button.collidepoint(pygame.mouse.get_pos()) else qqq, reset_button)
        draw_text("1 рівень", WHITE, level1)
        draw_text("2 рівень", WHITE, level2)
        draw_text("3 рівень", WHITE, level3)
        draw_text("4 рівень", WHITE, level4)
        draw_text("Назад", WHITE, back_button)
        draw_text("С", WHITE, reset_button)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    main_menu()
                if reset_button.collidepoint(event.pos):
                    l1, l2, l3, l4 = False, False, False, False
                if level1.collidepoint(event.pos):
                    startgame.play()
                    level1start()
                if level2.collidepoint(event.pos):
                    startgame.play()
                    level2start()
                if level3.collidepoint(event.pos):
                    startgame.play()
                    level3start()
                if level4.collidepoint(event.pos):
                    startgame.play()
                    level4start()
        uwu.blit(sss, (0, 0))
main_menu()
