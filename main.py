import pygame, os, random

pygame.init()

SIZESCREEN = WIDTH, HEIGHT = 1366, 740
screen = pygame.display.set_mode(SIZESCREEN)
clock = pygame.time.Clock()
# wczytywanie grafik
# path = os.path.join(os.pardir, 'images')
path = os.path.join(os.getcwd(), 'images')
file_names = os.listdir(path)
LIGHTGREEN = pygame.color.THECOLORS['lightgreen']


BACKGROUND = pygame.image.load(os.path.join(path, 'background.jpg')).convert()
file_names.remove('background.jpg')
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
        self.level = None
        self.lives = 3

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#konkretyzacja obiektów
player = Player(IMAGES['PLAYER'], 500, 500)


#pętla gry
window_open = True
while window_open:
    # pętla zdarzeń
    #screen.fill(LIGHTGREEN)
    screen.blit(BACKGROUND, [-300, -300])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window_open = False
        if event.type == pygame.QUIT:
            window_open = False

    # rysowanie i aktualizacja obiektów
    player.draw(screen)

    # aktualizacja okna gry
    pygame.display.flip()

    clock.tick(60)


pygame.quit()







