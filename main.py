import pygame, os, random, time

pygame.init()

SIZESCREEN = WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()
# wczytywanie grafik
path = os.path.join(os.getcwd(), 'images')
file_names = os.listdir(path)
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']
BACKGROUND = pygame.image.load(os.path.join(path, 'Background.png')).convert()
Failed_Attack_P1 = pygame.USEREVENT + 1
Failed_Attack_P2 = pygame.USEREVENT + 2

file_names.remove('Background.png')
IMAGES = {}
for file_name in file_names:
    image_name = file_name[:-4].upper()
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)


# klasa reprezentująca gracza
class Player(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.lives = 3
        self.score = 0
        self.CanAttack = False
        self.FailedAttack = False
        self.IsAttacking = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def Attack(self):

        if exclamation.AllowAttack and self.FailedAttack == False:
            if self.image == IMAGES['PLAYER2']:
                self.image = IMAGES['PLAYER2ATTACK']
                player.lives -= 1
                exclamation.AllowAttack = False
                player2.IsAttacking = True
                player.image = IMAGES['PLAYER1DAMAGE']
            elif self.image == IMAGES['PLAYER']:
                self.image = IMAGES['PLAYER1ATTACK']
                player2.lives -= 1
                exclamation.AllowAttack = False
                player2.image = IMAGES['PLAYER2DAMAGE']
                player.IsAttacking = True
        else:
            print("Atak Zjeabyy")
            self.FailedAttack = True
            if self.image == IMAGES['PLAYER']:
                cross.drawing = True
                pygame.time.set_timer(Failed_Attack_P1, 3000, 1)
            if self.image == IMAGES['PLAYER2']:
                cross2.drawing = True
                pygame.time.set_timer(Failed_Attack_P2, 3000, 1)


class Exclamation():
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.AllowAttack = False
        self.IsDraw = False
        self.start_time = None
        self.start_time2 = None
        self.random_interval = random.randint(1000, 3000)  # Random interval between 1 and 3 seconds
    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def CheckAttack(self):
        if exclamation.AllowAttack:
            if self.start_time is None:
                self.start_time = pygame.time.get_ticks()
            # Check the time elapsed
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time <= 500:  # 2000 milliseconds = 2 seconds
                exclamation.draw(screen)
                player.CanAttack = True
                player2.CanAttack = True
            else:
                exclamation.AllowAttack = False
                self.start_time = None
                player.CanAttack = False
                player2.CanAttack = False

    def StartTimer(self):
        current_time2 = pygame.time.get_ticks()
        if self.start_time2 is None:
            self.start_time2 = current_time2
            self.random_interval = random.randint(2000, 4000)  # Generate new random interval
            print(self.random_interval/1000)
        if current_time2 - self.start_time2 >= self.random_interval:
            # Perform the action
            self.AllowAttack = True
            # Reset the timer
            self.start_time2 = current_time2
            self.random_interval = random.randint(2000, 4000)  # Generate new random interval for next action
            print(self.random_interval/1000)

class Cross():
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.drawing = False
    def draw(self, surface):
        if self.drawing:
            surface.blit(self.image, self.rect)

class Level():
    def __init__(self, player, player2):
        self.player1 = player
        self.player2 = player2
        self.pointP1 = 0
        self.PointP2 = 0
        self.IntroWasPlayed = False

    def draw(self):
        screen.blit(BACKGROUND, [0, 0])
        for i in range(self.player1.lives):
            screen.blit(IMAGES['HEARTH2'], (20 + i * 120, 750))
        for i in range(self.player2.lives):
            screen.blit(IMAGES['HEARTH2'], (1460 - i * 120, 20))



# konkretyzacja obiektów
player = Player(IMAGES['PLAYER'], -150, 500)
player2 = Player(IMAGES['PLAYER2'], 1750, 300)
level = Level(player, player2)
exclamation = Exclamation(IMAGES['EXCLAMATION'], 800, 400)
cross = Cross(IMAGES['CROSS'], 550, 500)
cross2 = Cross(IMAGES['CROSS'], 1050, 300)

# pętla gry
window_open = True

while window_open:

    # pętla zdarzeń
    level.draw()
    if not level.IntroWasPlayed:
        if player.rect.x < 550-190 and player2.rect.x > 1050-190:
            player.rect.x += 10
            player2.rect.x -= 10
        else:
            level.IntroWasPlayed = True
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
            if event.key == pygame.K_RIGHT and event.key == pygame.K_LEFT:
                print("Remis")
            #ATAKI GRACZY
            if event.key == pygame.K_RIGHT:
                player2.Attack()
            if event.key == pygame.K_LEFT:
                player.Attack()

        if event.type == pygame.QUIT:
            window_open = False
        if event.type == Failed_Attack_P1:
            player.FailedAttack = False
            cross.drawing = False
        if event.type == Failed_Attack_P2:
            player2.FailedAttack = False
            cross2.drawing = False



    exclamation.StartTimer()

    if player.IsAttacking:
        if player.rect.x < 600:
            player.rect.x += 60
        if player.rect.y > 200:
            player.rect.y -= 20
        if player.rect.x > 600 and player.rect.y < 200:
            pygame.time.delay(500)
            player.image = IMAGES['PLAYER']
            player2.image = IMAGES["PLAYER2"]
            player.rect.center = 550, 500
            player2.FailedAttack = False
            cross2.drawing = False
            player.IsAttacking = False

    if player2.IsAttacking:
        if player2.rect.x > 600:
            player2.rect.x -= 60
        if player2.rect.y < 400:
            player2.rect.y += 20
        if player2.rect.x < 600 and player.rect.y > 200:
            pygame.time.delay(500)
            player2.image = IMAGES['PLAYER2']
            player.image = IMAGES["PLAYER"]
            player2.rect.center = 1050, 300
            player.FailedAttack = False
            cross.drawing = False
            player2.IsAttacking = False

    # rysowanie i aktualizacja obiektów
    player.draw(screen)
    player2.draw(screen)
    exclamation.CheckAttack()
    cross.draw(screen)
    cross2.draw(screen)


    # aktualizacja okna gry
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
