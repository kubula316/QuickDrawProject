import pygame


class Text(pygame.font.Font):
    def __init__(self, text, text_color, pc_x, pc_y, font_size=36, font_type=None):
        super().__init__(font_type, font_size)
        self.text = str(text)
        self.text_color = text_color
        self.pc_x = pc_x
        self.pc_y = pc_y

    def draw(self, surface):
        self.image = self.render(self.text, True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.pc_x, self.pc_y
        surface.blit(self.image, self.rect)