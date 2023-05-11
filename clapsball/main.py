from math import *
import pygame as pg
import sys

pg.init()
shot_timer = pg.time.get_ticks()
pg.display.set_caption('')

class player_class():
    def __init__(self, image, x, y, size):
        self.face = pg.image.load(image)
        self.face.set_colorkey((255, 255, 255))
        self.x = x
        self.y = y
        self.size = size
        self.move_list = []

    def render(self):
        screen.blit(self.face, (self.x, self.y))

    def move(self, b):
        for i in self.move_list:
            self.x += i[0]
            self.y += i[1]
            i[2] -= 1
            if i[2] == 0:
                self.move_list.remove(i)


class ball_class():
    def __init__(self, image, x, y, size):
        self.face = pg.image.load(image)
        self.face.set_colorkey((255, 255, 255))
        self.x = x
        self.y = y
        self.size = size
        self.move_list = []

    def move(self, p):
        global ball_shot, ball_near
        for i in self.move_list:
            self.x += i[0]
            self.y += i[1]
            if (self.y < 70):
                self.x -= i[0]
                self.y -= i[1]
                i[1] *= -1
            if (self.y + self.size > 470):
                self.x -= i[0]
                self.y -= i[1]
                i[1] *= -1
            if (self.x < 70):
                self.x -= i[0]
                self.y -= i[1]
                i[0] *= -1
            if (self.x + self.size > 890):
                self.x -= i[0]
                self.y -= i[1]
                i[0] *= -1
            i[2] -= 1
            if i[2] == 0:
                ball_shot = False
                self.move_list.remove(i)
            else:
                if (pg.time.get_ticks() - shot_timer >= 2.5) and (ball_near):
                    k1 = (self.x + self.size / 2) - (p.x + p.size / 2)
                    k2 = (self.y + self.size / 2) - (p.y + p.size / 2)
                    h = sqrt(k1 ** 2 + k2 ** 2)
                    a = (step * k1) / h
                    b = (step * k2) / h
                    i[1] = b
                i[0] -= i[0] / i[2]
                i[1] -= i[1] / i[2]

    def render(self):
        screen.blit(self.face, (self.x, self.y))

def screen_starting():
    pg.mouse.set_visible(True)
    starting = True
    while starting:
        pointer = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if (event.button == 1) and (pointer[0] >= 360) and (pointer[0] <= 660) and (pointer[1] >= 170) and (pointer[1] <= 370):
                    pg.display.flip()
                    pg.time.delay(250)
                    screen.blit(loading_1, (0, 0))
                    pg.time.delay(250)
                    pg.display.flip()
                    screen.blit(loading_2, (0, 0))
                    pg.time.delay(250)
                    pg.display.flip()
                    screen.blit(loading_3, (0, 0))
                    pg.time.delay(250)
                    pg.display.flip()
                    screen.blit(loading_4, (0, 0))
                    pg.time.delay(250)
                    pg.display.flip()
                    screen.blit(loading_4, (0, 0))
                    pg.time.delay(750)
                    pg.display.flip()
                    starting = False
        screen.blit(start_screen, (0, 0))
        pg.display.flip()
def intersect_shot(p, b):
    p_cen = [p.x + p.size / 2, p.y + p.size / 2]
    b_cen = [b.x + b.size / 2, b.y + b.size / 2]
    r = (b.size / 2) + (p.size / 2) + 10
    return abs(p_cen[0] - b_cen[0]) <= r and abs(p_cen[1] - b_cen[1]) <= r
def intersect_move(p, b):
    r = p.size / 2 + b.size / 2
    k1 = abs((p.x + p.size / 2) - (b.x + b.size / 2))
    k2 = abs((p.y + p.size / 2) - (b.y + b.size / 2))
    s = sqrt(k1 ** 2 + k2 ** 2)
    return s < r

start_screen = pg.image.load('play_button.png')
loading_1 = pg.image.load('loading_1.png')
loading_2 = pg.image.load('loading_2.png')
loading_3 = pg.image.load('loading_3.png')
loading_4 = pg.image.load('loading_4.png')
screen = pg.display.set_mode((960, 540))
field = pg.image.load('grass.png')
screen.blit(field, (0, 0))

player = player_class('player_loy.png', 140, 240, 61)
step = 0.3
step_diog = 0.21213

ball = ball_class('ball.png', 465, 255, 31)
ball_near = False
ball_shot = False

pg.key.set_repeat(1, 1)
screen_starting()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        keys = pg.key.get_pressed()
        if (keys[pg.K_w]) and (keys[pg.K_d]) and (player.x + player.size <= 960) and (player.y >= 0):
            player.move_list = [[step_diog, 0 - step_diog, 1]]
        elif (keys[pg.K_w]) and (keys[pg.K_a]) and (player.x >= 0) and (player.y >= 0):
            player.move_list = [[0 - step_diog, 0 - step_diog, 1]]
        elif (keys[pg.K_s]) and (keys[pg.K_d]) and (player.x + player.size <= 960) and (player.y + player.size <= 540):
            player.move_list = [[step_diog, step_diog, 1]]
        elif (keys[pg.K_s]) and (keys[pg.K_a]) and (player.x >= 0) and (player.y + player.size <= 540):
            player.move_list = [[0 - step_diog, step_diog, 1]]
        elif (keys[pg.K_w]) and (player.y - step >= 0):
            player.move_list = [[0, 0 - step, 1]]
        elif (keys[pg.K_a]) and (player.x - step >= 0):
            player.move_list = [[0 - step, 0, 1]]
        elif (keys[pg.K_s]) and (player.y + step + player.size <= 540):
            player.move_list = [[0, step, 1]]
        elif (keys[pg.K_d]) and (player.x + step + player.size <= 960):
            player.move_list = [[step, 0, 1]]
        if (event.type == pg.MOUSEBUTTONDOWN):
            if event.button == 1 and intersect_shot(player, ball):
                k1 = (ball.x + ball.size / 2) - (player.x + player.size / 2)
                k2 = (ball.y + ball.size / 2) - (player.y + player.size / 2)
                h = sqrt(k1 ** 2 + k2 ** 2)
                a = (step * k1) / h
                b = (step * k2) / h
                shot_timer = pg.time.get_ticks()
                ball.move_list = [[a * 3, b * 3, 1000]]
                ball_shot = True
    if intersect_move(player, ball) and (pg.time.get_ticks() - shot_timer >= 2.5):
        if (not ball_shot):
            k1 = (ball.x + ball.size / 2) - (player.x + player.size / 2)
            k2 = (ball.y + ball.size / 2) - (player.y + player.size / 2);
            h = sqrt(k1 ** 2 + k2 ** 2)
            s = (player.size / 2 + ball.size / 2) - h
            a = (s * k1) / h
            b = (s * k2) / h
            ball.move_list = [[a, b, 1]]
        ball_near = True
    screen.blit(field, (0, 0))
    ball.move(player)
    ball.render()
    ball_near = False
    player.move(ball)
    player.render()
    pg.display.flip()