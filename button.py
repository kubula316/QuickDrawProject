import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image, image2, cx, cy):
        super().__init__()
        self.image = image
        self.image2 = image2
        self.rect = self.image.get_rect()
        self.rect.center = cx, cy
        self.sound_hovered = pygame.mixer.Sound('sounds/hover.wav')
        self.hover_sound_played = False

    def draw(self, surface):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.image, self.rect)
            self.hover_sound_played = False
        else:
            surface.blit(self.image2, self.rect)
            if not self.hover_sound_played:
                self.sound_hovered.play()
                self.hover_sound_played = True