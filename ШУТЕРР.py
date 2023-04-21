import pygame
import random
pygame.init()

window = pygame.display.set_mode((700, 500))
bg = pygame.transform.scale(pygame.image.load("Scorched_Stone-Map.webp"), (800, 600))
clock = pygame.time.Clock()


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def lol(self):
        pyla = Pyla("pixilart-drawing.png", self.rect.centerx, self.rect.top, 50, 50, 15)
        pyls.add(pyla)

class Rusar(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 399:
            self.rect.y = 0
            self.rect.x = random.randint(20, 600)

class Pyla(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player("Piper.webp", 300, 360, 70, 140, 10) 
rusars = pygame.sprite.Group()
pyls = pygame.sprite.Group()

score = 0

for i in range(4):
    rusar = Rusar("Mexo.webp", random.randint(20, 600), random.randint(-50, 0), 100, 120, random.randint(1, 2))
    rusars.add(rusar)

font = pygame.font.Font(None, 80)
text = font.render("Ты лутше всех!!!", True, (0, 0, 0))

game = True
while game:
    window.blit(bg, (-50, -50))
    player.reset()
    player.update()
    rusars.draw(window)
    rusars.update()
    pyls.draw(window)
    pyls.update()

    if score >= 20:
        window.blit(text, (100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.lol()

    collides = pygame.sprite.groupcollide(rusars, pyls, True, True)
    for i in collides:
        score += 1
        rusar = Rusar("Mexo.webp", random.randint(20, 600), random.randint(-50, 0), 100, 120, random.randint(3, 5))
        rusars.add(rusar)

    pygame.display.update()
    clock.tick(50)