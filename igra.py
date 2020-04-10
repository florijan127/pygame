#importam pygame
import pygame

import random

# ovo je za lakši pristup tipkama za pomicanje
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# radimo klasu player pomoću pygameovog spritea
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        
    # funkcija update pomiče igrača s obzirom na pritisnute tipke
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # ovo služi da igrač nemože izaći iz ekrana
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# stvaramo neprijatelje
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # funkcija koja pomiče neprijatelja određenom brzinom
    # neprijatelj se briše iz svih grupa kada izaže s ekrana
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# initializacija 
pygame.init()

# stvaramo prozor
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# stvaramo novi event koji će se ponavljati svakij 250 milisekundi
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# stvaramo playera
player = Player()

# stvaramo grupe za neprijatelje i za sve objekte na ekranu(spriteove)
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# pokrećemo loop
running = True

while running:
    # za svaki događaj
    for event in pygame.event.get():
         # ako je pritisnuta tipka
        if event.type == KEYDOWN:
            # ako je pritisnut escape, loop se zatvara
            if event.key == K_ESCAPE:
                running = False

        # ako je pritisnut gump za zatvaranje prozora loop se zatvara
        elif event.type == QUIT:
            running = False

        # ako je event za dodavanje neprijatelja, stvaramo ga i dodajemo ga u grupu
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
    # dobivamo rjecnik svih pritisnutih tipki
    pressed_keys = pygame.key.get_pressed()

    # funkcijom update pomičemo igrača
    player.update(pressed_keys)

    # pa neprijatelja
    enemies.update()


    # bojamo prozor u bijelo
    screen.fill((0, 0, 0))

     # funkcijom blit crtamo objekte(spriteove) na prozoru
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # pygame ima funkciju za provjeravanje ako je došlo do sudara igrača i neprijatelja
    if pygame.sprite.spritecollideany(player, enemies):
    # ako jest, loop se gasi
        player.kill()
        running = False
        
    # flip funkcija prikazuje sve ovo na prozoru
    pygame.display.flip()
