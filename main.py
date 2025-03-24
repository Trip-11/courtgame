import pygame
import random

# Game constants
WIDTH = 1300
HEIGHT = 1024
FPS = 30

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (238, 130, 238)
ORANGE = (255, 165, 0)

font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 50 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)



def newmob():
    mob = Mob()
    mobs.add(mob)
    all_sprites.add(mob)

class Gavel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # size
        self.width = 205
        self.height = 215
        # image
        self.image = pygame.image.load("image-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # rectangle
        self.rect = self.image.get_rect()
        # Spawn at a random x along the top
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = 0  # fixed at top

    def update(self):
        pass

class Beam(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # size
        self.width = 200
        self.height = 555
        # image
        self.image = pygame.image.load("oie_transparent (1) (1).png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # rectangle
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y  # starts at the bottom of the gavel
        # movement speed (downward)
        self.speedy = 10


    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        # size
        self.width = 55
        self.height = 55
        # randomly choose power type
        self.type = random.choice(['health', 'gun'])
        # self.image = pygame.image.load("betr mone.png")
        # self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.Surface((self.width,self.height))
        # color the image based on type
        if self.type == 'gun':
            self.image.fill(BLUE)
        else:  # 'health'
            self.image.fill(ORANGE)
        # rectangle
        self.rect = self.image.get_rect()
        self.rect.center = center
        # vertical speed
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # size
        self.width = 55
        self.height = 55
        # image
        self.image = pygame.image.load("mrbeasts money.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # rectangle
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        # movement speeds
        self.speedx = 0
        self.speedy = 10

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # size
        self.width = 90
        self.height = 110
        self.mob_images = [
            pygame.image.load("mrbeasts lawsuits.png"),
            pygame.image.load("document_02.png"),
            pygame.image.load("document_01.png"),
            pygame.image.load("scroll_01.png"),
            pygame.image.load("scroll_02_blue.png"),
            pygame.image.load("scroll_02_red.png"),
            pygame.image.load("scroll_02_grey.png"),
            pygame.image.load("scroll_02_purple.png"),
            pygame.image.load("scroll_02_green.png"),
            pygame.image.load("scroll_02_brown.png"),
            pygame.image.load("scroll_02_yellow.png"),
            pygame.image.load("scroll_02_cyan.png"),
            pygame.image.load("paper.png"),
            pygame.image.load("scroll_03.png")
        ]
        self.image = random.choice(self.mob_images)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # rectangle
        self.rect = self.image.get_rect()
        # spawn at random x and above the screen
        self.rect.x = random.randrange(0, WIDTH - self.width)
        self.rect.centery = random.randrange(-200, -100)
        # vertical speed
        self.speedy = random.randrange(10, 30)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top >= HEIGHT:
            self.rect.x = random.randrange(0, WIDTH - self.width)
            self.rect.centery = random.randrange(-200, -100)
            self.speedy = random.randrange(5, 20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # size
        self.width = 160
        self.height = 185
        # image
        self.image = pygame.image.load("mrbeast (1).png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mini_img = pygame.transform.scale(self.image, (40,46))
        # rectangle
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        # movement speeds and stats
        self.speedx = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.score = 0
        self.lives = 3
        self.health = 100
        self.power = 1
        self.power_time = pygame.time.get_ticks()



    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power==1:
                b = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(b)
            bullets.add(b)
        if self.power==2:
            b1 = Bullet(self.rect.left, self.rect.top)
            b2 = Bullet(self.rect.right, self.rect.top)
            all_sprites.add(b1)
            bullets.add(b1)
            all_sprites.add(b2)
            bullets.add(b2)

    def update(self):
        if self.power>=2 and pygame.time.get_ticks()-self.power_time>5000:
            self.power -=1
            self.power_time =pygame.time.get_ticks()
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx


def start_screen():
    screen.fill(BLUE)
    draw_text(screen, "my game", 64, WIDTH // 2,HEIGHT// 4, WHITE)
    draw_text(screen, "Use Arrow Keys For Movement", 32,  WIDTH // 2, HEIGHT//2, WHITE)
    draw_text(screen, "Press A To Begin", 32, WIDTH // 2, 3*HEIGHT//4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting=False
def lose_screen():
    screen.fill(BLUE)
    draw_text(screen, "You Lost", 64, WIDTH // 2,HEIGHT// 4, WHITE)
    draw_text(screen, "Use Arrow Keys For Movement", 32,  WIDTH // 2, HEIGHT//2, WHITE)
    draw_text(screen, "Press A To Begin", 32, WIDTH // 2, 3*HEIGHT//4, WHITE)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            keystate = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if keystate[pygame.K_a]:
                    waiting=False

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.expl_anim = {}
        self.width = 40
        self.height = 40
            # Need shooting

        self.expl_anim['sm'] = []
        self.expl_anim['lg'] = []
        self.load_image()
        self.image = pygame.Surface((self.width, self.height))
            # self.image.fill(BLUE)
            # self.player_img = pygame.image.load('club2.PNG')
            # self.player_img =pygame.transform.scale(self.player_img,(self.width,self.height))

            # self.image = self.expl_anim[self.size][0]
            # self.image=self.player_img
        self.rect = self.image.get_rect()
            # self.rect.x = WIDTH / 2
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 45
        self.last_update = pygame.time.get_ticks()
    def load_image(self):
        now = pygame.time.get_ticks()
        for i in range(1,10):
            filename = 'frame_{}_delay-0.07s.png'.format(i)
            img = pygame.image.load(filename)
            img_lg = pygame.transform.scale(img,(77,77))
            self.expl_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img,(32, 32))
            self.expl_anim['sm'].append(img_sm)
    def update(self):
        now =pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1

            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
        else:
            center = self.rect.center
            self.image = self.expl_anim[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center



class Coins(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.expl_anim = {}
        self.width = 40
        self.height = 40
            # Need shooting

        self.expl_anim['sml'] = []
        self.expl_anim['lrg'] = []
        self.load_image()
        self.image = pygame.Surface((self.width, self.height))
            # self.image.fill(BLUE)
            # self.player_img = pygame.image.load('club2.PNG')
            # self.player_img =pygame.transform.scale(self.player_img,(self.width,self.height))

            # self.image = self.expl_anim[self.size][0]
            # self.image=self.player_img
        self.rect = self.image.get_rect()
            # self.rect.x = WIDTH / 2
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 45
        self.last_update = pygame.time.get_ticks()
    def load_image(self):
        now = pygame.time.get_ticks()
        for i in range(10,20):
            filename = 'frame_{}_delay-0.04s.gif'.format(i)
            img = pygame.image.load(filename)
            img_lg = pygame.transform.scale(img,(77,77))
            self.expl_anim['lrg'].append(img_lg)
            img_sm = pygame.transform.scale(img,(32, 32))
            self.expl_anim['sml'].append(img_sm)
    def update(self):
        now =pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1

            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
        else:
            center = self.rect.center
            self.image = self.expl_anim[self.size][self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")
clock = pygame.time.Clock()

# sprite groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()
beam_groups = pygame.sprite.Group()

gavels = pygame.sprite.Group()








# Load background image
background_img = pygame.image.load("court room.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
background_rect = background_img.get_rect()

# Timer variables for gavel to like beam thing
last_gavel= pygame.time.get_ticks()
gavel_interval = 10000
last_strike_time = pygame.time.get_ticks()
strike_interval = 5500

running = True
new_game=True
while running:
    if new_game:
        start_screen()
        new_game = False
        ship = Player()
        all_sprites.add(ship)
        for i in range(8):
            newmob()
        gavel = Gavel()
        # all_sprites.add(gavel)
        # gavels.add(gavel)
        end_level=False
        no_beam = True
        new_beam = Beam(gavel.rect.centerx, gavel.rect.bottom)
    expl = Coins(Player.rect.midtop, 'sm')

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # beam from hammer gavel thing
    if no_beam:

        current_time = pygame.time.get_ticks()
        if current_time - last_strike_time >= strike_interval:
            gavel = Gavel()
            all_sprites.add(gavel)
            gavels.add(gavel)
            new_beam = Beam(gavel.rect.centerx, gavel.rect.bottom)
            all_sprites.add(new_beam)
            beam_groups.add(new_beam)
            last_strike_time = current_time
            no_beam = False

    current_time = pygame.time.get_ticks()
    # if current_time - last_gavel >= gavel_interval:
    #     all_sprites.add(gavel)
    #     gavels.add(gavel)
    #     last_gavel = current_time



    hit_mobs = pygame.sprite.groupcollide(mobs, bullets, True, True)
    if hit_mobs:
        for hit in hit_mobs:
            expl = Explosion(hit.rect.center, 'lrg')
            all_sprites.add(expl)
            newmob()
            ship.score += 10
            # if random.random() > 0.1:
            #     pow_obj = Power(hit.rect.center)
            #     all_sprites.add(pow_obj)
            #     powers.add(pow_obj)
            newmob()

    #hitpower = pygame.sprite.spritecollide(ship, powers, True)
    # for hit in hitpower:
    #     if hit.type=='health':
    #         ship.health += random.randrange(10,30)
    #         if ship.health>=ship.health==100:
    #             ship.health=100
    #     if hit.type=='gun':
    #         ship.power+=1

    # hit_player = pygame.sprite.spritecollide(ship,powers, True)
    # if hit_player:
    #     ship.health -= 25
    #     newmob()
    # if ship.health <= 0:
    #     ship.health = 100
    #     ship.lives -= 1
    # if ship.lives <= 0:
    #     running = False
    if new_beam.rect.top>HEIGHT:
        for b in beam_groups:
            b.kill()
        gavel.kill()

        no_beam = True
    hit_player = pygame.sprite.spritecollide(ship,mobs,True)
    if hit_player:
        ship.health -= random.randrange(5,20)
        newmob()
    if pygame.sprite.spritecollide(ship, beam_groups, True):
        ship.lives -= 1
        for b in beam_groups:
            b.kill()
        gavel.kill()
        no_beam = True
    if ship.lives <= 0:
        new_game=True
        end_level=True
        ship.kill()
        lose_screen()
        new_game=True
        #kill all - to reset
    if ship.health <=0:
        ship.lives -=1
        ship.health = 100


    if end_level:
        end_level=False
        for g in gavels:
            g.kill()
        for m in mobs:
            m.kill()

    # Update all sprites
    all_sprites.update()

    # Draw/render
    screen.blit(background_img, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(ship.score), 32, WIDTH // 2, 10, WHITE)
    draw_text(screen, str(ship.lives), 32, 3 * WIDTH // 4, 10, WHITE)
    draw_text(screen, str(ship.health), 32, WIDTH // 4, 10, WHITE)
    draw_shield_bar(screen, 20, 5, ship.health)
    draw_lives(screen, WIDTH - 150, 5, ship.lives, ship.mini_img)
    pygame.display.flip()

pygame.quit()



#whenever a mob is killed it duplicates
#upgrades r disabled

#graphics:

#white in things are transparent
#make beam bigger, maybe animated
#fix coin pile effect on hit player
