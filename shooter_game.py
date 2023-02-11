from pygame import *
from random import randint

score = 0
lost = 0
live = 5
font.init()
font1 = font.SysFont("Arial", 26)

win_x = 1000
win_y = 600
window = display.set_mode((win_x, win_y))
display.set_caption("Mission in space")
image1 = transform.scale(image.load("galaxy.jpg"), (win_x, win_y))


mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fir = mixer.Sound("fire.ogg")

#основной класс
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
#класс для передвижения игрока
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x > 5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x < win_x -80:
            self.rect.x += self.speed
        # if (keys[K_UP] or keys[K_w]) and self.rect.y > 5:
            # self.rect.y -= self.speed
        # if (keys[K_DOWN] or keys[K_s]) and self.rect.y < win_y -80:
            # self.rect.y += self.speed

    def fire(self):
            bullet = Bullet("bullet.png", self.rect.centerx ,  self.rect.top, -50)
            bullets.add(bullet)
            fir.play()
#для появления нло
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_y:
            self.rect.x = randint(80, win_x - 80)
            self.rect.y = 0
            lost += 1

#для появления астеройдов
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_y:
            self.rect.x = randint(80, win_x - 80)
            self.rect.y = 0
            
#для пуль
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()
asteroids = sprite.Group()
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_x - 80), -40, randint(1, 2))
    monsters.add(monster)

for i in range(1, 2):
    asteroid = Asteroid("asteroid.png", randint(80, win_x - 80), -40, randint(1, 6))
    asteroids.add(asteroid)

player = Player("rocket.png", win_x/2, win_y - 80, 10)

font = font.SysFont('Arial', 70)
w1n = font.render("You won!", True, (255,255,255))
lose = font.render("You lose!", True, (255,255,255))

clock = time.Clock()
FPS = 100
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()


    if not finish:
        window.blit(image1, (0, 0))
        text = font1.render("Счёт: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 15))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_live = font1.render(str(live), 1, (0,255,0))
        window.blit(text_live, (950, 15))
        
 
        for i in sprite.groupcollide(monsters, bullets, True, True):
            score += 1
            monster = Enemy("ufo.png", randint(80, win_x - 80), -40, randint(1, 2))
            monsters.add(monster)

        sprite.groupcollide(asteroids, bullets, False, True)

        '''if sprite.spritecollide(player, asteroids, False) or sprite.spritecollide(player, monsters, False):
            sprite.spritecollide(player, asteroids, True)
            sprite.spritecollide(player, monsters, True)
            live -= 1'''
        for i in sprite.spritecollide(player, monsters, True):
            monster = Enemy("ufo.png", randint(80, win_x - 80), -40, randint(1, 2))
            monsters.add(monster)
            live -= 1
        for i in sprite.spritecollide(player, asteroids, True):
            asteroid = Asteroid("asteroid.png", randint(80, win_x - 80), -40, randint(1, 6))
            asteroids.add(asteroid)
            live -= 1

        if score >= 20:
            finish = True
            window.blit(w1n, (375,275))
        
        if lost >= 5 or live <= 0:
            finish = True
            window.blit(lose, (375,275))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        asteroids.draw(window)
        asteroids.update()

        bullets.draw(window)
        bullets.update()


    display.update()
    clock.tick(FPS)
