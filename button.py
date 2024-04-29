import pygame as pg

class Button:
    def __init__(
            self, x, y, padding_x=15, padding_y=15,
            text="Label", font=None, fsize=16,
            color_normal=(129, 14, 88), color_hover=(129, 14, 88),
            color_active=(129, 14, 88), text_color=(255, 255, 255)
    ):
        font = pg.font.Font(font, fsize)
        self.image = font.render(text, True, text_color)
        self.rect = self.image.get_rect()
        self.button_rect = pg.Rect(0, 0, self.rect.width + padding_x * 2, self.rect.height + padding_y * 2)
        self.button_rect.x, self.button_rect.y = x, y
        self.rect.center = self.button_rect.center
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.color_active = color_active
        self.status = 'normal'

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEMOTION:
                if self.button_rect.collidepoint(event.pos):
                    self.status = 'hover'
                else:
                    self.status = 'normal'
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_rect.collidepoint(event.pos):
                    self.status = 'active'
                else:
                    self.status = 'normal'

    def draw(self, surface):
        if self.status == 'active':
            color = self.color_active
        elif self.status == 'hover':
            color = self.color_hover
        else:
            color = self.color_normal  
        pg.draw.rect(surface, color, self.button_rect, border_radius=10)
        surface.blit(self.image, self.rect)

if __name__ == '__main__':
    pg.init()
    mw = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()

    btn = Button(
        100, 100, 60, 10, "New game", fsize=24, color_normal=(128, 176, 255),
        color_hover=(69, 120, 204), color_active=(45, 95, 179)
    )

    game = True
    while game:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                game = False

        btn.update(events)
        btn.draw(mw)

        clock.tick(60)
        pg.display.update()
