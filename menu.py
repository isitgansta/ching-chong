import pygame as pg
from button import Button


class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.play_with_bot = Button(
            30, 30, 100, 30, "Play with Bot", None, 20,
            (180, 0, 0), (140, 0, 0), (100, 0, 0),
            (255, 255, 255))
        self.play_with_friend = Button(
            30, 80, 100, 30, "Play with Friend", None, 20,
            (180, 0, 0), (140, 0, 0), (100, 0, 0),
            (255, 255, 255))
        self.settings = Button(
            30, 130, 100, 30, "Settings", None, 20,
            (180, 0, 0), (140, 0, 0), (100, 0, 0),
            (255, 255, 255))
        self.exit = Button(
            30, 180, 100, 30, "Exit", None, 20,
            (180, 0, 0), (140, 0, 0), (100, 0, 0),
            (255, 255, 255))
        self.clock = pg.time.Clock()
        self.FPS = 30

    def update(self, events):
        self.play_with_bot.update(events)
        self.play_with_friend.update(events)
        self.settings.update(events)
        self.exit.update(events)

    def draw(self):
        self.surface.fill((200, 255, 255))

        self.play_with_bot.draw(self.surface)
        self.play_with_friend.draw(self.surface)
        self.settings.draw(self.surface)
        self.exit.draw(self.surface)

class DVD_ball:
    def __init__(self, surface):
        self.surface = surface
        self.ball = pg.transform.scale(pg.image.load("ball.png"), (50,50))
        self.rect = self.ball.get_rect()
        self.rect.x = surface.get_rect().width // 2
        self.rect.y = surface.get_rect().height // 2
        self.speed_y = 5
        self.speed_x = 5
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x < 0:
            self.speed_x *= -1
        if self.rect.x < 0 or self.rect.width < self.surface.get_rect().width:
            self.speed_x *= -1
        if self.rect.y < 0:
            self.speed_y *= -1
        if self.rect.y < 0 or self.rect.height < self.surface.get_rect().height:
            self.speed_y *= -1

if __name__ == '__main__':
    pg.init()

    mw = pg.display.set_mode((700, 500))

    menu = Menu(mw)

    game = True
    while game:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                game = False
        
        menu.update(events)
        menu.draw()

        pg.display.flip()
        pg.time.Clock().tick(30)
