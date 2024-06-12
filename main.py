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
P1ATTACK = pygame.USEREVENT + 1
P2ATTACK = pygame.USEREVENT + 2
pygame.time.set_timer(P1ATTACK, 1)
pygame.time.set_timer(P2ATTACK, 1)

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
        if exclamation.AllowAttack:
            if self.image == IMAGES['PLAYER2']:
                self.image = IMAGES['PLAYER2ATTACK']
                if player.lives > 1:
                    player.lives -= 1
                    #aniamcja ataku z cofnieciem
                if player.lives == 1:
                    print("koniec gry WYGRYWA P2")
                    # aniamcja ataku bez cofnieciem
                    #zakonczenie gry
            elif self.image == IMAGES['PLAYER']:
                self.image = IMAGES['PLAYER1ATTACK']
                player2.lives -= 1
                exclamation.AllowAttack = False
                player2.image = IMAGES['PLAYER2DAMAGE']
                player.IsAttacking = True

        else:
            print("Atak Zjeabyy")




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


# konkretyzacja obiektów
player = Player(IMAGES['PLAYER'], 550, 500)
player2 = Player(IMAGES['PLAYER2'], 1050, 300)
exclamation = Exclamation(IMAGES['EXCLAMATION'], 800, 400)


# pętla gry
window_open = True

while window_open:

    # pętla zdarzeń
    screen.blit(BACKGROUND, [0, 0])
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



    # rysowanie i aktualizacja obiektów
    exclamation.StartTimer()
    if event.type == P1ATTACK:
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
                player.IsAttacking = False









    player.draw(screen)
    player2.draw(screen)
    exclamation.CheckAttack()








    # aktualizacja okna gry
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
