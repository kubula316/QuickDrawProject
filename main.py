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
ATTACKTIME = pygame.USEREVENT +1
start_time = None
start_time2 = None
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
        self.IsAttacked = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Exclamation():
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.AllowAttack = False
        self.IsDraw = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)





# konkretyzacja obiektów
player = Player(IMAGES['PLAYER'], 550, 500)
player2 = Player(IMAGES['PLAYER2'], 1050, 300)
exclamation = Exclamation(IMAGES['EXCLAMATION'], 800, 400)


# pętla gry
window_open = True
start_time2 = pygame.time.get_ticks()

while window_open:
    # pętla zdarzeń
    screen.blit(BACKGROUND, [0, 0])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
            if event.key == pygame.K_SPACE:
                exclamation.AllowAttack = True
                print("DUPA")
        if event.type == pygame.QUIT:
            window_open = False



    # rysowanie i aktualizacja obiektów
    player.draw(screen)
    player2.draw(screen)

    if exclamation.AllowAttack:
        if start_time is None:
            start_time = pygame.time.get_ticks()
        # Check the time elapsed
        current_time = pygame.time.get_ticks()
        if current_time - start_time <= 2000:  # 2000 milliseconds = 2 seconds
            exclamation.draw(screen)
            #Dodac zminna na attak
        else:
            exclamation.AllowAttack = False
            start_time = None






    # aktualizacja okna gry
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
